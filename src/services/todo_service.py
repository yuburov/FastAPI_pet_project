from datetime import datetime

from config import JWT_SECRET_KEY
from models.todos import Todo
from typing import List

from repositories.auth_repo import JWTRepo
from schemas.todos import TodoSchema, PriorityEnum
from adapters.unitofwork import IUnitOfWork


class TodoService:
    @staticmethod
    async def list_todos(
            uow: IUnitOfWork,
            credentials: str,
            filter_by_date: str = None,
            filter_by_priority: PriorityEnum = None,
            sort_by_date: str = None,
            sort_by_priority: str = None,
            page: int = 1,
            items_per_page: int = 10
    ) -> List[Todo]:
        token = JWTRepo.extract_token(credentials, JWT_SECRET_KEY)
        user_id = token['sub']
        async with uow:
            todos = await uow.todos.find_all(user_id=user_id)

            if filter_by_date:
                filter_date = datetime.strptime(filter_by_date, "%Y-%m-%dT%H:%M:%S.%f")
                todos = [todo for todo in todos if todo.created_at == filter_date]

            if filter_by_priority:
                todos = [todo for todo in todos if todo.priority == int(filter_by_priority)]

            if sort_by_date:
                todos = sorted(todos, key=lambda x: x.created_at, reverse=sort_by_date == 'desc')

            if sort_by_priority:
                todos = sorted(todos, key=lambda x: x.priority, reverse=sort_by_priority == 'desc')

            start_index = (page - 1) * items_per_page
            end_index = start_index + items_per_page
            paginated_todos = todos[start_index:end_index]
            return paginated_todos

    @staticmethod
    async def create_todo(data: TodoSchema, uow: IUnitOfWork, credentials: str) -> Todo:
        token = JWTRepo.extract_token(credentials, JWT_SECRET_KEY)
        user_id = token['sub']
        data_dict = data.model_dump()
        data_dict['user_id'] = user_id
        async with uow:
            todo = await uow.todos.add_one(data_dict)
            await uow.commit()
            return todo.to_read_model()

    @staticmethod
    async def retrieve_todo(todo_id: int, uow: IUnitOfWork, credentials: str) -> Todo:
        token = JWTRepo.extract_token(credentials, JWT_SECRET_KEY)
        user_id = token['sub']
        async with uow:
            todo = await uow.todos.find_one(id=todo_id, user_id=user_id)
            return todo.to_read_model()

    @staticmethod
    async def update_todo(todo_id, data: TodoSchema, uow: IUnitOfWork, credentials: str) -> Todo:
        todo = await TodoService.retrieve_todo(todo_id, uow, credentials)
        if todo:
            async with uow:
                todo = await uow.todos.edit_one(id=todo_id, data={**data.model_dump()})
                await uow.commit()
                return todo.to_read_model()

    @staticmethod
    async def delete_todo(todo_id: int, uow: IUnitOfWork, credentials: str) -> str:
        todo = await TodoService.retrieve_todo(todo_id, uow, credentials)
        if todo:
            async with uow:
                await uow.todos.delete_by_ids(Todo.id, [todo_id])
                await uow.commit()

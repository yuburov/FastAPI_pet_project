from src.config import JWT_SECRET_KEY
from src.models.todos import Todo
from typing import List

from src.repositories.auth_repo import JWTRepo
from src.schemas.todos import TodoSchema
from src.utils.unitofwork import IUnitOfWork


class TodoService:
    @staticmethod
    async def list_todos(uow: IUnitOfWork, credentials: str) -> List[Todo]:
        token = JWTRepo.extract_token(credentials, JWT_SECRET_KEY)
        user_id = token['sub']
        async with uow:
            todos = await uow.todos.find_all(user_id=user_id)
            return todos

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

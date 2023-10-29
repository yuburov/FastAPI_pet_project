from fastapi import APIRouter, Security, Query
from fastapi.security import HTTPAuthorizationCredentials

from api.dependencies import UOWDep
from repositories.auth_repo import JWTBearer
from schemas.todos import TodoSchema
from schemas.users import ResponseSchema
from services.todo_service import TodoService
from adapters.decorators import token_required

router = APIRouter(
    prefix="/todo",
    tags=["todo"],
)


@router.get('/', summary="Get all todos of the user", response_model=ResponseSchema, response_model_exclude_none=True)
@token_required(uow=UOWDep)
async def todos_list(uow: UOWDep,
                     credentials: HTTPAuthorizationCredentials = Security(JWTBearer()),
                     filter_by_date: str = Query(None, description="Filter by date"),
                     filter_by_priority: str = Query(None, description="Filter by priority"),
                     sort_by_date: str = Query(None, description="Sort by date"),
                     sort_by_priority: str = Query(None, description="Sort by priority"),
                     page: int = Query(1, description="Page number", ge=1),
                     items_per_page: int = Query(10, description="Items per page", le=100)
                     ):
    result = await TodoService.list_todos(
        uow, credentials, filter_by_date, filter_by_priority, sort_by_date, sort_by_priority, page, items_per_page
    )
    return ResponseSchema(detail="Successfully fetched data.", result=result)


@router.post('/create', summary="Create todo", response_model=ResponseSchema, response_model_exclude_none=True)
@token_required(uow=UOWDep)
async def create_todo(data: TodoSchema, uow: UOWDep,
                      credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    result = await TodoService.create_todo(data, uow, credentials)
    return ResponseSchema(detail='Data successfully created', result=result)


@router.get('/{todo_id}', summary="Get a todo by todo_id", response_model=ResponseSchema,
            response_model_exclude_none=True)
@token_required(uow=UOWDep)
async def retrieve_todo(todo_id: int, uow: UOWDep, credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    result = await TodoService.retrieve_todo(todo_id, uow, credentials)
    return ResponseSchema(detail='Success', result=result)


@router.put('/{todo_id}', summary="Update todo by task_id", response_model=ResponseSchema,
            response_model_exclude_none=True)
@token_required(uow=UOWDep)
async def update_todo(todo_id: int, data: TodoSchema, uow: UOWDep,
                      credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    result = await TodoService.update_todo(todo_id, data, uow, credentials)
    return ResponseSchema(detail='Successfully updated', result=result)


@router.delete('/{todo_id}', summary="Delete todo by todo_id", response_model=ResponseSchema,
               response_model_exclude_none=True)
@token_required(uow=UOWDep)
async def delete_todo(todo_id: int, uow: UOWDep,
                      credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    await TodoService.delete_todo(todo_id, uow, credentials)
    return ResponseSchema(detail="Successfully deleted", result="ok")

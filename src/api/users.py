from fastapi import APIRouter, Security

from api.dependencies import UOWDep
from schemas.users import ResponseSchema
from repositories.auth_repo import JWTBearer
from fastapi.security import HTTPAuthorizationCredentials

from services.user_service import UsersService
from adapters.decorators import token_required

router = APIRouter(
    prefix="/users",
    tags=['user'],
)


@router.get("", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_users(uow: UOWDep):
    result = await UsersService().get_users(uow)
    return ResponseSchema(detail='Success', result=result)


@router.get("/me", response_model=ResponseSchema, response_model_exclude_none=True)
@token_required(uow=UOWDep)
async def get_user_profile(uow: UOWDep, credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    result = await UsersService.get_user_profile(uow, credentials)
    return ResponseSchema(detail="Successfully fetch data!", result=result)

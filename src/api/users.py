from fastapi import APIRouter, Security, HTTPException

from src.api.dependencies import UOWDep
from src.config import JWT_SECRET_KEY
from src.schemas.users import ResponseSchema
from src.repositories.auth_repo import JWTBearer, JWTRepo
from fastapi.security import HTTPAuthorizationCredentials

from src.services.users import UsersService
from src.utils.decorators import token_required

router = APIRouter(
    prefix="/users",
    tags=['user'],
)


@router.get("")
async def get_users(uow: UOWDep):
    users = await UsersService().get_users(uow)
    return users


@router.get("/me", response_model=ResponseSchema, response_model_exclude_none=True)
@token_required(uow=UOWDep)
async def get_user_profile(uow: UOWDep, credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    result = await UsersService.get_user_profile(uow, credentials)
    return ResponseSchema(detail="Successfully fetch data!", result=result)

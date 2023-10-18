# from fastapi import APIRouter, Depends, Security
#
# from src.api.dependencies import UOWDep
# from src.config import JWT_SECRET_KEY
# from src.schemas.users import ResponseSchema
# from src.repositories.auth_repo import JWTBearer, JWTRepo
# from fastapi.security import HTTPAuthorizationCredentials
# from src.services.users import UsersService
#
# router = APIRouter(
#     prefix="/users",
#     tags=['user'],
#     dependencies=[Depends(JWTBearer())]
# )
#
#
# @router.get("/", response_model=ResponseSchema, response_model_exclude_none=True)
# async def get_user_profile(uow: UOWDep, credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
#     print(credentials)
#     token = JWTRepo.extract_token(credentials, JWT_SECRET_KEY)
#     result = await UsersService.get_user_profile(uow, token['username'])
#     return ResponseSchema(detail="Successfully fetch data!", result=result)
from fastapi import APIRouter, Depends, Security

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


@router.get("/", response_model=ResponseSchema, response_model_exclude_none=True)
@token_required(uow=UOWDep)
async def get_user_profile(uow: UOWDep, credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials, JWT_SECRET_KEY)
    user_id = token['sub']
    result = await UsersService.get_user_profile(uow, user_id)
    return ResponseSchema(detail="Successfully fetch data!", result=result)

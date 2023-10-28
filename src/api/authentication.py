import jose
from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status
from starlette.background import BackgroundTasks

from api.dependencies import UOWDep
from config import JWT_REFRESH_SECRET_KEY
from repositories.auth_repo import JWTBearer
from schemas.users import ResponseSchema, UserSchemaAdd, RequestDetails
from services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", response_model=ResponseSchema, response_model_exclude_none=True)
async def register(
        request: UserSchemaAdd,
        background_tasks: BackgroundTasks,
        uow: UOWDep
):
    result = await AuthService.register_service(uow, background_tasks, request)
    return ResponseSchema(detail="Data saved", result=result)


@router.post("/login", response_model=ResponseSchema)
async def login(request: RequestDetails, uow: UOWDep):
    result = await AuthService.logins_service(uow, request)
    return ResponseSchema(detail="Successfully login", result=result)


@router.post("/logout", response_model=ResponseSchema)
async def logout(uow: UOWDep, token: str = Depends(JWTBearer())):
    result = await AuthService.logout(uow, token)
    return ResponseSchema(detail='Successfully logout', result=result)


@router.post("/refresh", response_model=ResponseSchema)
async def refresh(uow: UOWDep, credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    try:
        result = await AuthService.refresh_service(uow, credentials, JWT_REFRESH_SECRET_KEY)
        return ResponseSchema(detail='Successfully refresh tokens', result=result)
    except jose.exceptions.JWTError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or expired token")

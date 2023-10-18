from fastapi import HTTPException
from functools import wraps

from src.config import JWT_SECRET_KEY
from src.repositories.auth_repo import JWTRepo
from src.utils.unitofwork import IUnitOfWork


def validate_credentials(credentials):
    if not credentials:
        raise HTTPException(status_code=403, detail="Invalid authorization code")


async def check_token(uow, user_id, credentials):
    async with uow:
        data = await uow.tokens.find_one(user_id=user_id, access_token=credentials, status=True)

    if not data:
        raise HTTPException(status_code=403, detail="Token blocked")


def token_required(uow: IUnitOfWork):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            credentials = kwargs.get('credentials')
            validate_credentials(credentials)

            token = JWTRepo.extract_token(credentials, JWT_SECRET_KEY)
            user_id = token.get('sub')
            await check_token(uow, user_id, credentials)

            return await func(*args, **kwargs)

        return wrapper

    return decorator

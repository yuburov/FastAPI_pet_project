from functools import wraps

from fastapi import HTTPException

from config import JWT_SECRET_KEY
from repositories.auth_repo import JWTRepo
from adapters.unitofwork import IUnitOfWork


def token_required(uow: IUnitOfWork):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            credentials = kwargs.get('credentials')
            if not credentials:
                raise HTTPException(status_code=403, detail="Invalid authorization code")

            token = JWTRepo.extract_token(credentials, JWT_SECRET_KEY)
            user_id = token.get('sub')
            uow = kwargs.get('uow')
            async with uow:
                data = await uow.tokens.find_one(user_id=user_id, access_token=credentials, status=True)

            if data:
                return await func(*args, **kwargs)
            else:
                raise HTTPException(status_code=403, detail="Token blocked")

        return wrapper

    return decorator

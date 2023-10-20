from src.config import JWT_SECRET_KEY
from src.repositories.auth_repo import JWTRepo
from src.adapters.unitofwork import IUnitOfWork


class UsersService:

    @staticmethod
    async def get_users(uow: IUnitOfWork):
        async with uow:
            users = await uow.users.find_all()
            return users

    @staticmethod
    async def get_user_profile(uow: IUnitOfWork, credentials: str):
        token = JWTRepo.extract_token(credentials, JWT_SECRET_KEY)
        user_id = token['sub']
        async with uow:
            user = await uow.users.find_one(id=user_id)
            return user.to_read_model()

from src.schemas.users import UserSchemaAdd
from src.utils.unitofwork import IUnitOfWork


class UsersService:
    @staticmethod
    async def add_user(uow: IUnitOfWork, user: UserSchemaAdd):
        user_dict = user.model_dump()
        async with uow:
            user_id = await uow.users.add_one(user_dict)
            await uow.commit()
            return user_id

    @staticmethod
    async def get_users(uow: IUnitOfWork):
        async with uow:
            users = await uow.users.find_all()
            return users

    @staticmethod
    async def get_user_profile(uow: IUnitOfWork, sub: str):
        async with uow:
            user = await uow.users.find_one(id=sub)
            return user.to_read_model()

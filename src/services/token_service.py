from datetime import datetime

from config import JWT_SECRET_KEY, JWT_REFRESH_SECRET_KEY
from models.tokens import TokenTable
from repositories.auth_repo import JWTRepo
from adapters.unitofwork import IUnitOfWork


class TokenService:
    @staticmethod
    def generate_tokens(user_id: str):
        access_token = JWTRepo(data={"sub": user_id}).generate_token(JWT_SECRET_KEY)
        refresh_token = JWTRepo(data={"sub": user_id}).generate_refresh_token(JWT_REFRESH_SECRET_KEY)
        return access_token, refresh_token

    @staticmethod
    async def add_token_to_db(uow: IUnitOfWork, user_id: str, access_token: str, refresh_token: str):
        token_db = TokenTable(user_id=user_id, access_token=access_token,
                              refresh_token=refresh_token, status=True, created_date=datetime.utcnow())
        await uow.tokens.add_one(token_db.to_dict())
        await uow.commit()

    @staticmethod
    async def update_tokens_in_db(uow: IUnitOfWork, user_id: str, access_token: str, refresh_token: str):
        async with uow:
            try:
                token_record = await uow.tokens.find_one(user_id=user_id, status=True)
                if token_record:
                    token_record.access_token = access_token
                    token_record.refresh_token = refresh_token
                    token_record.created_date = datetime.utcnow()
                    await uow.commit()
                else:
                    raise Exception(f"Token for user {user_id} not found in the database.")
            except Exception as e:
                print(f"An error occurred while updating tokens: {str(e)}")
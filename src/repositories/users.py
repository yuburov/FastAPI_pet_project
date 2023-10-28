from models.users import User
from adapters.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = User

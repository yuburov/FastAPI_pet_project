from models.tokens import TokenTable
from adapters.repository import SQLAlchemyRepository


class TokenRepository(SQLAlchemyRepository):
    model = TokenTable

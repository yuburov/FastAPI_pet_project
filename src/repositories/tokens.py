from src.models.tokens import TokenTable
from src.adapters.repository import SQLAlchemyRepository


class TokenRepository(SQLAlchemyRepository):
    model = TokenTable

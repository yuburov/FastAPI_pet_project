from src.models.tokens import TokenTable
from src.utils.repository import SQLAlchemyRepository


class TokenRepository(SQLAlchemyRepository):
    model = TokenTable

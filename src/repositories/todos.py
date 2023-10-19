from src.models.todos import Todo
from src.utils.repository import SQLAlchemyRepository


class TodosRepository(SQLAlchemyRepository):
    model = Todo

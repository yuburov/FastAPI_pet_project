from src.models.todos import Todo
from src.adapters.repository import SQLAlchemyRepository


class TodosRepository(SQLAlchemyRepository):
    model = Todo

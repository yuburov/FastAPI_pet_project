from models.todos import Todo
from adapters.repository import SQLAlchemyRepository


class TodosRepository(SQLAlchemyRepository):
    model = Todo

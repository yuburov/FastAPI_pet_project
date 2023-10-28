from datetime import datetime
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base
from schemas.todos import TodoSchema, TodoOut


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[id] = mapped_column(Integer(), primary_key=True)
    title: Mapped[str] = mapped_column(String(), index=True, nullable=True)
    description: Mapped[str] = mapped_column(String())
    status: Mapped[bool] = mapped_column(Boolean(), default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    user_id: Mapped[str] = mapped_column(String(), ForeignKey("users.id"))

    def to_read_model(self) -> TodoOut:
        return TodoSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

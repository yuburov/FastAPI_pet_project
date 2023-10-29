from datetime import datetime

from sqlalchemy import String, Boolean, ForeignKey, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base
from schemas.todos import TodoSchema, PriorityEnum, TodoOut


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[id] = mapped_column(Integer(), primary_key=True)
    title: Mapped[str] = mapped_column(String(), index=True, nullable=False)
    description: Mapped[str] = mapped_column(String())
    status: Mapped[bool] = mapped_column(Boolean(), default=False)
    priority: Mapped[int] = mapped_column(Integer(), default=PriorityEnum.medium)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    user_id: Mapped[str] = mapped_column(String(), ForeignKey("users.id"))

    def to_read_model(self):
        return TodoOut(
            id=self.id,
            title=self.title,
            description=self.description,
            status=self.status,
            priority=self.priority,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

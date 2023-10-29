from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class PriorityEnum(int, Enum):
    low = 1
    medium = 2
    high = 3


class TodoOut(BaseModel):
    id: int
    title: str
    description: str
    status: bool
    priority: PriorityEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TodoSchema(BaseModel):
    title: str = Field(..., json_schema_extra={"title": 'Title'}, max_length=55, min_length=1)
    description: str = Field(..., json_schema_extra={"description": 'Description'}, max_length=755, min_length=1)
    status: Optional[bool] = False
    priority: Optional[PriorityEnum] = PriorityEnum.medium

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority.value,
        }

    # def to_todo(self):
    #     return Todo(
    #         # преобразуйте поля TodoSchema в поля Todo
    #         title=self.title,
    #         description=self.description,
    #         status=self.status,
    #         priority=self.priority,
    #         created_at=datetime.utcnow(),
    #         updated_at=datetime.utcnow(),
    #     )
    #


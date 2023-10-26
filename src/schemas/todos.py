from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TodoOut(BaseModel):
    id: str
    title: str
    description: str
    status: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TodoSchema(BaseModel):
    title: str = Field(..., json_schema_extra={"title": 'Title'}, max_length=55, min_length=1)
    description: str = Field(..., json_schema_extra={"description": 'Description'}, max_length=755, min_length=1)
    status: Optional[bool] = False

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "status": self.status
        }



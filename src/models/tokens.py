from datetime import datetime

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base
from schemas.tokens import TokenCreate


class TokenTable(Base):
    __tablename__ = "tokens"

    user_id: Mapped[str] = mapped_column(String(200), nullable=False)
    access_token: Mapped[str] = mapped_column(String(450), primary_key=True)
    refresh_token: Mapped[str] = mapped_column(String(450), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean())
    created_date: Mapped[datetime] = mapped_column(default=datetime.utcnow())

    def to_read_model(self) -> TokenCreate:
        return TokenCreate(
            user_id=self.user_id,
            access_token=self.access_token,
            refresh_token=self.refresh_token,
            status=self.status,
            created_date=self.created_date
        )

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "status": self.status,
            "created_date": self.created_date
        }

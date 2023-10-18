from abc import ABC, abstractmethod
from typing import List, Union

from sqlalchemy import insert, select, update, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def edit_one(self, data: dict, **kwargs) -> int:
        filters = []
        for key, value in kwargs.items():
            filters.append(getattr(self.model, key) == value)

        stmt = update(self.model).values(**data).where(or_(*filters)).returning(self.model)
        res = await self.session.execute(stmt)

        return res.scalar_one()

    async def find_all(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res

    async def find_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        return res

    async def delete_by_ids(self, field, ids: List[str]):
        stmt = delete(self.model).where(field.in_(ids))
        await self.session.execute(stmt)

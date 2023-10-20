from typing import Annotated

from fastapi import Depends

from src.adapters.unitofwork import IUnitOfWork, UnitOfWork

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]

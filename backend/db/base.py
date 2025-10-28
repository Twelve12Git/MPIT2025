from sqlalchemy.orm import declared_attr, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession

class BaseModel(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower().replace('model', '')

class BaseDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


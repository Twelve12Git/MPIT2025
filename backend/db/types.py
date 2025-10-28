from sqlalchemy.dialects.postgresql import UUID as SQL_UUID
from sqlalchemy import DateTime as ORM_DateTime, ForeignKey, TypeDecorator, text, LargeBinary
from sqlalchemy.orm import mapped_column
from typing import Annotated
from uuid import UUID
from datetime import datetime


PrimaryKey = Annotated[UUID, mapped_column(SQL_UUID, primary_key=True, server_default=text("gen_random_uuid()"))]
CreateAt = Annotated[datetime, mapped_column(ORM_DateTime(timezone=False), nullable=False, server_default=text("now()"))]
UpdateAt = Annotated[datetime, mapped_column(ORM_DateTime(timezone=False), nullable=False, server_onupdate=text("now()"))]
UserIDForeignKey = Annotated[UUID, mapped_column(ForeignKey("user.id"), nullable=False)]

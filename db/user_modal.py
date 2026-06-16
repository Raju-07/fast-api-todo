from sqlalchemy import String,Integer,DateTime,func
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from datetime import datetime,timezone

class Base(DeclarativeBase):
    pass

class UserModal(Base):
    
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(Integer,index=True,primary_key=True,autoincrement=True)
    username: Mapped[str] = mapped_column(String,unique=True,index=True,nullable=False)
    email: Mapped[str] = mapped_column(String,unique=True,index=True,nullable=False)
    password: Mapped[str] = mapped_column(String,nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.current_timestamp(),
        default=lambda: datetime.now(timezone.utc)
        )

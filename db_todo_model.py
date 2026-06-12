from sqlalchemy import String,Integer,Date,Boolean,func,cast,DateTime,event
from sqlalchemy.orm import Mapped,DeclarativeBase,column_property
from sqlalchemy.orm import mapped_column as map_col
from datetime import date,timedelta,datetime,timezone

class Base(DeclarativeBase):
    pass

class Todo(Base):
    __tablename__ = "todo"

    id: Mapped[int] = map_col(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True)

    title: Mapped[str] = map_col(
        String(200),
        nullable=False)

    description: Mapped[str] = map_col(String(255))

    priority: Mapped[int] = map_col(
        Integer,
        nullable=False,
        default=2)

    created_at: Mapped[DateTime] = map_col(
        DateTime(timezone=True),
        default= lambda: datetime.now(timezone.utc),
        server_default=func.timezone("UTC",func.now()),
        nullable=False)
    
    updated_at: Mapped[DateTime] = map_col(
        DateTime(timezone = True),
        nullable=False,
        default= lambda: datetime.now(timezone.utc),
        server_default=func.timezone("UTC",func.now()),
        onupdate=datetime.now(timezone.utc),
        server_onupdate=func.timezone("UTC",func.now()),)

    expired_at: Mapped[Date] = map_col(
        Date,
        nullable=False,
        default= lambda:date.today()+timedelta(days=2))
    
    is_completed: Mapped[bool] = map_col(Boolean,nullable=False,default=False)
    
    time_left: Mapped[int] = column_property(
        cast(expired_at - func.current_date(), Integer)
    )

# Adding Event for updating at update_at column automatically

@event.listens_for(Todo,"before_update")
def update_timestamp(mapper,connection,target):
    target.updated_at = datetime.now(timezone.utc)  
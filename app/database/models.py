from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database.engine import Base

class Conversation(Base):

    __tablename__ = "conversations"

    id = Column(
        Integer,
        primary_key = True
    ) #sufficiente per uso singolo e locale 

    role = Column(
        String,
        nullable=False
    )


    content = Column(
        Text,
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
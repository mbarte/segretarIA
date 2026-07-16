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

class ProcessedEmails(Base):
    
    __tablename__ = "processed_emails"

    id = Column(
        Integer,
        primary_key=True
    )

    uid = Column(
        String,
        unique=True,
        nullable=False
    )

    processed_at = Column(
        DateTime,
        default=datetime.utcnow
    )
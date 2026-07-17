from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
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

class EmailModel(Base):

    __tablename__ = "emails"

    id = Column(
        Integer,
        primary_key=True
    )

    uid = Column(
        String,
        nullable=True
    )

    message_id = Column(
        String,
        unique=True, #vs duplicates
        nullable=False
    )

    subject = Column(
        String(500),
        nullable=False
    )

    sender = Column(
        String(500),
        nullable=False
    )

    recipients = Column(
        Text, #nel mapper json.dumps()
        nullable=False
    )

    date = Column(
        DateTime,
        nullable=False
    )

    body = Column(
        Text,
        nullable=False
    )

    is_read = Column(
        Boolean,
        default=False
    )

    has_attachments = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


    attachments = relationship(
        "AttachmentModel",
        back_populates="email",
        cascade="all, delete-orphan"
    )


class AttachmentModel(Base):

    __tablename__ = "attachments"

    id = Column(
        Integer,
        primary_key=True
    )

    email_id = Column(
        Integer,
        ForeignKey("emails.id"),
        nullable=False
    )

    filename = Column(
        String(500),
        nullable=False
    )

    content_type = Column(
        String(255),
        nullable=False
    )

    size = Column(
        Integer,
        nullable=False
    )


    email = relationship(
        "EmailModel",
        back_populates="attachments"
    )

    message_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )
    
    uid = Column(
        String,
        index=True,
        nullable=True
    )
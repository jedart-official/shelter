import sqlalchemy as db
from sqlalchemy import Integer, \
    Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()
engine = db.create_engine('sqlite:///shelter.db')
session_db = Session(bind=engine)


class SessionDB(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)


class MessageDB(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id', ondelete="CASCADE"),  nullable=False)
    message_id = Column(Integer, nullable=False)
    chat_id = Column(Integer, nullable=False)


Base.metadata.create_all(engine)

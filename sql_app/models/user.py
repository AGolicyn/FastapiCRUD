from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sql_app.db.session import Base
from sql_app.db.session import engine

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_pswd = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship('Item', back_populates='owner')

Base.metadata.create_all(bind=engine)
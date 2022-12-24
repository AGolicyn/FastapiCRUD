from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sql_app.db.session import Base
from sql_app.db.session import engine

Base.metadata.create_all(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # todo username: Mapped[str | None] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_pswd: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)

    items: Mapped[list['Item']] = relationship(back_populates='owner')


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str | None] = mapped_column(index=True)
    owner_id = mapped_column(ForeignKey('users.id'))

    owner: Mapped[User] = relationship(back_populates='items')

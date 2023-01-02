from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase): pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UpdateItem(BaseModel):
    id: int
    title: str | None = None
    description: str | None = None

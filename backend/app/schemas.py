from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    description: str | None = Field(default=None, max_length=500)


class Item(ItemCreate):
    id: int


class Health(BaseModel):
    status: str


class Hello(BaseModel):
    message: str

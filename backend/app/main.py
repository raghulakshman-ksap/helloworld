from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.schemas import Health, Hello, Item, ItemCreate

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for demonstration; replace with a database for real use.
_items: dict[int, Item] = {}


@app.get("/health", response_model=Health)
def health() -> Health:
    return Health(status="ok")


@app.get("/hello", response_model=Hello)
def hello() -> Hello:
    return Hello(message="Hello, World!")


@app.get("/items", response_model=list[Item])
def list_items() -> list[Item]:
    return list(_items.values())


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate) -> Item:
    item = Item(id=max(_items, default=0) + 1, **payload.model_dump())
    _items[item.id] = item
    return item


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    if item_id not in _items:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")
    return _items[item_id]

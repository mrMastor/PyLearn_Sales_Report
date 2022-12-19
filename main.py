from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
import service
from datetime import datetime
from base import init_models, get_session, session_destroy
from exceptions import UniqueViolationError, ForeignKeyViolationError

app = FastAPI()

class Store(BaseModel):
    id: int
    address: str
class Item(BaseModel):
    id: int
    name: str
    price: float
class SaleSchema(BaseModel):
    id_item: int
    id_store: int
class TopStores(BaseModel):
    id: int
    address: str
    summ: float
class TopItems(BaseModel):
    id: int
    name: str
    count: int
class AddStore(BaseModel):
    address: str
class AddItem(BaseModel):
    name: str
    price: float

@app.on_event("startup")
async def startup():
    await init_models()

@app.on_event("shutdown")
async def shutdown():
    await session_destroy()

@app.get("/")
async def index():
    await init_models()
    await session_destroy()
    print (datetime.now())
    return "Hello!"

@app.get("/items/", response_model=list[Item])
async def get_items(session: AsyncSession = Depends(get_session)):
    items = await service.get_items(session)
    try:
        return [Item(id=c.id, name=c.name, price=c.price) for c in items]
    except IntegrityError as ex:
        await session.rollback()
        raise ForeignKeyViolationError("Не корректный запрос")
    finally:
        await session_destroy()

@app.get("/stores/", response_model=list[Store])
async def get_store(session: AsyncSession = Depends(get_session)):
    stores = await service.get_store(session)
    try:
        return [Item(id=c.id, address=c.addresses) for c in stores]
    except IntegrityError as ex:
        await session.rollback()
        raise ForeignKeyViolationError("Не корректный запрос")
    finally:
        await session_destroy()

@app.get("/stores/top/", response_model=list[TopStores])
async def get_top_store(session: AsyncSession = Depends(get_session)):
    top_stores = await service.get_top_store(session)
    try:
        return [TopStores(id=c.id, address=c.address, summ=c.summ) for c in top_stores]
    except IntegrityError as ex:
        await session.rollback()
        raise ForeignKeyViolationError("Не корректный запрос")
    finally:
        await session_destroy()

@app.get("/items/top/", response_model=list[TopItems])
async def get_top_items(session: AsyncSession = Depends(get_session)):
    top_items = await service.get_top_items(session)
    try:
        return [TopItems(id=c.id, name=c.name, count=c.count) for c in top_items]
    except IntegrityError as ex:
        await session.rollback()
        raise ForeignKeyViolationError("Не корректный запрос")
    finally:
        await session_destroy()

@app.post("/sales/")
async def add_sale(sale: SaleSchema, session: AsyncSession = Depends(get_session)):
    sale = await service.add_sale(session, sale.id_store, sale.id_item)
    try:
        await session.commit()
        return sale
    except IntegrityError as ex:
        await session.rollback()
        raise ForeignKeyViolationError("Не корректные данные")
    finally:
        await session_destroy()

@app.post("/store/add/")
async def add_store(store: AddStore, session: AsyncSession = Depends(get_session)):
    store = await service.add_store(session, store.address)
    try:
        await session.commit()
        return store
    except IntegrityError as ex:
        await session.rollback()
        raise UniqueViolationError('Нарушена уникальность адреса магазина')
    finally:
        await session_destroy()

@app.post("/item/add/")
async def add_item(item: AddItem, session: AsyncSession = Depends(get_session)):
    item = await service.add_item(session, item.name, item.price)
    try:
        await session.commit()
        return item
    except IntegrityError as ex:
        await session.rollback()
        raise ForeignKeyViolationError("Что-то пошло не так")
    finally:
        await session_destroy()
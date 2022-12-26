from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
import service
from datetime import datetime
from base import init_model, get_session, session_destroy, async_session
from exceptions import UniqueViolationError, ForeignKeyViolationError
import json
import aiofiles
import asyncio

app = FastAPI()

class Store(BaseModel):
    id: int
    address: str
class Item(BaseModel):
    id: int
    name: str
    price: float
class Sale(BaseModel):
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
    await init_model()
    await load_files('jitems')
    await load_files('jstores')  
    await load_files('jsales')

@app.on_event("shutdown")
async def shutdown():
    await session_destroy()

@app.get("/")
async def index():
    print (datetime.now().strftime("%Y-%m-%d %H:%M"))
    return "Hello!"

@app.get("/items/", response_model=list[Item])
async def get_items(session: AsyncSession = Depends(get_session)):
    try:
        items = await service.get_items(session)
        return [Item(id=c.id, name=c.name, price=c.price) for c in items]
    except IntegrityError as ex:
        await session.rollback()
        raise ForeignKeyViolationError("Не корректный запрос")
    finally:
        await session_destroy()

@app.get("/stores/", response_model=list[Store])
async def get_store(session: AsyncSession = Depends(get_session)):
    try:
        stores = await service.get_store(session)
        return [Store(id=c.id, address=c.address) for c in stores]
    except IntegrityError as ex:
        await session.rollback()
        raise ForeignKeyViolationError("Не корректный запрос")
    finally:
        await session_destroy()

@app.get("/stores/top/", response_model=list[TopStores])
async def get_top_store(session: AsyncSession = Depends(get_session)):
    try:
        top_stores = await service.get_top_store(session)
        return [TopStores(id=c.id, address=c.address, summ=c.summ) for c in top_stores]
    except IntegrityError as ex:
        await session.rollback()
        raise ForeignKeyViolationError("Не корректный запрос")
    finally:
        await session_destroy()

@app.get("/items/top/", response_model=list[TopItems])
async def get_top_items(session: AsyncSession = Depends(get_session)):
    try:
        top_items = await service.get_top_items(session)
        x= [TopItems(id=id, name=name, count=count) for id, name, count in top_items]
        return x
    except IntegrityError as ex:
        await session.rollback()
        raise ForeignKeyViolationError("Не корректный запрос")
    finally:
        await session_destroy()


@app.post("/sales/")
async def add_sale(sale: Sale, session: AsyncSession = Depends(get_session)):
    sale = await service.add_sale(session, sale.id_store, sale.id_item)
    try:
        await session.commit()
        return sale
    except IntegrityError as ex:
        await session.rollback()
        raise ForeignKeyViolationError("Не корректные данные")
    finally:
        await session_destroy()

@app.post("/add/store/")
async def add_store(store: AddStore, session: AsyncSession = Depends(get_session)):
    store = await service.add_store(session, store.address)
    try:
        await session.commit()
        return store
    except IntegrityError as ex:
        await session.rollback()
        raise UniqueViolationError('Нарушена уникальность адреса магазина')

@app.post("/add/item/")
async def add_item(item: AddItem, session: AsyncSession = Depends(get_session)):
    item = await service.add_item(session=session, name=item.name, price=item.price)
    try:
        await session.commit()
        return item
    except IntegrityError as ex:
        await session.rollback()
        raise ForeignKeyViolationError("Что-то пошло не так")

async def load_files(fname: str):
    file_name = "data/"+ fname+".json"
    async with aiofiles.open(file_name, mode="r") as my_file:
        conn= async_session()
        try:
            jfile = json.loads(await my_file.read())
            if fname == "jitems":
                for i in jfile:
                    await add_item(item=AddItem.parse_obj(jfile[i]), session=conn)
                return print("Итемы успешно подгружены в БД")
            elif fname == "jstores":
                for i in jfile:
                    await add_store(store=AddStore.parse_obj(jfile[i]), session=conn)
                return print("Магазины успешно подгружены в БД")
            elif fname == 'jsales':
                for i in jfile:
                    await add_sale(sale=Sale.parse_obj(jfile[i]), session=conn)
                return print("Продажи успешно подгружены в БД")
        except:
            raise ("Пробблемы в блоке работы с файлом")

if __name__=="__main__":
    asyncio.run(get_top_items())
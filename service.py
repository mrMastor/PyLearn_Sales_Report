from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from model import *
from datetime import datetime

async def get_items(session: AsyncSession) -> list[Item]:
    result = await session.execute(select(Item))
    return result.scalars().all

async def get_store(session: AsyncSession) -> list[Store]:
    result = await session.execute(select(Store))
    return result.scalars().all

async def get_top_store(session: AsyncSession) -> list[Item]:
    result = await session.execute(select(Item))
    return result.scalars().all

async def get_top_items(session: AsyncSession) -> list[Item]:
    result = await session.execute(select(Item))
    return result.scalars().all

async def add_sale(session: AsyncSession, id_store: int, id_item: int):
    new_sale = Sale(
                    sale_time=datetime.today(), 
                    store_id=id_store, 
                    item_id=id_item)
    session.add(new_sale)
    return new_sale


async def add_item(session: AsyncSession, name: str, price: float):
    new_item = Item(name=name, price=price)
    session.add(new_item)
    return new_item

async def add_store(session: AsyncSession, address: String):
    new_store = Store(address=address)
    session.add(new_store)
    return new_store
from sqlalchemy import String, Column, Integer, Float, ForeignKey, DateTime
from base import Base

class Store(Base):
    __tablename__='stores'
    id=Column(Integer, primary_key=True, autoincrement=True, unique=True, comment='ID магазина')
    address=Column(String(255), unique=True, comment='Адрес магазина')

class Item(Base):
    __tablename__='items'
    id=Column(Integer, primary_key=True, autoincrement=True, unique=True, comment='ID товара')
    name=Column(String(255), unique=False, comment='Название товара')
    price=Column(Float, comment='Цена')

class Sale(Base):
    __tablename__='sales'
    id=Column(Integer, primary_key=True, autoincrement=True, unique=True, comment='ID продажи')
    sale_time=Column(DateTime, comment='Время продажи')
    item_id=Column('item_id', ForeignKey('items.id'), comment='ID проданного товара')
    store_id=Column('store_id', ForeignKey('stores.id'), comment='ID магазина, где продали')
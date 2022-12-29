Решение ДЗ №1 по теме "Асинхронность". Отчет по продажам.
Инструмент: FastAPI + asyncio + sqlalchemy + postgresql

Инструкция по запуску:
1) Установить пакеты "pip install -r requirements.txt".
2) В Файле settings.py необходимо подставить свои данные по подключению к БД.
3) Запуск uvicorn main:app
4) Проверить работу (http://127.0.0.1:8000/docs):
    *GET /items/ (http://127.0.0.1:8000/docs#/default/get_items_items__get)
    *GET /stores/ (http://127.0.0.1:8000/docs#/default/get_store_stores__get)
    *POST /sales/ (http://127.0.0.1:8000/docs#/default/add_sale_sales__post)
    *GET /stores/top/ (http://127.0.0.1:8000/docs#/default/get_top_store_stores_top__get)
    *GET /items/top/ (http://127.0.0.1:8000/docs#/default/get_top_items_items_top__get)
    При желании можно добавить магизины, итемы:
    *POST /add/store/ (http://127.0.0.1:8000/docs#/default/add_store_add_store__post)
    *POST /add/item/ (http://127.0.0.1:8000/docs#/default/add_item_add_item__post)

Задание:
Реализуйте асинхронное веб приложение которое:
    обрабатывает GET-запрос на получение всех товарных позиций
    обрабатывает GET-запрос на получение всех магазинов
    обрабатывает POST-запрос с json-телом для сохранения данных о произведенной продаже (id товара + id магазина)
    обрабатывает GET-запрос на получение данных по топ 10 самых доходных магазинов за месяц (id + адрес + суммарная выручка)
    обрабатывает GET-запрос на получение данных по топ 10 самых продаваемых товаров (id + наименование + количество проданных товаров)
    никакие лишние эндпоинты реализовывать не требуется
напишите readme.md с кратким описанием эндпоинтов и инструкцией запуска
используйте requirements.txt для указания сторонних зависимостей и их версий
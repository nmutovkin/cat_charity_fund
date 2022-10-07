# QRKot

Сервис для пожертвований на благотворительность. В сервисе возможно создать благотворительные проекты и собирать на них пожертвования.

# Технологии

* Python
* FastAPI
* SQLAlchemy

## Запуск проекта

1. Клонируйте репозиторий ```git clone https://github.com/nmutovkin/cat_charity_fund.git```
2. В папке с репозиторием ```cd cat_charity_fund``` создайте виртуальное окружение ```python -m venv venv```
3. Активируйте окружение ```source venv/bin/activate```
4. Установите зависимости ```pip install -r requirements.txt```
5. Создайте файл для переменных окружения ```touch .env```
6. Задайте переменные окружения в .env (замените указанные значения на свои)

```
APP_TITLE=кошачий благотворительный фонд # название приложения
DESCRIPTION=описание # описание приложения
DATABASE_URI=dialect+driver://username:password@host:port/database # расположение файла базы данных
SECRET=secret_key # секретный ключ приложения
FIRST_SUPERUSER_EMAIL=admin@mail.ru # почтовый адрес первого суперюзера
FIRST_SUPERUSER_PASSWORD=password # пароль для уч. записи первого суперюзера
LOG_FILE_PATH=/home/user/log.txt # путь до файла с логами приложения
```

7. Иницируйте бд ```alembic init --template async alembic```
8. Выполните миграции ```alembic upgrade head```
9. Запустите проект ```uvicorn app.main:app --reload```

API сервиса доступно по адресу ```http://127.0.0.1:8000```
Документация в Swagger формате будет доступна по адресу ```http://127.0.0.1:8000/docs```.

# Примеры запросов

## Получение списка благотворительных проектов

**GET /charity_project/**

**RESPONSE**
```
[
  {
    "name": "string",
    "description": "string",
    "full_amount": 0,
    "id": 0,
    "invested_amount": 0,
    "fully_invested": true,
    "create_date": "2022-10-07T07:14:24.254Z",
    "close_date": "2022-10-07T07:14:24.254Z"
  }
]
```

## Получение списка пожертвований для текущего пользователя

**GET /donation/my**

**RESPONSE**
```
[
  {
    "full_amount": 0,
    "comment": "string",
    "id": 0,
    "create_date": "2022-10-07T07:16:46.541Z"
  }
]
```

# Автор

Никита Мутовкин

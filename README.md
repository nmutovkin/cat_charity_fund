# Кошачий благотворительный фонд

Сервис для поддержки котиков!

Сервис написан с использованием технологий Python 3.7 и FastAPI

## Запуск проекта

1. Клонируйте репозиторий git clone https://github.com/nmutovkin/cat_charity_fund.git
2. В папке с репозиторием (cd cat_charity_fund) создайте виртуальное окружение python -m venv venv
3. Активируйте окружение source venv/bin/activate
4. Установите зависимости pip install -r requirements.txt
5. Создайте файл для переменных окружения touch .env
6. Задаем переменные окружения в .env (замените указанные значения на свои)

APP_TITLE=кошачий благотворительный фонд # название приложения
DESCRIPTION=описание # описание приложения
DATABASE_URI=dialect+driver://username:password@host:port/database # расположение файла базы данных
SECRET=secret_key # секретный ключ приложения
FIRST_SUPERUSER_EMAIL=admin@mail.ru # почтовый адрес первого суперюзера
FIRST_SUPERUSER_PASSWORD=password # пароль для уч. записи первого суперюзера
LOG_FILE_PATH=/home/user/log.txt # путь до файла с логами приложения

7. Иницируем бд alembic init --template async alembic
8. Выполняем миграции alembic upgrade head
9. Запускаем проект uvicorn app.main:app --reload

Документация Swagger будет доступна по адресу http://127.0.0.1:8000/docs.

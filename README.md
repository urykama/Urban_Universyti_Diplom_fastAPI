# Blog fastAPI

### Краткое описание:
API для блога, в котором пользователи могут публиковать записи/сообщения и просматривать сообщению других пользователей. Реализованы механизм комментариев к записям, возможность подписки на публикации интересующий авторов, регистрация пользователей.
Для аутентификации используется JWT-токен.
В проекте использованы следующие инструменты:
_Python3, FastAPI, Pydantic, SQLAlchemy, Alembic, python-jose and bcrypt_

## Подготовка проекта
### Установить менеджер пакетов, создать и активировать виртуальное окружение, установить зависимости:
```sh
pip install --user pipenv
pipenv shell
pipenv sync
```

### Переименовать файл .env.example (/project_dir/blog/app/.env.example) в .env и указать в нем недостающую информацию:
Для генерации SECRET_KEY:
```sh
openssl rand -hex 32
```
Полученное значение копируем в .env

### Создать базу и применить миграции:
Из корневой директории проекта выполнить:
```sh
alembic upgrade head
```

### Запустить проект:
```sh
uvicorn blog.main:app
```

**Документация доступкна по url: http://127.0.0.1:8000/redoc/**

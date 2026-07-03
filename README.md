# Django Объявления

Простое приложение для размещения объявлений с двумя реализациями API:
- **Чистый Django** (без сторонних фреймворков) – `/api/v2/`
- **Django REST Framework** – `/api/v2/drf/`

## Стек технологий
- Python 3.14
- Django 6.0.6
- Django REST Framework (для второй версии API)
- SQLite (по умолчанию)
- Pillow (для работы с изображениями)

## Модели
- **User** – кастомная модель пользователя (добавлено поле `phone`).
- **Trade** – объявление (поля: `title`, `description`, `status`, `author`, `created_at`, `updated_at`).
- **TradeImage** – изображение (поля: `image`, `author`, `trade`, `created_at`, `updated_at`).

## API Эндпоинты

### Версия на чистом Django (`/api/v2/`)

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/v2/trades/` | Список открытых объявлений (id, title, created_at) |
| POST | `/api/v2/trades/` | Создание объявления (требуется авторизация) |
| GET | `/api/v2/trades/<id>/` | Детали + ссылки на изображения |
| PUT | `/api/v2/trades/<id>/` | Обновление (title, description, status) |
| POST | `/api/v2/trades/<id>/images/` | Добавление изображения |
| DELETE | `/api/v2/trades/<id>/images/<image_id>/` | Удаление изображения |

### Версия на DRF (`/api/v2/drf/`)

Те же эндпоинты, но с использованием Django REST Framework:
- Автоматическая документация (Browsable API).
- Удобные формы для тестирования.
- Поддержка сериализации и валидации из коробки.

| Метод | URL |
|-------|-----|
| GET | `/api/v2/drf/trades/` |
| POST | `/api/v2/drf/trades/` |
| GET | `/api/v2/drf/trades/<id>/` |
| PUT | `/api/v2/drf/trades/<id>/` |
| POST | `/api/v2/drf/trades/<id>/images/` |
| DELETE | `/api/v2/drf/trades/<id>/images/<image_id>/` |

Все ответы – **JSON**. Ошибки валидации возвращают HTTP статус **400** с описанием.

## Дополнительные модули

### Асинхронный сервер для загрузки файлов (папка `t2/`)
- Реализован на `aiohttp`.
- Запуск: `python t2/main.py` (сервер слушает порт 8080).
- Эндпоинт: `POST /api/upload/` – принимает файл в теле запроса и возвращает JSON с его размером в байтах (файл не сохраняется на диск и не читается целиком в память).

## Установка и запуск

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Myers66/Django_clean.git
cd Django_clean

# 2. Создать виртуальное окружение и активировать его
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 3. Установить зависимости
pip install django pillow djangorestframework aiohttp

# 4. Применить миграции Django
python manage.py migrate

# 5. Создать суперпользователя
python manage.py createsuperuser

# 6. Запустить сервер разработки Django
python manage.py runserver

# 7. (для асинхронного сервера) запустить в другом терминале:
python t2/main.py

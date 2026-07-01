# Django Объявления (чистый Django API)

Простое приложение для размещения объявлений. Реализовано на чистом Django без использования Django REST Framework. API возвращает JSON, все эндпоинты соответствуют заданию.

## Стек технологий
- Python 3.14
- Django 6.0.6
- SQLite (по умолчанию)
- Pillow (для работы с изображениями)

## Модели
- **User** – кастомная модель пользователя (добавлено поле `phone`).
- **Trade** – объявление (поля: `title`, `description`, `status`, `author`, `created_at`, `updated_at`).
- **TradeImage** – изображение (поля: `image`, `author`, `trade`, `created_at`, `updated_at`).

## API Эндпоинты (версия v2)

| Метод | URL | Описание | Пример тела запроса |
|-------|-----|----------|----------------------|
| GET | `/api/v2/trades/` | Список открытых объявлений (поля: id, title, created_at) | – |
| POST | `/api/v2/trades/` | Создание объявления (требуется авторизация) | `{"title":"Продам слона","description":"Серый, 2 тонны","status":"open"}` |
| GET | `/api/v2/trades/<id>/` | Детали объявления + ссылки на изображения | – |
| PUT | `/api/v2/trades/<id>/` | Обновление объявления (title, description, status) | `{"title":"Новое название"}` (можно частично) |
| POST | `/api/v2/trades/<id>/images/` | Добавление изображения (multipart/form-data) | поле `image` – файл |
| DELETE | `/api/v2/trades/<id>/images/<image_id>/` | Удаление изображения | – |

Все ответы – **JSON**. Ошибки валидации возвращаются с HTTP статусом **400** и описанием в JSON.

## Установка и запуск

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Myers66/Django_clean.git
cd название_репозитория

# 2. Создать виртуальное окружение и активировать его
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 3. Установить зависимости
pip install django pillow

# 4. Применить миграции
python manage.py migrate

# 5. Создать суперпользователя (для доступа в админку и авторизации в API)
python manage.py createsuperuser

# 6. Запустить сервер разработки
python manage.py runserver

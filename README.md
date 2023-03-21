## Проект YaMDb

Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». В каждой категории есть произведения: книги, фильмы или музыка. Произведению может быть присвоен жанр. Новые жанры может создавать только администратор. Пользователи могут оставить к произведениям текстовые отзывы и поставить произведению оценку в диапазоне от одного до десяти. Из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. Присутствует возможность комментирования отзывов.

Функционал API:
1) Просмотр произведений (кино, музыка, книги), которые подразделяются по жанрам и категориям..
2) Возможность оставлять отзывы на произведения и ставить им оценки, на основе которых построена система рейтингов.
3) Комментирование оставленных отзывов.

## Стек технологий

[![Python](https://img.shields.io/badge/-Python-464641?-style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-464646?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Pytest](https://img.shields.io/badge/Pytest-464646?style=flat-square&logo=pytest)](https://docs.pytest.org/en/6.2.x/)
[![Postman](https://img.shields.io/badge/Postman-464646?style=flat-square&logo=postman)](https://www.postman.com/)

## Как запустить проект

Cоздать и активировать виртуальное окружение:

```
WIN: python -m venv venv
MAC: python3 -m venv venv
```

```
WIN: . venv/scripts/activate
MAC: source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py makemigrations users
python manage.py makemigrations titles
python manage.py migrate users
python manage.py migrate titles
python manage.py migrate

```
Загрузка тестовых данных из csv файлов

```
python manage.py loadcsv ./static/data/
```

Секретный ключ
Храним в файле .env и получаем с помощью команды

```
os.getenv('SECRET_KEY')
Ключ храним в виде  SECRET_KEY='секретный ключ'
```

И не забываем создать файл .env на уровне виртуального окружения
И прописать в нем: SECRET_KEY=<ваш код>
## Запуск тестов
Линтеры:

```
flake8 .
black .
```

Pytest:
```
pytest
```
## Просмотр API документации
```
python manage.py runserver
# open link:
http://127.0.0.1:8000/redoc/
```
## Примеры работы с API для всех пользователей

Подробная документация доступна по эндпоинту /redoc/

Для неавторизованных пользователей работа с API доступна в режиме чтения, что-либо изменить или создать не получится. 

```
Права доступа: Доступно без токена.
GET /api/v1/categories/ - Получение списка всех категорий
GET /api/v1/genres/ - Получение списка всех жанров
GET /api/v1/titles/ - Получение списка всех произведений
GET /api/v1/titles/{title_id}/reviews/ - Получение списка всех отзывов
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Получение списка всех комментариев к отзыву
Права доступа: Администратор
GET /api/v1/users/ - Получение списка всех пользователей
```
## Регистрация нового пользователя
Получить код подтверждения на переданный email.
Права доступа: Доступно без токена.
Использовать имя 'me' в качестве username запрещено.
Поля email и username должны быть уникальными.

Регистрация нового пользователя:

```
POST /api/v1/auth/signup/
```

```json
{
  "email": "string",
  "username": "string"
}

```

Получение JWT-токена:

```
POST /api/v1/auth/token/
```

```json
{
  "username": "string",
  "confirmation_code": "string"
}
```

## Примеры работы с API для авторизованных пользователей

Добавление категории:

```
Права доступа: Администратор.
POST /api/v1/categories/
```

```json
{
  "name": "string",
  "slug": "string"
}
```
### Авторы
- :white_check_mark: [s-kraynev (в роли Python-разработчика Тимлид - разработчик 1)](https://github.com/s-kraynev):
Разработка моделей "категории" (Categories),  "жанры" (Genres) и "произведения" (Titles), а также разработка представлений и эндпойнтов для них, скрипт по импорту CSV-файлов.

- :white_check_mark: [Dxbriy (в роли Python-разработчика - разработчик 2)](https://github.com/Dxbriy):
Работа всей части, касающуюся управления пользователями: системa регистрации и аутентификации, права доступа, работу с токеном, систему подтверждения через e-mail

- :white_check_mark: [VeraKupriyanova (в роли Python-разработчика - разработчик 3)](https://github.com/VeraKupriyanova):
Разработка моделей "отзывы" (Review) и "комментарии" (Comments), а также разработка представлений и эндпойнтов для них, а также рейтингом произведений

# Проект foodgram

## Описание проекта
Проект педставляет собой социальную сеть по обмену рецептами. Зарегистрированные пользователи могут добавлять рецепты в избранное, создавать свои рецепты с картинками, подписываться на других авторов, а также добавлять рецепты в список покупок с последующей генерацией списка в формате txt, где указано суммарное количество всех необходимых ингридентов. Список ингредиентов предоставлен в базе, при создании рецепта ингредиент можно выбрать из списка.

Страница проекта: http://foodgram-tmaria.hopto.org/ (не забудьте зарегистрироваться).
Документация по проекту: http://foodgram-tmaria.hopto.org/api/docs/.

## Технологии в проекте:
Python 3.7,
Django 3.2,
JSON,
React,
API,
Docker,
Gunicorn,
Nginx,
PostgreSQL,
JWT,
Postman

## Шаблон наполнения env-файла:
См. файл infra/.env.example

## Установка
1. Клонировать репозиторий и перейти в него в командной строке:
`git@github.com:mtedoradze/foodgram-project-react.git`
2. Cоздать и активировать виртуальное окружение:
`python3 -m venv env`
`source env/bin/activate`
3. Установить зависимости из файла requirements.txt:
`python3 -m pip install --upgrade pip`
`pip install -r requirements.txt`
4. Развернуть контейнеры в «фоновом режиме»:
`sudo docker-compose up -d`
5. Выполнить миграции в контейнере backend:
`sudo docker-compose exec backend python manage.py migrate`
6. Создать суперпользователя:
`sudo docker-compose exec backend python manage.py createsuperuser`
7. Собрать статику:
`sudo docker-compose exec backend python manage.py collectstatic --no-input`
8. Загрузить данные по ингредиентам и тэгам:
`sudo docker-compose exec backend python manage.py loadpredata`

# Продуктовый помощник
![Foodgram](https://github.com/Gilions/foodgram-project/actions/workflows/main.yml/badge.svg)

Сайт доступен по ссылке - http://84.252.142.98/

Данный проект был создан в рамках дипломного проекта, курсов Yandex Практикум, факультет
Python разработчик.

Стек технологий:
Python 3, Django 3.1.7,  REST API, PostgreSQL, Docker, NNGIX, Gunicorn

## Запуск проекта используя Docker compose:
____
MamOS/windows/Linux:

Потребуется Docker, Docker Compose, v 1.29 +

Для установки Docker используйте официальную документацию для своей OS
https://docs.docker.com/compose/install/

Для запуска проекта необходимо использовать файл docker-compose.yaml из
репозитария.

Используйте команду находясь в одной директории с файлом docker-compose.yaml:

`docker-compose up`

##  Установка
______

Для устновки проекта пребуется python3, venv, git

Используйте команду:

`sudo apt install python3-pip python3-venv git -y`

Клонируйте проект:

`git clone <ссылка на репозитарий>`

Перейдите в директорию проекта. Активируйте виртуальное окружение и
установите пакеты из requirements.txt

`python3 -m venv venv`

`source venv/bin/activate`

`python -m pip install -r requirements.txt `

Для запуска Django сервера используйте команду

`python manage.py runserver`

## Системные трубования
______

Для запуска проекта требуется: Python 3, Django 3.1.7, REST API

## Развитие проекта
______
В дальнейшем данный проект я планирую улучшить добавив функционал:
- Поиск рецептов
- Сортировка по рейтингу и популярности
- Планирую добавить комментарии к каждому рецепту
- В планах добавить возможность формировать корзину не авторизованным пользователям
- Расширить API (Создание, редактирование и удаление рецептов, подписка, а так же добавление в избранные)

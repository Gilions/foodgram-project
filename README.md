# Продуктовый помощник
<p align="center">
<img src="https://user-images.githubusercontent.com/68146917/118436907-4e77ab00-b6ea-11eb-98aa-12fc49ff60b9.png">
</p>

![Foodgram](https://github.com/Gilions/foodgram-project/actions/workflows/main.yml/badge.svg)

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

[Сайт доступен по ссылке.](http://84.252.142.98/)

## Техническое описание
___
**HTML**

Список шаблонов:
+ Главная страница проекта для неавторизованного пользователя.
+ Главная страница проекта для авторизованного пользователя.
+ Персональная страница пользователя (рецепты одного автора).
+ Страницы для регистрации/авторизации/сброса пароля/изменения пароля.
+ Страница рецепта для автора.
+ Страница рецепта для авторизованного читателя.
+ Страница рецепта для неавторизованного читателя.
+ Страница создания рецепта.
+ Страница редактирования/удаления рецепта.
+ Страница подписок.
+ Страница избранных рецептов.
+ Страница списка покупок.
+ Формы:
    + зарегистрироваться,
    + войти на сайт,
    + сбросить пароль,
    + изменить пароль.

**JavaScript**

JS отправляет запросы в таких случаях:
+ при добавлении рецепта в список избранного и удалении рецепта из списка;
+ при добавлении рецепта в список покупок и удалении рецепта из списка;
+ при подписке на автора и отмене подписки;
+ при вводе названия ингредиента в форме создания рецепта: на сервер отправляется введённый в поле фрагмент текста, возвращаются найденные совпадения, которые выводятся в подсказки. При выборе нужного ингредиента подставляются соответствующие единицы измерения: «Яйца — шт», «Молоко — мл», «Сахар — г»;
+ при изменении количества рецептов в «Списке покупок»: в запросе отправляется ID добавленного/удалённого рецепта, после успешного запроса в шапке сайта обновляется счётчик.

**Рецепт**

Рецепт описываться такими полями:
+ Автор публикации (пользователь).
+ Название.
+ Картинка.
+ Текстовое описание.
+ Ингредиенты:
    + продукты для приготовления блюда по рецепту. Множественное поле, выбор из предустановленного списка, с указанием количества и единицы измерения.
+ Тег (можно установить несколько тегов на один рецепт, выбор из предустановленных):
    + завтрак
    + обед
    + ужин
+ Время приготовления в минутах.
+ Slug (уникальная часть URL для рецепта)

Все поля обязательны для заполнения.

**Ингредиент**

Данные об ингредиентах хранятся в нескольких связанных таблицах. В результате на стороне пользователя ингредиент описываться такими полями:
+   Название
+ Количество
+ Единицы измерения

Все поля обязательны для заполнения.

**Главная страница**

Содержимое главной страницы — список рецептов, отсортированных по дате публикации (от новых к старым).

**Страница рецепта**

На странице — полное описание рецепта, возможность добавить рецепт в избранное и в список покупок, возможность подписаться на автора рецепта.

**Страница пользователя**

На странице — имя пользователя, все рецепты, опубликованные пользователем и возможность подписаться на пользователя.

**Подписка на авторов**

Подписка на публикации доступна только авторизованному пользователю. Страница подписок доступна только владельцу.

Сценарий поведения пользователя:
1. Пользователь переходит на страницу другого пользователя или на страницу рецепта и подписывается на публикации автора кликом по кнопке «Подписаться на автора».
2. Пользователь переходит на страницу «Мои подписки» и просматривает список рецептов, опубликованных теми авторами, на которых он подписался. Сортировка записей — по дате публикации (от новых к старым).
3. При необходимости пользователь может отказаться от подписки на автора: переходит на страницу автора или на страницу его рецепта и нажимает «Отписаться от автора».

**Список избранного**

Работа со списком избранного доступна только авторизованному пользователю. Список избранного может просматривать только его владелец.

Сценарий поведения пользователя:

1. Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в избранное».
2. Пользователь переходит на страницу «Список избранного» и просматривает персональный список избранных рецептов.
3. При необходимости пользователь может удалить рецепт из избранного.

**Список покупок**

Работа со списком покупок доступна авторизованным пользователям. Список покупок может просматривать только его владелец.

Сценарий поведения пользователя:

1. Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в покупки».
2. Пользователь переходит на страницу Список покупок, там доступны все добавленные в список рецепты.
3. Пользователь нажимает кнопку Скачать список и получает файл с суммированным перечнем и количеством необходимых ингредиентов для всех рецептов, сохранённых в «Списке покупок».

При необходимости пользователь может удалить рецепт из списка покупок.

Список покупок скачивается в формате PDF.

При скачивании списка покупок ингредиенты в результирующем списке не дублироваться;
если в двух рецептах есть сахар (в одном рецепте 5 г, в другом — 10 г), то в списке  один пункт:

Сахар — 15 г.

В результате список покупок может выглядеть так:

+ Фарш (баранина и говядина) (г) — 600
+ Сыр плавленый (г) — 200
+ Лук репчатый (г) — 50
+ Картофель (г) — 1000
+ Молоко (мл) — 250
+ Яйцо куриное (шт) — 5
+ Соевый соус (ст. л.) — 8
+ Сахар (г) — 230
+ Растительное масло рафинированное (ст. л.) — 2
+ Соль (по вкусу) — 4
+ Перец черный (щепотка) — 3

**Фильтрация по тегам**

При нажатии на название тега выводится список рецептов, отмеченных этим тегом. Фильтрация может проводится по нескольким тегам в комбинации «или»: если выбраны несколько тегов — в результате должны быть показаны рецепты, которые отмечены хотя бы одним из этих тегов.

При фильтрации на странице пользователя должны фильтроваться только рецепты выбранного пользователя. Такой же принцип должен соблюдаться при фильтрации списка избранного.

**Регистрация и авторизация**

В проекте доступна система регистрации и авторизации пользователей.

Обязательные поля для пользователя:
+ Логин
+ Пароль
+ Email

Валидация email при регистрации.

**Уровни доступа пользователей:**

+ Гость (неавторизованный пользователь)
+ Авторизованный пользователь
+ Администратор

**Что могут делать неавторизованные пользователи**
+ Создать аккаунт.
+ Просматривать рецепты на главной.
+ Просматривать отдельные страницы рецептов.
+ Просматривать страницы пользователей.
+ Фильтровать рецепты по тегам.

**Что могут делать авторизованные пользователи**
+ Входить в систему под своим логином и паролем.
+ Выходить из системы (разлогиниваться).
+ Восстанавливать свой пароль.
+ Менять свой пароль.
+ Создавать/редактировать/удалять собственные рецепты
+ Просматривать рецепты на главной.
+ Просматривать страницы пользователей.
+ Просматривать отдельные страницы рецептов.
+ Фильтровать рецепты по тегам.
+ Работать с персональным списком избранного: добавлять/удалять чужие рецепты, просматривать свою страницу избранных рецептов.
+ Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл со количеством необходимых ингредиентов для рецептов из списка покупок.
+ Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.

**Что может делать администратор**

 Администратор обладает всеми правами авторизованного пользователя.
Плюс к этому он может:
+ изменять пароль любого пользователя,
+ создавать/блокировать/удалять аккаунты пользователей,
+ редактировать/удалять любые рецепты,
+ добавлять/удалять/редактировать ингредиенты.

**Настройки админки**
В интерфейс админ-зоны выведены необходимые поля моделей и настроены фильтры.

Модели:
+ Выведены все модели с возможностью редактирования и удаление записей.

Модель пользователей:

+ Добавлен фильтр списка по email и имени пользователя.

Модель рецептов:
+ В списке рецептов отображается название и автора рецепта.
+ Добавлен фильтр по автору, названию рецепта, тегам.
+ На странице рецепта отображается число добавлений этого рецепта в избранное.

Модель ингредиентов:
+ Отображается название ингредиента и единицы измерения.
+ Добавлен фильтр по названию.

**Инфраструктура**

Проект использует базу данных [PostgrSQL](https://www.postgresql.org/).

В корневой папке расположен файл requirements.txt со всеми зависимостями.

Проект запускается в трёх контейнерах (nginx, PostgreSQL и Django) через docker-compose на сервере в [Yandex.Cloud](https://cloud.yandex.ru/).
## Системные трубования
______


- [Python 3](https://www.python.org/)
- [Django 3.0.5](https://www.djangoproject.com/)
- [REST API Framework](https://www.django-rest-framework.org/)
- [DRF Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [NGINX](https://www.nginx.com/)
- [Gunicorn](https://gunicorn.org/)
- [Docker](https://www.docker.com/)
- [PostgrSQL](https://www.postgresql.org/)
- [Yandex.Cloud](https://cloud.yandex.ru/)

## Запуск проекта используя Docker compose:
____
MamOS/windows/Linux:

Потребуется Docker, Docker Compose, v 1.29 +

[Для установки Docker используйте официальную документацию для своей OS](https://docs.docker.com/compose/install/)


Для запуска проекта необходимо использовать файл docker-compose.yaml из
репозитария.

Предварительно в корневой папке создайте файл .env со следующем содержимым

```
SECRET_KEY='6m+%9$h)m7_s_m^=$q-1v@pbf25i4d1uonrzq=4rvhov%t%ozl1'

#Postgres setting
DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<Yours password>
DB_HOST=db
DB_PORT=5432
```

Используйте команду находясь в одной директории с файлом docker-compose.yaml:

`docker-compose up`

##  Установка
______

Для устновки проекта пребуется:
- [Python 3](https://www.python.org/)
- [PostgrSQL](https://www.postgresql.org/)
- [venv](https://docs.python.org/3/library/venv.html)
- [GitHub](https://github.com/git-guides/install-git)

Используйте команду:

`sudo apt install python3-pip python3-venv git -y`

Клонируйте проект:

`git clone https://github.com/Gilions/foodgram-project.git`

Перейдите в директорию проекта. Активируйте виртуальное окружение и
установите пакеты из requirements.txt
```
python3 -m venv venv

source venv/bin/activate

python -m pip install -r requirements.txt
```

В корневом каталоге созайде файл .env со следующем содержанием

```
SECRET_KEY='6m+%9$h)m7_s_m^=$q-1v@pbf25i4d1uonrzq=4rvhov%t%ozl1'

#Postgres setting
DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<Yours password>
DB_HOST=localhost
DB_PORT=5432
```

Установите базу данных PostgreSQL

[Download PostgreSQL](https://www.postgresql.org/download/)

Запустите базу данных, убедитесь в том, что локальный сервер запущен.
Это можно понять в приложении [pgAdmin4](https://www.pgadmin.org/download/)

![](https://user-images.githubusercontent.com/68146917/118441461-e6c55e00-b6f1-11eb-992e-60c48be9dc85.png)

Перед запуском проекта, необходимо выполнить миграции. В терминале из коневого каталога выполните:

`python3 manage.py migrate`

Для запуска Django сервера используйте команду

`python manage.py runserver`

## Развитие проекта
______
В дальнейшем данный проект я планирую улучшить добавив функционал:
- Поиск рецептов
- Сортировка по рейтингу и популярности
- Планирую добавить комментарии к каждому рецепту
- В планах добавить возможность формировать корзину не авторизованным пользователям
- Расширить API (Создание, редактирование и удаление рецептов, подписка, а так же добавление в избранные)

[![pipeline status](https://gitlab.crja72.ru/django/2024/spring/course/projects/team-8/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/spring/course/projects/team-8/-/pipelines)

# **Инструкция по запуску проекта**

1. Скачайте python 3.12.
2. Скачайте репозиторий.
3. Перейдите в папку с проектом. Команды указаны для Mac/Linux.
4. Создайте виртуальное окружение. Иногда бывает что просто `python` не работает, поэтому лучше поставить `python3`.
```bash
python3 -m venv venv
```
5. Активируйте виртуальное окружение.
```bash
source venv/bin/activate
```
6. На этом этапе вы должны установить зависимости. Существует два файла с зависимости, prod и dev. Просто скачайте один из файлов. Prod - для простого запуска, dev - для разработки.
```bash
pip install -r requirements/prod.txt
```
```bash
pip install -r requirements/dev.txt
```
7. В корневом каталоге создайте .env файл. Скопируйте содержимое файла .env.example в ваш .env.
```bash
cp .env.example .env
```
8. Откройте .env файл и добавьте значение SECRET_KEY и установите DEBUG в нужное положение (рекомендуется установить **DEBUG=True**, для этого установите **dev** зависимости).
9. Перейдите в папку lyceum, чтобы следующая команда выполнилась корректно.
```bash
cd event_manager
```
10.    Запустите сервер, выполнив команду:
```bash
python manage.py runserver
```
11.    Перейдите на адрес: http://127.0.0.1:8000/

# **База данных**
База данных находится в репозитории для учебных целей.
## Миграции
После того как внесли изменения в структуру моделей, выполните миграции.
1. Создайте миграцию.
```bash
cd event_manager
```
```bash
python manage.py makemigrations
```
2. Мигрируйте базу данный.
```bash
python manage.py migrate
```
## Фикстуры
**Пока их нет.**

~~Чтобы загрузить фикстуру выполните команду.
```bash
cd event_manager
python manage.py loaddata fixtures/data.json
```~~
## Создать пользователя с правами админа
1. Создайте админа. Введите логин, почту и пароль.
```bash
cd event_manager
```

```bash
python manage.py createsuperuser
```
## Использование админки
1. Перейдите на http://127.0.0.1:8000/admin/
2. Введите логин и пароль созданного ранее суперюзера.

# **Тестирование**

Тесты находятся в файлах, начинающихся на test. Чтобы запустить тесты:
1. Запустите тесты.
```bash
cd event_manager
python manage.py test
```

# Статика
Чтобы собрать всю статику выполните команду:
```bash
python manage.py collectstatic
```
Эту команду нужно выполнять перед запуском сервера. Это не обязательно, но может привести к некорректому отображению статики.

**Важно**: для корректного отображения статики поставьте DEBUG=True. Это временная мера, в скором времени будет устранена.

# **Доп информация**
## ER диаграмма

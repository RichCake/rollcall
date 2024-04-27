[![pipeline status](https://gitlab.crja72.ru/django/2024/spring/course/projects/team-8/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/spring/course/projects/team-8/-/pipelines)

# Менеджер мероприятий
RollCall — сайт для геймеров. Планируйте катки с дузьями легко и быстро!

# Инструкция по запуску проекта
## Настройка виртуального окружения

1. Скачайте python 3.12.
2. Скачайте репозиторий.
3. Перейдите в папку с проектом.

**Для Linux замените `python` на `python3`**

4. Создайте виртуальное окружение.
```bash
python -m venv venv
```
5. Активируйте виртуальное окружение.

Linux:
```bash
source venv/bin/activate
```
Windows:
```
venv\Scripts\activate
```
6. На этом этапе вы должны установить зависимости. Существует два файла с зависимости, prod и dev. Просто скачайте один из файлов. Prod - для простого запуска, dev - для разработки.
```bash
pip install -r requirements/prod.txt
```
```bash
pip install -r requirements/dev.txt
```
7. Скопируйте содержимое файла .env.example в .env.
```bash
cp .env.template .env
```
8. Откройте .env файл и добавьте значение SECRET_KEY и установите DEBUG в нужное положение (рекомендуется установить **DEBUG=True**, для этого установите **dev** зависимости).
   
## Настройка базы данных
9. Скачайте **PostgreSQL**, и перейдите в интерфейс командной строки.
10. Создайте юзера, если его нет.
```sql
CREATE USER test WITH PASSWORD 'test';
```
11. Создайте базу данных event_manager.
```sql
CREATE DATABASE event_manager OWNER test;
```
12. В файле .env укажите имя пользователя, пароль.

## Запуск сервера
1. **Команды `python manage.py ...` выполняются из каталога event_manager!**
```bash
cd event_manager
```
2. Выполните миграции
```bash
python manage.py migrate
```
3. Запустите сервер, выполнив команду:
```bash
python manage.py runserver
```
4.    Перейдите на адрес: http://127.0.0.1:8000/

## Запуск уведомлений
Чтобы получать уведомления выполните следующую команду:
```bash
python manage.py run_huey
```

## Фикстуры

Чтобы загрузить фикстуру выполните команду.
```bash
python manage.py loaddata fixtures/data.json
```
## Создать пользователя с правами админа
1. Создайте админа. Введите логин, почту и пароль.
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
python manage.py test
```

# Статика
Чтобы собрать всю статику выполните команду:
```bash
python manage.py collectstatic
```
Эту команду нужно выполнять перед запуском сервера. Это не обязательно, но может привести к некорректному отображению статики.

**Важно**: для корректного отображения статики поставьте DEBUG=True.

Проект заморожен/закончен в спешке, работодатель попросил как можно скорее заморозить работу (из-за войны), поэтому в проекте сейчас есть некоторые модули, которые пока не используются, и некоторые моменты могут быть неоттесчены. Плюс администрирование планировали делать из другого проекта (должна была быть синхронизация), но и тот проект пока заморожен


Для запуска требуется

Python 3.10
PostgreSQL 14
pipenv

Предварительно нужно сделать файл /server/env.py с используемыми переменными. Пример для dev окружения

```python
DEBUG = True

DB_NAME = '' # Название базы данных
DB_USER = '' # Имя пользователя базы данных
DB_PASSWORD = '' # Пароль пользователя

SERVER_DOMAINS = ['localhost', '127.0.0.1']
MEDIA_ROOT_URL = 'http://localhost:8000'
SERVER_URL = 'http://localhost:8000'

GOOGLEMAPS_KEY = '' # Для полноценной работы сервиса требуется указать ключ google maps


EMAIL = '' # Почта, с которой будут отправляться сообщения

EMAIL_HOST_USER = EMAIL
EMAIL_HOST_PASSWORD = '' # Пароль для почты
EMAIL_HOST = '' # SMTP сервер для отправки email
EMAIL_PORT = 1 # Порт для обращений
# EMAIL_USE_SSL = True # Указать, если используется ssl для email
EMAIL_USE_TLS = True # Указать, если используется tls для email
DEFAULT_FROM_EMAIL = EMAIL

SECRET_KEY = '' # Секретный ключ для django приложения (можно сгенерировать например на https://django-secret-key-generator.netlify.app/)

```

```bash

pipenv sync
pipenv run python ./manage.py makemigrations
pipenv run python ./manage.py migrate

```

После установки нужно создать superuser
```bash
pipenv run python ./manage.py createsuperuser
```

Теперь можно запускать приложение
```bash
pipenv run python ./manage.py runserver
```

Оно доступно по адресу (должен быть либо запущен в dev режиме фронтенд, либо сбилжен)
http://localhost:8000/

Сначала зайдите на http://localhost:8000/admin/ . Тут требуется создать новый элемент в настройках и указать нужные поля. Теперь всё готово

Для того, чтобы наполнить сайт контентом, добавьте несколько комплексов, а у них по паре планировок. Также желательно создать несколько подборок (они бывают 3 типов и отображаются по разному)

### Django-шаблон для бота адресов

##### Структура

- saldiframe - точка входа в Django-приложение

    - tgbots - работа с шаблонным Телеграм-ботом
    - db - папка с тестовой базой данных SQLite3
    - cache - папка для хранения файлов кэша, когда он включен 

- docs - папка со справкой, как и что делать с использованием Django


##### Установка Django:

1. Создаем виртуальное окружение.
2. Набираем `pip install django`.
3. Набираем `django-admin startproject saldiframe`.
3. Набираем `django-admin startapp tgbots`.
4. Запускаем сервер: `python manage.py runserver`.


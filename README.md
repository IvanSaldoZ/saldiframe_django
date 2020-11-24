### Django-шаблон для бота адресов

##### Структура

- saldiframe - точка входа в Django-приложение

    - tgbots - работа с шаблонным Телеграм-ботом
    - dinarapp - Тестовый проект на основе https://www.youtube.com/watch?v=YptkRsLNUi4
    - db - папка с тестовой базой данных SQLite3
    - cache - папка для хранения файлов кэша, когда он включен 

- docs - папка со справкой, как и что делать с использованием Django


##### Установка Django и создание шаблона первого приложения:

1. Создаем виртуальное окружение командой `python -m venv env` или через `pythonenv`
    1.a Активировать виртуальное окружение можно командой: `. env/bin/activate` или `source env/bin/activate`
2. Набираем `pip install django`.
3. Набираем `django-admin startproject saldiframe`.
3. Набираем `django-admin startapp dinarapp`, где dinarapp - это тестовое приложение
4. Запускаем сервер: `python manage.py runserver`.
5. Добавляем в settings.py в INSTALLED_APPS в конце наше новое приложение:
    `'dinarapp.apps.DinarappConfig',`
5. В `urls.py` добавляем url-ы:
    ```
        from django.urls import include
        ...
        urlpatterns = [
            path('', include('dinarapp.urls')),
        ]
    ```
6. Добавляем контроллер в `views.py`:
    ```
        # Create your views here.
        def home(request):
            return render(request, 'home.html')
    ``` 
7. Добавляем папку templates в папке dinarapp и создаем внутри этой папки наш вид "home.html":
8. Создаем файл `urls.py` в папке dinarapp:
    ```
    from django.urls import path
    from .views import home
    
    urlpatterns = [
        path('', home, name='home'),
    ]
    ``` 
   Где home - это имя функции из файла `views.py`
9. Для отображения ошибок на русском языке находим в файле `settings.py` переменную `LANGUAGE_CODE` и меняем ее на:
    `LANGUAGE_CODE = 'ru-ru'`.



### Работа с моделями пользователей

1. Набираем `python manage.py migrate` для применения миграция.
2. Создаем супер-пользователя `python manage.py createsuperuser`: `admin`/`123456`.
3. Переходим в `http://127.0.0.1:8000/admin/` и вводим данные нашего пользователя.


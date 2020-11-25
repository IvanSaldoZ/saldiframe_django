### Django-шаблон для бота адресов

##### Структура

- saldiframe - точка входа в Django-приложение

    - tgbots - работа с шаблонным Телеграм-ботом
    - dinarapp - Тестовый проект на основе https://www.youtube.com/watch?v=YptkRsLNUi4
    - dinarapp2 - Проект по управлению статьями в блоге, который можно брать за основу
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



### Создание Super-пользователя

1. Набираем `python manage.py migrate` для применения миграция.
2. Создаем супер-пользователя `python manage.py createsuperuser`: `admin`/`123456`.
3. Переходим в `http://127.0.0.1:8000/admin/` и вводим данные нашего пользователя.

### Создаем модели

1. В файле `models.py` пишем:
    ```
    from django.db import models
    
    # Create your models here.
    class Articles(models.Model):
        create_date = models.DateTimeField(auto_now=True)
        name = models.CharField(max_length=200)
        text = models.TextField()
    ```
2. Для отображения нашей модели в админ-панели добавляем ее в файл `admin.py`:
    ```
    from django.contrib import admin
    from .models import Articles
    
    # Register your models here.
    admin.site.register(Articles)
    ```
3. Для создания файла миграции нужно выполнить команду:
    `python manage.py makemigrations dinarapp2`
4. Для выполнения команд из файла миграций:
    `python manage.py migrate`
    


### Bootstrap

1. Переходим на getbootsrap.com > Documentation https://getbootstrap.com/docs/4.5/getting-started/introduction/ и копируем готовые стили:
    ```
    <!doctype html>
    <html lang="en">
      <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.3/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
    
        <title>Hello, world!</title>
      </head>
      <body>
        <h1>Hello, world!</h1>
    
        <!-- Optional JavaScript -->
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.3/js/bootstrap.min.js" integrity="sha384-w1Q4orYjBQndcko6MimVbzY0tgp4pWB4lZ7lr30WKz0vr/aWKhXdBNmNb5D92v7s" crossorigin="anonymous"></script>
      </body>
    </html>
    ```
   
2. Для меню можно выбрать шаблон из Navs:
    https://getbootstrap.com/docs/4.5/components/navs/
    
    ```
        <ul class="nav nav-pills">
          <li class="nav-item">
              {% url 'index' as url_home %}

            <a class="nav-link{% if request.path == url_home %} active{% endif %}" href="{{ url_home }}">Главная</a>
          </li>
          <li class="nav-item">
              {% url 'edit_page' as url_edit_page %}

            <a class="nav-link{% if request.path == url_edit_page %} active{% endif %}" href="{{ url_edit_page }}">Создание/ред/удаление</a>
          </li>
        </ul>
    ```
    
3. В index.html создаем общий контент:
    ```
        ...
            {% block content %}
                <h1 class="mt-4">Список статей</h1>
    
                {% for i in article_list %}
                    <ul class="list-group mt-4">
                        <li class="list-group-item">
                            <b>{{ i.create_date }}</b>
                            <span class="m-2">{{ i.name }}</span>
                            <span>{{ i.text | truncatechars:"5" }}</span>
    
                            <span class="float-right mr-3"><a href="detail/{{ i.id }}">Перейти к статье</a></span>
                        </li>
                    </ul>
                {% endfor %}
    
            {% endblock %}
        ...
    ```   
    А в других файлах делаем так, чтобы отобразить в них что-то (`detail.html`)
    ```
    {% extends 'index.html' %}

        {% block content %}
                <h1 class="mt-4">Статья: {{ get_article.name }}</h1>
                <p><a href="/">Вернуться на главную</a></p>
                <p>Дата создания: {{get_article.create_date}}</p>
                <p>Текст: {{ get_article.text }}</p>
        {% endblock %}
   ```
   
4. Таблицы можно взять с https://getbootstrap.com/docs/4.5/content/tables/

5. Модальное окно можно взять с https://getbootstrap.com/docs/4.5/components/modal/

   

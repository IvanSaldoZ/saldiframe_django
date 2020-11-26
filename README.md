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


### Регистрация и Авторизация пользователей

1. В forms.py:
    ```
    class AuthUserForm(AuthenticationForm, forms.ModelForm):
        class Meta:
            model = User
            fields = ('username', 'password')
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'
    
    
    class RegisterUserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ('username', 'password')
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'
        # Нужно переопределить метод save для пользователя, потому что по умолчанию нужно
        # хэшировать пароли, а не просто их туда строкой сохранять.
        # Этот метод основан на методе save класса UserCreationForm из django.contrib.auth.forms.py
        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password"])
            if commit:
                user.save()
            return user
    ```   


2. В views.py:
    ```
    from django.contrib.auth.views import LoginView, LogoutView
    from .forms import ArticleForm, AuthUserForm, RegisterUserForm
    from django.urls import reverse_lazy
    from django.contrib.auth.models import User
    
    class RegisterUserView(CreateView):
        """Регистрация пользователя"""
        model = User
        template_name = 'register_page.html'
        # Передаем форму
        form_class = RegisterUserForm
        # Что делать при успешном создании
        success_url = reverse_lazy('edit_page')
        success_msg = 'Пользователь успешно создан'
    
    
    class ProjectLoginView(LoginView):
        """Авторизация пользователя"""
        template_name = 'login.html'
        form_class = AuthUserForm
        success_url = reverse_lazy('edit_page')
        # Переопределяем перенаправлении при успешной авторизации
        def get_success_url(self):
            return self.success_url
    
    
    class ProjectLogout(LogoutView):
        """Выход пользователя из системы"""
        next_page = reverse_lazy('edit_page')
    
    ```

3. Проверка в шаблоне, авторизован ли пользователь: `{% if request.user.is_authenticated %}`


### База данных всех методов View из Django:

http://ccbv.co.uk/projects/Django/3.0/django.contrib.auth.views/LogoutView/


### При добавлении нового поля в базу данных:

1. Обязательно нужно сделать поле необязательным, чтобы применить миграции:
    ```
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец статьи',
                                   blank=True, null=True)
    ```

2. Выполнить команду `python manage.py makemigrations` для создания файла миграций из новых моделей
3. Выполнить команду `python manage.py migrate` для внесения изменений в базу данных


### Разграничение прав доступа

1. Примешиваем класс для авторизации в тот класс, который мы хотим закрыть

`from django.contrib.auth.mixins import LoginRequiredMixin`

и добавляем его в класс, который должен быть доступен только для авторизованных пользователей:

    ```
    class ArticleCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
        """Класс вида создания статьи"""
        model = Articles
        template_name = 'edit_page.html'
        form_class = ArticleForm
        ...
    ```

2. Для того, чтобы допускать до редактирования только того пользователя, который является автором,
переопределеяем метод get_form_kwargs класса ModelFormMixin из django.views.generic.edit:

    ```
    class ArticleUpdateView(LoginRequiredMixin, CustomSuccessMessageMixin, UpdateView):
        """Класс вида редактирования статьи"""

        ...

        def get_form_kwargs(self):
            """Переопределяем метод родительского класса при инициализации формы
            Return the keyword arguments for instantiating the form."""
            kwargs = super().get_form_kwargs()
            # Если Автор статьи != Текущий пользователь
            if kwargs['instance'].author != self.request.user:
                # То, отказываем в доступе
                return self.handle_no_permission()
            return kwargs
    ```

3. Для того, чтобы не допускать удаления переопределяем метод delete класса DeletionMixin в
модуле django.views.generic.edit:
```
    from django.http import HttpResponseRedirect
    
    class ArticleDeleteView(LoginRequiredMixin, DeleteView):
        """Класс для удаления статьи"""
        model = Articles
        template_name = 'edit_page.html'
        # Что делать при успешном создании
        success_url = reverse_lazy('edit_page')
        success_msg = 'Статья удалена'
    
        def delete(self, request, *args, **kwargs):
            """
            Переопределение метода удаления для разграничения прав доступа
            Call the delete() method on the fetched object and then redirect to the
            success URL.
            """
            self.object = self.get_object()
            # Если Автор статьи != Текущий пользователь
            if self.object.author != self.request.user:
                # То, отказываем в доступе
                return self.handle_no_permission()
            success_url = self.get_success_url()
            self.object.delete()
            return HttpResponseRedirect(success_url)
```

### Добавление комментариев:

1. Добавляем модели:
    ```
    class Comments(models.Model):
        """Модель комментариев"""
        article = models.ForeignKey(Articles, on_delete=models.CASCADE, verbose_name='Статья',
                                   blank=True, null=True, related_name='comments_articles')
        author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария',
                                   blank=True, null=True)
        create_date = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
        text = models.TextField(verbose_name='Текст комментария')
        status = models.BooleanField(verbose_name='Видимость комментария', default=False)
   
    ```

2. Добавляем формы:
    ```
    class CommentForm(forms.ModelForm):
        """Форма добавления комментария"""
        class Meta:
            model = Comments
            fields = ('text',)
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'
    ```
   
3. Расширяем контроллер просмотра статьи чере миксин добавления формы:
    ```
    from django.views.generic.edit import FormMixin
   
    class HomeDetailView(CustomSuccessMessageMixin, FormMixin, DetailView):
        """Контролер - одна статья"""
        model = Articles
        template_name = 'detail.html'
        context_object_name = 'get_article'
        form_class = CommentForm
        success_msg = 'Комментарий успешно создан, ожидайте модерации'
    
        def post(self, request, *args, **kwargs):
            """Переопределяем метод POST при публикации комментария
            с помощью формы"""
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
    
        def get_success_url(self, **kwargs):
            """При успешндом добавлении комментария перенаправить на страницу статьи"""
            return reverse_lazy('detail', kwargs={'pk': self.get_object().id})
    
        def form_valid(self, form):
            """Переопределяем метод, который вызывается при отправке формы
            Сохраняем комментарий, если форма валидна
            :param form:
            :return:
            """
            # Получаем данные для записи в БД,
            # но не сохраняем в БД пока что
            self.object = form.save(commit=False)
            # Получаем то, для какой статьи идет добавление комментария
            # self.get_object() - возвращает объект той статьи,
            # для которой применена вьюшка
            self.object.article = self.get_object()
            # Получаем то, какой пользователь отправл комментарий
            self.object.author = self.request.user
            # Сохраняем в базу данных
            self.object.save()
            return super().form_valid(form)
    ```

4. Добавляем вид в `detail.html`:
    ```
        <h4>Комментарии ({{get_article.comments_articles.all.count}})</h4>

          {% if messages %}
            <!-- Success alert after adding article -->
            <div class="alert alert-success mt-4" role="alert">
              {% for m in messages %}
                {{m}}
              {% endfor %}
            </div>
          {% endif %}

        <ul>
        {% for item in get_article.comments_articles.all %}
            <li>
                Дата создания: {{ item.create_date }}<br>
                Автор: {{ item.author }}<br>
                Статус комментария: {{ item.status }}<br><br>
                Текст: {{ item.text }}<br>
            </li>
        {% endfor %}
        </ul>
        <hr>

        <h5>Добавить комментарии</h5>

        <div class="col-4">
          <form action="" id="add_form" method="post">
            {% csrf_token %}
            {{form.as_p}}
          </form>
          <button form="add_form" type="submit" class="btn btn-primary">Добавить комментарий</button>
        </div>
    ```


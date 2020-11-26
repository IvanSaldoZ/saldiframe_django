from .models import Articles
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from .forms import ArticleForm, AuthUserForm, RegisterUserForm, CommentForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse


class CustomSuccessMessageMixin:
    """Миксин для отображения сообщения об успешности
    выполнения операции добавления/редактирования"""

    @property
    def success_msg(self):
        return False

    # Переопределяем метод, который вызывается при отправке формы
    # Выводим сообщение об успешности
    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    # Переопределяем метод класса Django для отображения URL
    # при перенаправлении на success_url
    # (при добавлении/редактировании статьи,
    # нужно для выделения последней добавленной статьи)
    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)


class HomeListView(ListView):
    """Можно так создавать контроллеры
    Контролер - список статей"""
    model = Articles
    template_name = 'index.html'
    context_object_name = 'article_list'


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

class ArticleCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
    """Класс вида создания статьи"""
    login_url = reverse_lazy('login_page')
    model = Articles
    template_name = 'edit_page.html'
    form_class = ArticleForm
    # Что делать при успешном создании
    success_url = reverse_lazy('edit_page')
    success_msg = 'Статья создана'

    def get_context_data(self, **kwargs):
        kwargs['list_articles'] = Articles.objects.all().order_by('-id')
        return super().get_context_data(**kwargs)

    # Переопределяем метод, который вызывается при отправке формы
    # Определяем пользователя, который добавил статью
    def form_valid(self, form):
        # Получаем данные для записи в БД,
        # но не сохраняем в БД пока что
        self.object = form.save(commit=False)
        # Обновляем автора, чтобы он был тем, кто делает отправку
        self.object.author = self.request.user
        # Сохраняем в базу данных
        self.object.save()
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, CustomSuccessMessageMixin, UpdateView):
    """Класс вида редактирования статьи"""
    login_url = reverse_lazy('login_page')
    model = Articles
    template_name = 'edit_page.html'
    form_class = ArticleForm
    # Что делать при успешном редактировании
    success_url = reverse_lazy('edit_page')
    success_msg = 'Статья успешно отредактирована'

    def get_context_data(self, **kwargs):
        """Переопределяем метод при обновлении контекста
        Insert the form into the context dict."""
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        """Переопределяем метод родительского класса при инициализации формы
        Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        # Если Автор статьи != Текущий пользователь
        if kwargs['instance'].author != self.request.user:
            # То, отказываем в доступе
            return self.handle_no_permission()
        return kwargs


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    """Класс для удаления статьи"""
    login_url = reverse_lazy('login_page')
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

    def post(self, request, *args, **kwargs):
        """Переопределяем метод для отрпавки сообщения об удалении статьи"""
        messages.success(self.request, self.success_msg)
        return super().post(request)


class RegisterUserView(CreateView):
    """Регистрация пользователя"""
    model = User
    template_name = 'register_page.html'
    # Передаем форму
    form_class = RegisterUserForm
    # Что делать при успешном создании
    success_url = reverse_lazy('edit_page')
    success_msg = 'Вы успешно прошли регистрацию. Спасибо'

    # Переопределяем метод, который вызывается при отправке формы
    # Авторизуем пользователя сразу после регистрации
    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        # Авторизуем пользователя
        auth_user = authenticate(username=username, password=password)
        # и осуществляем вход
        login(self.request, auth_user)
        return form_valid


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
    next_page = reverse_lazy('index')
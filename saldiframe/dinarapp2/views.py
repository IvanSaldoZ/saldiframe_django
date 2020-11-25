from .models import Articles
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ArticleForm, AuthUserForm, RegisterUserForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


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


class HomeDetailView(DetailView):
    """Контролер - одна статья"""
    model = Articles
    template_name = 'detail.html'
    context_object_name = 'get_article'


class ArticleCreateView(CustomSuccessMessageMixin, CreateView):
    """Класс вида создания статьи"""
    model = Articles
    template_name = 'edit_page.html'
    form_class = ArticleForm
    # Что делать при успешном создании
    success_url = reverse_lazy('edit_page')
    success_msg = 'Статья создана'
    def get_context_data(self, **kwargs):
        kwargs['list_articles'] = Articles.objects.all().order_by('-id')
        return super().get_context_data(**kwargs)


class ArticleUpdateView(CustomSuccessMessageMixin, UpdateView):
    """Класс вида редактирования статьи"""
    model = Articles
    template_name = 'edit_page.html'
    form_class = ArticleForm
    # Что делать при успешном создании
    success_url = reverse_lazy('edit_page')
    success_msg = 'Статья успешно отредактирована'
    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)


class ArticleDeleteView(DeleteView):
    """Класс для удаления статьи"""
    model = Articles
    template_name = 'edit_page.html'
    # Что делать при успешном создании
    success_url = reverse_lazy('edit_page')
    success_msg = 'Статья удалена'
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
    next_page = reverse_lazy('edit_page')
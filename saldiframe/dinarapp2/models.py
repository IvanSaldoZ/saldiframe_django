from django.db import models
from django.contrib.auth.models import User
from .middleware import get_current_user
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser

class Articles(models.Model):
    """Модель статей"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец статьи',
                               blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, verbose_name='Название')
    text = models.TextField(verbose_name='Текст статьи')

    def __str__(self):
        return "%s: %s-%s" % (self.create_date, self.name, self.text)

    class Meta:
        verbose_name = 'Статью'
        verbose_name_plural = 'Статьи'


class StatusFilterComments(models.Manager):
    """Класс для отображения только тех комментариев,
     который имеют статус True"""

    def get_queryset(self):
        """Переопределяем метод получения данных"""
        # Получаем текущего пользователя через Middleware
        user = get_current_user()
        # Если юзер не залогинен, то переназначаем пользователя на None:
        if user == AnonymousUser():
            user = None
        # Используем фильтр и метод Q из django.db.model для того, чтобы составить сложные запросы
        # Здесь например мы видим только:
        #   - комментарии, которые имеют статус False и при этом оставлены мной
        #   - комментарии, которые имеют статус False и при этом Я являюсь автором статьи
        #   - комментарии, которые имеют статус True
        # Вертикальная черта | означает условие ИЛИ
        return super().get_queryset().filter(Q(status=True)
                                             | Q(status=False, author=user)
                                             | Q(status=False, article__author=user)
                                             )


class Comments(models.Model):
    """Модель комментариев"""
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, verbose_name='Статья',
                               blank=True, null=True, related_name='comments_articles')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария',
                               blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    text = models.TextField(verbose_name='Текст комментария')
    status = models.BooleanField(verbose_name='Видимость комментария', default=False)
    # Переопределение объектов - комментариев. Отображаем только те, которые имеют статус True
    objects = StatusFilterComments()


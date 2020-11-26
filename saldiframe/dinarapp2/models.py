from django.db import models
from django.contrib.auth.models import User


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


class Comments(models.Model):
    """Модель комментариев"""
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, verbose_name='Статья',
                               blank=True, null=True, related_name='comments_articles')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария',
                               blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    text = models.TextField(verbose_name='Текст комментария')
    status = models.BooleanField(verbose_name='Видимость комментария', default=False)


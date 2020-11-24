from django.shortcuts import render
from .models import Articles
from django.views.generic import ListView, DetailView

# def home(request):
#     """Страница вывода статей"""
#     article_list = Articles.objects.all()
#     template = 'index.html'
#     context = {
#         'article_list': article_list
#     }
#     return render(request, template_name=template, context=context)

# def detail_page(request, id):
#     """Страница статьи"""
#     get_article = Articles.objects.get(id=id)
#     template = 'detail.html'
#     context = {
#         'get_article': get_article
#     }
#     return render(request, template_name=template, context=context)

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




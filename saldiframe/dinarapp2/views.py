from django.shortcuts import render, redirect
from .models import Articles
from django.views.generic import ListView, DetailView
from .forms import ArticleForm
from django.urls import reverse
from django.views.decorators.cache import cache_control
from django.core.cache import cache

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

@cache_control(must_revalidate=True, no_cache=True)
def edit_page(request):
    """Добавление статей"""
    success = False
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            success = True

    template = 'edit_page.html'
    context = {
        'list_articles': Articles.objects.all().order_by('-id'),
        'form': ArticleForm(),
        'success': success,
    }
    return render(request, template, context)

#@cache_control(must_revalidate=True, no_cache=True)
def update_page(request, pk):
    """Редактирование статьи"""
    get_article = Articles.objects.get(pk=pk)
    success_update = False
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance = get_article)
        if form.is_valid():
            form.save()
            success_update = True
    template = 'edit_page.html'
    context = {
        'get_article': get_article,
        'update': True,
        'form': ArticleForm(instance=get_article),
        'success_update': success_update,
    }
    # cache.clear()
    return render(request, template, context)


#@cache_control(must_revalidate=True, no_cache=True)
def delete_page(request, pk):
    """Удаление статьи"""
    get_article = Articles.objects.get(pk=pk)
    get_article.delete()
    #cache.clear()
    return redirect(reverse('edit_page'))

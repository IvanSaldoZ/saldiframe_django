from django.urls import path
from . import views

urlpatterns = [
    path('', views.addresses, name='addresses'),
    path('categories', views.categories, name='categories'),
]

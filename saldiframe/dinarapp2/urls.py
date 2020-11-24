from django.urls import path
from .views import HomeListView, HomeDetailView
#from .views import home, detail_page

urlpatterns = [
    #path('', home, name='index'),
    #path('detail/<int:id>', detail_page, name='detail'),
    path('', HomeListView.as_view(), name='index'),
    path('detail/<int:pk>', HomeDetailView.as_view(), name='detail'),


]
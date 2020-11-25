from django.urls import path
from .views import HomeListView, HomeDetailView, edit_page, update_page, delete_page
#from .views import home, detail_page

urlpatterns = [
    #path('', home, name='index'),
    #path('detail/<int:id>', detail_page, name='detail'),
    path('', HomeListView.as_view(), name='index'),
    path('detail/<int:pk>', HomeDetailView.as_view(), name='detail'),
    path('edit-page', edit_page, name='edit_page'),
    path('update-page/<int:pk>', update_page, name='update_page'),
    path('delete-page/<int:pk>', delete_page, name='delete_page'),

]
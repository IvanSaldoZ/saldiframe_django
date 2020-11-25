from django.urls import path
from .views import HomeListView, HomeDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView


urlpatterns = [
    path('', HomeListView.as_view(), name='index'),
    path('detail/<int:pk>', HomeDetailView.as_view(), name='detail'),
    path('edit-page', ArticleCreateView.as_view(), name='edit_page'),
    path('update-page/<int:pk>', ArticleUpdateView.as_view(), name='update_page'),
    path('delete-page/<int:pk>', ArticleDeleteView.as_view(), name='delete_page'),

]
from django.urls import path
from .views import HomeListView, HomeDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView, \
    ProjectLoginView, RegisterUserView, ProjectLogout, update_comment_status


urlpatterns = [
    path('', HomeListView.as_view(), name='index'),
    path('detail/<int:pk>', HomeDetailView.as_view(), name='detail'),
    path('edit-page', ArticleCreateView.as_view(), name='edit_page'),
    path('update-page/<int:pk>', ArticleUpdateView.as_view(), name='update_page'),
    path('delete-page/<int:pk>', ArticleDeleteView.as_view(), name='delete_page'),
    path('login', ProjectLoginView.as_view(), name='login_page'),
    path('register', RegisterUserView.as_view(), name='register_page'),
    path('logout', ProjectLogout.as_view(), name='logout_page'),

    # ajax
    path('update_comment_status/<int:pk>/<slug:type>', update_comment_status, name='update_comment_status'),

]
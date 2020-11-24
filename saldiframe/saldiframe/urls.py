from django.contrib import admin
from django.urls import path, include
from .settings import DEBUG

urlpatterns = [
    #path('', include('tgbots.urls')),
    path('dinarapp1', include('dinarapp.urls')),
    path('', include('dinarapp2.urls')),
]

if DEBUG:
    urlpatterns.append(path('admin/', admin.site.urls),)


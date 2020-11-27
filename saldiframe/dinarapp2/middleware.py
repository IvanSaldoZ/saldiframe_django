# Наши Middleware
from django.utils.deprecation import MiddlewareMixin

import threading

# Хранилище для данных о запросе
_local_storage = threading.local()

class CurrentRequestMiddlewareUser(MiddlewareMixin):
    """Middleware для отображения данных по пользователю"""

    def process_request(self, request):
        """При посылке запроса - обрабатываем его путем """
        _local_storage.request = request


def get_current_request():
    """Получаем текущее хранилище"""
    return getattr(_local_storage, 'request', None)

def get_current_user():
    request = get_current_request()
    if request is None:
        return None
    # Вернем атрибут, а если нет ничего, то вернем None
    return getattr(request, 'user', None)




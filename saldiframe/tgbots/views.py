from django.shortcuts import render


def addresses(request):
    # Отображаем адреса
    return render(request, 'tgbots/addresses.html')


def categories(request):
    # Отображаем категории
    return render(request, 'tgbots/categories.html')
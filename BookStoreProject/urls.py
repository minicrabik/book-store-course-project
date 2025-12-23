"""
URL configuration for BookStoreProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Стандартная админка
    path('admin/', admin.site.urls),
    
    # Подключаем каталог (главная страница и книги)
    path('', include('catalog.urls')),
    
    # Подключаем продажи (логин, регистрация, профиль, корзина)
    # Оставляем только одну строку для sales!
    path('', include('sales.urls')), 
]
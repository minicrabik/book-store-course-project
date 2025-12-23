from . import views # Здесь это правильно, так как файл views.py лежит рядом
from django.urls import path

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
]
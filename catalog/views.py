from django.shortcuts import render
from .models import Book, BookAuthor

def index(request):
    # Получаем книги и сразу подтягиваем связанные данные для скорости
    books = Book.objects.all().select_related('publisher')
    
    # Для каждой книги найдем ее авторов
    for book in books:
        # Получаем список имен авторов через связующую таблицу
        authors = BookAuthor.objects.filter(book=book).select_related('author')
        book.author_list = ", ".join([f"{a.author.first_name} {a.author.last_name}" for a in authors])
    
    return render(request, 'catalog/index.html', {'books': books})
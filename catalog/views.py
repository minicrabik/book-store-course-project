from django.shortcuts import render, get_object_or_404
from .models import Book

def index(request):
    # Главная страница (Лендинг)
    featured_books = Book.objects.all()[:3]
    return render(request, 'catalog/index.html', {'featured_books': featured_books})

def book_list(request):
    # Страница каталога
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query).distinct()
    else:
        books = Book.objects.all()
    return render(request, 'catalog/book_list.html', {'books': books, 'query': query})

def book_detail(request, pk):
    # Детальная страница конкретной книги
    # pk — это primary key (ID книги)
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'catalog/book_detail.html', {'book': book})
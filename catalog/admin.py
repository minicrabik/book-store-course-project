from django.contrib import admin
from .models import Author, Genre, Section, Publisher, Book, BookAuthor, Supplier, Supply

# Создаем "вкладку" для авторов внутри страницы книги
class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1 # Количество пустых полей для новых авторов

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_authors', 'price', 'stock', 'publisher')
    search_fields = ('title',)
    # Добавляем выбор авторов прямо в карточку книги
    inlines = [BookAuthorInline]

    # Метод для отображения списка авторов в общей таблице
    def get_authors(self, obj):
        return ", ".join([f"{ba.author.last_name} {ba.author.first_name}" for ba in obj.bookauthor_set.all()])
    get_authors.short_description = 'Авторы'

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'birth_date')

# Регистрируем остальные модели, чтобы они были в админке
admin.site.register(Genre)
admin.site.register(Section)
admin.site.register(Publisher)
admin.site.register(Supplier)
admin.site.register(Supply)
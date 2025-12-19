from django.contrib import admin
from .models import Author, Genre, Publisher, Section, Book, BookAuthor, BookGenre, BookSection

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
    search_fields = ('last_name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher') 
    search_fields = ('title',)

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(BookAuthor)
admin.site.register(BookGenre)
admin.site.register(BookSection)
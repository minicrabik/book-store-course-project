import csv
import json
import io
from django.contrib import admin
from django.http import HttpResponse
from .models import Author, Genre, Section, Publisher, Book, BookAuthor, Supplier, Supply

# Библиотеки для сложных форматов 
try:
    import openpyxl
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.pagesizes import A4
except ImportError:
    pass

# --- ФУНКЦИИ ВЫГРУЗКИ (ACTIONS) ---

def export_as_json(modeladmin, request, queryset):
    """Экспорт в JSON"""
    response = HttpResponse(content_type="application/json")
    response['Content-Disposition'] = 'attachment; filename="books_export.json"'
    data = []
    for obj in queryset:
        data.append({
            "title": obj.title,
            "price": str(obj.price),
            "stock": obj.stock,
            "publisher": obj.publisher.name if obj.publisher else "Нет",
        })
    response.write(json.dumps(data, indent=4, ensure_ascii=False))
    return response
export_as_json.short_description = "Скачать выбранное в JSON"

def export_as_csv(modeladmin, request, queryset):
    """Экспорт в CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books_export.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Название', 'Цена', 'Остаток', 'Издательство'])
    for obj in queryset:
        writer.writerow([obj.title, obj.price, obj.stock, obj.publisher.name if obj.publisher else ''])
    return response
export_as_csv.short_description = "Скачать выбранное в CSV"

def export_as_xlsx(modeladmin, request, queryset):
    """Экспорт в Excel (XLSX)"""
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Книги"
    
    # Шапка
    columns = ['Название', 'Цена', 'Остаток', 'Издательство']
    ws.append(columns)
    
    # Данные
    for obj in queryset:
        ws.append([obj.title, float(obj.price), obj.stock, obj.publisher.name if obj.publisher else ''])
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="books_export.xlsx"'
    wb.save(response)
    return response
export_as_xlsx.short_description = "Скачать выбранное в Excel (XLSX)"

# --- НАСТРОЙКИ АДМИНКИ ---

class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_authors', 'price', 'stock', 'publisher')
    search_fields = ('title',)
    inlines = [BookAuthorInline]
    # Добавляем все действия в список
    actions = [export_as_json, export_as_csv, export_as_xlsx]

    def get_authors(self, obj):
        return ", ".join([f"{ba.author.last_name} {ba.author.first_name}" for ba in obj.bookauthor_set.all()])
    get_authors.short_description = 'Авторы'

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'birth_date')

@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('supply_date', 'book', 'supplier', 'quantity', 'purchase_price')

admin.site.register(Genre)
admin.site.register(Section)
admin.site.register(Publisher)
admin.site.register(Supplier)
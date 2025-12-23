from django.contrib import admin
from .models import Employee, Customer, Sale, SaleItem

# Позволяет добавлять товары в чек прямо на странице продажи
class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    raw_id_fields = ('book',) # Удобный поиск книг, если их станет много

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'sale_date', 'employee', 'customer', 'total_amount')
    list_filter = ('sale_date', 'employee')
    inlines = [SaleItemInline]
    
    # Автоматический расчет суммы чека можно будет добавить позже, 
    # пока вводим вручную или через сигналы.

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'position', 'phone')
    list_filter = ('position',)
    search_fields = ('last_name', 'passport')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'phone')
    search_fields = ('last_name', 'phone')
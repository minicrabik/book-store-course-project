from django.contrib import admin
from .models import Employee, Customer, Supplier, Sale, Receipt, SalePosition, ReceiptPosition

# Настройка отображения сотрудников
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'position', 'salary', 'phone')
    list_filter = ('position',)
    search_fields = ('last_name', 'passport')

# Настройка отображения покупателей
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'phone')
    search_fields = ('last_name', 'phone')

# Настройка отображения продаж
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'sale_date', 'employee', 'customer')
    list_filter = ('sale_date', 'employee')

# Настройка отображения поступлений
@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('id', 'receipt_date', 'supplier', 'publisher')
    list_filter = ('receipt_date',)

# Регистрация позиций (состав чеков и накладных)
@admin.register(SalePosition)
class SalePositionAdmin(admin.ModelAdmin):
    list_display = ('sale', 'book', 'quantity', 'price')

@admin.register(ReceiptPosition)
class ReceiptPositionAdmin(admin.ModelAdmin):
    list_display = ('receipt', 'book', 'quantity', 'purchase_price')

admin.site.register(Supplier)
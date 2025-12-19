from django.db import models 
from catalog.models import Book, Publisher 

# Сущности, связанные с персоналом и клиентами 

# Сотрудники магазина
class Employee(models.Model):
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Зарплата")
    experience = models.IntegerField(verbose_name="Стаж (лет)")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    position = models.CharField(max_length=50, verbose_name="Должность")
    passport = models.CharField(max_length=12, unique=True, verbose_name="Паспорт (серия и номер)")
    address = models.TextField(verbose_name="Адрес проживания")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f'{self.last_name} ({self.position})'

# Покупатели
class Customer(models.Model):
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

# Поставщики книг
class Supplier(models.Model):
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

# Основные операции (Продажи и Поступления)

#Информация о продаже. Связь с сотрудником и покупателем
class Sale(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, verbose_name="Сотрудник (Кассир)")
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name="Покупатель")
    sale_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время продажи")
    
    # M:N связь с Book через SalePosition
    books = models.ManyToManyField(Book, through='SalePosition', verbose_name="Проданные книги")

    class Meta:
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"

    def __str__(self):
        return f'Продажа №{self.id} от {self.sale_date.strftime("%Y-%m-%d")}'

# Информация о поступлении товаров. Связь с поставщиком и издательством
class Receipt(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, verbose_name="Поставщик")
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, verbose_name="Издательство")
    receipt_date = models.DateField(auto_now_add=True, verbose_name="Дата поступления")

    # M:N связь с Book через ReceiptPosition
    books = models.ManyToManyField(Book, through='ReceiptPosition', verbose_name="Поступившие книги")

    class Meta:
        verbose_name = "Поступление"
        verbose_name_plural = "Поступления"

    def __str__(self):
        return f'Поступление №{self.id} от {self.receipt_date}'

# Промежуточные M:N таблицы с дополнительными данными

# Позиции_Продажи: Что, сколько и по какой цене было продано в рамках одной продажи.
class SalePosition(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name="Продажа")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена продажи (за ед.)")
    quantity = models.IntegerField(verbose_name="Количество")

    class Meta:
        # Составной уникальный ключ
        unique_together = ('sale', 'book') 
        verbose_name = "Позиция Продажи"
        verbose_name_plural = "Позиции Продаж"
    
    def __str__(self):
        return f'{self.book.title} x{self.quantity}'

# Позиции_Поступления: Что, сколько и по какой закупочной цене поступило
class ReceiptPosition(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, verbose_name="Поступление")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Закупочная цена (за ед.)")
    quantity = models.IntegerField(verbose_name="Количество")

    class Meta:
        # Составной уникальный ключ
        unique_together = ('receipt', 'book')
        verbose_name = "Позиция Поступления"
        verbose_name_plural = "Позиции Поступлений"

    def __str__(self):
        return f'{self.book.title} x{self.quantity} (Закупка)'

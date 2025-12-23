from django.db import models
from django.contrib.auth.models import User
from catalog.models import Book
from django.db.models.signals import post_save
from django.dispatch import receiver

class Employee(models.Model):
    """Сотрудники книжного магазина"""
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")
    position = models.CharField(max_length=100, verbose_name="Должность")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Зарплата")
    experience = models.IntegerField(verbose_name="Стаж (полных лет)")
    phone = models.CharField(max_length=20, verbose_name="Контактный телефон")
    passport = models.CharField(max_length=50, verbose_name="Паспортные данные")
    address = models.TextField(verbose_name="Адрес проживания")

    def __str__(self):
        return f"{self.last_name} — {self.position}"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

class Customer(models.Model):
    """База покупателей (связана с пользователями сайта)"""
    # Связываем с системным пользователем для входа на сайт
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='customer_profile')
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

# Автоматическое создание профиля покупателя при регистрации нового пользователя
@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        # Пытаемся заполнить имя из данных User
        Customer.objects.create(
            user=instance, 
            first_name=instance.first_name or instance.username,
            last_name=instance.last_name or ""
        )

class Sale(models.Model):
    """Заголовок чека (общая информация о продаже)"""
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.PROTECT, 
        verbose_name="Продавец-консультант",
        null=True, blank=True # Разрешаем null для онлайн-продаж без участия сотрудника
    )
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Покупатель"
    )
    sale_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время транзакции")
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        verbose_name="Итоговая сумма чека"
    )

    def __str__(self):
        return f"Продажа №{self.id} от {self.sale_date.strftime('%d.%m.%Y %H:%M')}"

    class Meta:
        verbose_name = "Продажа (Чек)"
        verbose_name_plural = "Продажи (Чеки)"

class SaleItem(models.Model):
    """Позиции в чеке (конкретные книги в одной продаже)"""
    sale = models.ForeignKey(
        Sale, 
        on_delete=models.CASCADE, 
        related_name='items', 
        verbose_name="Номер чека"
    )
    book = models.ForeignKey(
        Book, 
        on_delete=models.PROTECT, 
        verbose_name="Проданная книга"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество (шт)")
    price_at_sale = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Цена за ед. на момент продажи"
    )

    def save(self, *args, **kwargs):
        # ГЛАВНАЯ ЛОГИКА: Списание со склада при сохранении позиции чека
        if not self.pk: # Только для новых записей
            if self.book.stock >= self.quantity:
                self.book.stock -= self.quantity
                self.book.save()
                
                # Авто-заполнение цены, если не указана
                if not self.price_at_sale:
                    self.price_at_sale = self.book.price
            else:
                raise ValueError(f"Недостаточно товара '{self.book.title}' (в наличии: {self.book.stock})")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.book.title} (x{self.quantity})"

    class Meta:
        verbose_name = "Позиция чека"
        verbose_name_plural = "Позиции чеков"
from django.db import models

class Author(models.Model):
    """Модель автора книги"""
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

class Genre(models.Model):
    """Жанры литературы"""
    name = models.CharField(max_length=100, verbose_name="Название жанра")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

class Section(models.Model):
    """Разделы магазина (например, Детская литература, Наука)"""
    name = models.CharField(max_length=100, verbose_name="Название раздела")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"

class Publisher(models.Model):
    """Издательства"""
    name = models.CharField(max_length=255, verbose_name="Название издательства")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Издательство"
        verbose_name_plural = "Издательства"

class Book(models.Model):
    """Основная модель книги"""
    title = models.CharField(max_length=255, verbose_name="Название книги")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    publish_year = models.IntegerField(verbose_name="Год издания")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена продажи")
    stock = models.PositiveIntegerField(default=0, verbose_name="Остаток на складе (шт)")
    
    # Внешние ключи
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, verbose_name="Издательство")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, verbose_name="Жанр")
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, verbose_name="Раздел")

    def __str__(self):
        return f"{self.title} — {self.stock} шт."

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

class BookAuthor(models.Model):
    """Связующая таблица для реализации связи Многие-ко-Многим между книгами и авторами"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")

    class Meta:
        verbose_name = "Автор книги"
        verbose_name_plural = "Авторы книг"
        unique_together = ('book', 'author')

class Supplier(models.Model):
    """Поставщики книг"""
    name = models.CharField(max_length=255, verbose_name="Наименование поставщика")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

class Supply(models.Model):
    """Журнал поступлений книг на склад"""
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name="Поставщик")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена закупки")
    supply_date = models.DateField(auto_now_add=True, verbose_name="Дата поступления")

    def __str__(self):
        return f"Поставка №{self.id} ({self.book.title})"

    class Meta:
        verbose_name = "Поступление"
        verbose_name_plural = "Поступления"
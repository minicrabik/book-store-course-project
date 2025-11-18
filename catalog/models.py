from django.db import models

# Базовые сущности Справочники

# Издательства. Связь 1:M с Книгами и Поступлениями.
class Publisher(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название издательства")

    class Meta:
        verbose_name = "Издательство"
        verbose_name_plural = "Издательства"

    def __str__(self):
        return self.name

# Авторы. Связь M:N с Книгами.
class Author(models.Model):
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")
    date_of_birth = models.DateField(verbose_name="Дата рождения")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

# Жанры. Связь M:N с Книгами.
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название жанра")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


# Разделы магазина. Связь M:N с Книгами.
class Section(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название раздела")

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"

    def __str__(self):
        return self.name


# Основная сущность

# Книги. Центральная сущность каталога.
class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название книги")
    description = models.TextField(blank=True, verbose_name="Описание")
    publication_year = models.IntegerField(verbose_name="Год издания")
    
    # 1:M связь с Издательством
    publisher = models.ForeignKey(
        Publisher, 
        on_delete=models.SET_NULL, # Если издательство удалено, поле обнулится, но книга останется
        null=True, 
        verbose_name="Издательство"
    )
    
    # M:N связи через ManyToManyField
    authors = models.ManyToManyField(Author, through='BookAuthor', verbose_name="Авторы")
    genres = models.ManyToManyField(Genre, through='BookGenre', verbose_name="Жанры")
    sections = models.ManyToManyField(Section, through='BookSection', verbose_name="Разделы")

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.title

# Промежуточные M:N таблицы 

# Связующая таблица для Книга <-> Автор
class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('book', 'author') # Книга-Автор - это составной PK из схемы

# Связующая таблица для Книга <-> Жанр.
class BookGenre(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('book', 'genre')

# Связующая таблица для Книга <-> Раздел.
class BookSection(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('book', 'section')

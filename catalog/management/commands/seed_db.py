import random
from django.core.management.base import BaseCommand
from catalog.models import Author, Genre, Section, Publisher, Book, BookAuthor, Supplier, Supply
from sales.models import Employee, Customer, Sale, SaleItem
from django.utils import timezone
from django.db import connection

class Command(BaseCommand):
    help = 'Наполняет базу данных начальными данными, предварительно очищая её'

    def handle(self, *args, **kwargs):
        self.stdout.write('Очистка старых данных...')
        
        # Список моделей для очистки
        models_to_clear = [SaleItem, Sale, BookAuthor, Book, Author, Employee, Customer]
        
        for model in models_to_clear:
            table_name = model._meta.db_table
            # Проверяем, существует ли таблица в базе данных перед удалением
            if table_name in connection.introspection.table_names():
                model.objects.all().delete()
            else:
                self.stdout.write(f'Пропуск очистки: таблица {table_name} еще не создана.')

        self.stdout.write('Начинаю чистое наполнение базы данных...')

        # 1. Жанры
        genres_names = ['Фэнтези', 'Классика', 'Программирование', 'История', 'Детектив']
        genres = [Genre.objects.get_or_create(name=name)[0] for name in genres_names]

        # 2. Разделы
        sections_names = ['Художественная литература', 'Техническая литература', 'Детям']
        sections = [Section.objects.get_or_create(name=name)[0] for name in sections_names]

        # 3. Издательства
        publishers_names = ['Эксмо', 'АСТ', 'Питер', 'МИФ', 'Альпина']
        publishers = [Publisher.objects.get_or_create(name=name)[0] for name in publishers_names]

        # 4. Авторы
        authors_data = [
            ('Джон', 'Толкин', 'Рональд'),
            ('Федор', 'Достоевский', 'Михайлович'),
            ('Мартин', 'Фаулер', None),
            ('Агата', 'Кристи', None),
            ('Роберт', 'Мартин', 'Сесил'),
        ]
        authors = [Author.objects.create(first_name=f, last_name=l, middle_name=m) for f, l, m in authors_data]

        # 5. Книги
        books_data = [
            ('Властелин колец', 1200.00, publishers[0], genres[0], sections[0]),
            ('Преступление и наказание', 600.00, publishers[1], genres[1], sections[0]),
            ('Чистая архитектура', 2500.00, publishers[2], genres[2], sections[1]),
            ('Убийство в Восточном экспрессе', 550.00, publishers[0], genres[4], sections[0]),
            ('Совершенный код', 3200.00, publishers[2], genres[2], sections[1]),
        ]
        
        books = []
        for title, price, pub, gen, sec in books_data:
            book = Book.objects.create(
                title=title, 
                price=price, 
                publisher=pub, 
                genre=gen, 
                section=sec,
                publish_year=random.randint(2010, 2024),
                stock=random.randint(10, 50)
            )
            books.append(book)
            BookAuthor.objects.create(book=book, author=random.choice(authors))

        # 6. Сотрудники
        employees_data = [
            ('Иван', 'Иванов', 'Старший менеджер', 75000, '4510 111222'),
            ('Анна', 'Петрова', 'Продавец-кассир', 45000, '4511 333444'),
            ('Сергей', 'Сидоров', 'Продавец-кассир', 45000, '4512 555666'),
        ]
        employees = []
        for f, l, pos, sal, pas in employees_data:
            emp = Employee.objects.create(
                first_name=f, last_name=l, position=pos, salary=sal, 
                passport=pas, experience=random.randint(1, 10), 
                phone='555-01', address='г. Москва, ул. Книжная'
            )
            employees.append(emp)

        # 7. Покупатели
        customers_data = [('Алексей', 'Волков', '89111'), ('Мария', 'Кузнецова', '89222')]
        customers = [Customer.objects.create(first_name=f, last_name=l, phone=p) for f, l, p in customers_data]

        # 8. Продажи
        for _ in range(10):
            sale = Sale.objects.create(
                employee=random.choice(employees),
                customer=random.choice(customers),
                total_amount=0
            )
            total = 0
            for _ in range(random.randint(1, 3)):
                book = random.choice(books)
                qty = random.randint(1, 2)
                SaleItem.objects.create(
                    sale=sale, book=book, quantity=qty, price_at_sale=book.price
                )
                total += book.price * qty
            sale.total_amount = total
            sale.save()

        self.stdout.write(self.style.SUCCESS('База данных очищена (где это было возможно) и наполнена заново!'))
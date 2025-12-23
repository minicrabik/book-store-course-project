from decimal import Decimal
from django.conf import settings
from catalog.models import Book

class Cart:
    def __init__(self, request):
        """Инициализация корзины из сессии"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, book, quantity=1, override_quantity=False):
        """Добавить книгу в корзину или обновить ее количество"""
        book_id = str(book.id)
        if book_id not in self.cart:
            self.cart[book_id] = {
                'quantity': 0,
                'price': str(book.price)
            }
        if override_quantity:
            self.cart[book_id]['quantity'] = quantity
        else:
            self.cart[book_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, book):
        """Удалить книгу из корзины"""
        book_id = str(book.id)
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def __iter__(self):
        """Перебор элементов в корзине и получение объектов книг из БД"""
        book_ids = self.cart.keys()
        books = Book.objects.filter(id__in=book_ids)
        cart = self.cart.copy()
        
        for book in books:
            cart[str(book.id)]['book'] = book

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_price(self):
        """Подсчет общей стоимости всех книг"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Очистка корзины"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
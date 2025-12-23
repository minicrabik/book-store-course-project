from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Customer, Sale, SaleItem
from catalog.models import Book
from .forms import CustomerSignupForm
from .cart import Cart 

# 1. Личный кабинет
@login_required
def profile_view(request):
    """Отображение профиля и истории заказов"""
    try:
        customer = request.user.customer_profile
    except Customer.DoesNotExist:
        customer = Customer.objects.create(
            user=request.user,
            first_name=request.user.first_name or request.user.username,
            last_name=request.user.last_name or ""
        )
    
    # Сортируем заказы: сначала новые
    sales = Sale.objects.filter(customer=customer).order_by('-sale_date')
    return render(request, 'sales/profile.html', {'customer': customer, 'sales': sales})

# 2. Редактирование профиля (отдельная страница)
@login_required
def edit_profile_view(request):
    """Страница изменения личных данных"""
    customer = request.user.customer_profile
    if request.method == 'POST':
        customer.first_name = request.POST.get('first_name')
        customer.last_name = request.POST.get('last_name')
        customer.phone = request.POST.get('phone')
        customer.save()
        
        # Синхронизируем с моделью User
        request.user.first_name = customer.first_name
        request.user.last_name = customer.last_name
        request.user.save()
        
        messages.success(request, "Данные успешно обновлены!")
        return redirect('sales:profile')
    
    return render(request, 'sales/edit_profile.html', {'customer': customer})

# 3. Регистрация
def signup_view(request):
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.first_name}!")
            return redirect('sales:profile')
    else:
        form = CustomerSignupForm()
    return render(request, 'sales/signup.html', {'form': form})

# 4. Выход
def logout_user(request):
    logout(request)
    return redirect('catalog:index')

# --- КОРЗИНА И ОФОРМЛЕНИЕ ЗАКАЗА ---

@require_POST
def cart_add(request, book_id):
    """Добавление товара в корзину"""
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.add(book=book, quantity=1)
    messages.success(request, f"Книга '{book.title}' добавлена в корзину.")
    return redirect('sales:cart_detail')

def cart_detail(request):
    """Просмотр содержимого корзины"""
    cart = Cart(request)
    return render(request, 'sales/cart_detail.html', {'cart': cart})

@login_required
def checkout(request):
    """Оформление заказа с промежуточным подтверждением данных"""
    cart = Cart(request)
    customer = request.user.customer_profile
    
    if not cart:
        messages.error(request, "Ваша корзина пуста.")
        return redirect('catalog:book_list')

    # Обработка нажатия кнопки "Подтвердить заказ" на странице checkout_confirm.html
    if request.method == 'POST':
        # Обновляем данные, если пользователь изменил их перед заказом
        customer.first_name = request.POST.get('first_name', customer.first_name)
        customer.last_name = request.POST.get('last_name', customer.last_name)
        customer.phone = request.POST.get('phone', customer.phone)
        customer.save()

        # Создаем запись о продаже (Sale)
        sale = Sale.objects.create(
            customer=customer,
            total_amount=cart.get_total_price()
        )
        
        # Переносим товары из корзины в SaleItem и уменьшаем остаток на складе
        for item in cart:
            book = item['book']
            quantity = item['quantity']
            
            # Создаем позицию чека
            SaleItem.objects.create(
                sale=sale,
                book=book,
                quantity=quantity,
                price_at_sale=item['price']
            )
            
            # Логика уменьшения склада (если реализована в модели Book)
            if hasattr(book, 'stock'):
                book.stock -= quantity
                book.save()
        
        # Очистка корзины
        cart.clear()
        
        # Отображаем страницу успеха (sales/success.html)
        return render(request, 'sales/success.html', {'sale': sale})

    # Если GET запрос — показываем форму подтверждения данных (checkout_confirm.html)
    return render(request, 'sales/checkout_confirm.html', {
        'cart': cart,
        'customer': customer
    })
    
@require_POST
def cart_remove(request, book_id):
    """Удаление товара из корзины"""
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    messages.success(request, f"Книга '{book.title}' удалена из корзины.")
    return redirect('sales:cart_detail')
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'sales'

urlpatterns = [
    # Кабинет и профиль
    path('profile/', views.profile_view, name='profile'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='sales/login.html'), name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Корзина
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:book_id>/', views.cart_add, name='cart_add'),
    
    # Оформление заказа (ИМЕННО ЭТОЙ СТРОКИ НЕ ХВАТАЛО)
    path('checkout/', views.checkout, name='checkout'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),

    path('cart/remove/<int:book_id>/', views.cart_remove, name='cart_remove'),
    
    path('checkout/', views.checkout, name='checkout'),
]
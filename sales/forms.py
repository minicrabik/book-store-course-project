from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class CustomerSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label="Имя", required=True)
    last_name = forms.CharField(max_length=100, label="Фамилия", required=True)
    phone = forms.CharField(max_length=20, label="Телефон", required=True)

    class Meta(UserCreationForm.Meta):
        # Добавляем стандартные поля и наши новые
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name')

    def save(self, commit=True):
        # Сначала сохраняем базового пользователя User
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Находим профиль Customer (созданный сигналом) и дополняем его данными
            customer = user.customer_profile
            customer.first_name = user.first_name
            customer.last_name = user.last_name
            customer.phone = self.cleaned_data['phone']
            customer.save()
            
        return user
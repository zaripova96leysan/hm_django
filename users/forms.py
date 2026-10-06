from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser



class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'avatar', 'phone', 'country')

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

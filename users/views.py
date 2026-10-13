from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm
from django.core.mail import send_mail



class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        send_mail(
            'Добро пожаловать!',
            f'Спасибо за регистрацию, {user.username}!',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

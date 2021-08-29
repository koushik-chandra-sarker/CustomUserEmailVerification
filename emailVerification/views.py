from django.contrib.auth import login,logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from customAccount.forms import UserRegistrationForm, UserLoginForm
# Create your views here.
from customAccount.models import EmailConfirmed

User = get_user_model()


def home(request):
    return render(request, 'home.html')


def login_attempt(request):
    _next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.cleaned_data.get('user')
            login(request, user)
            if _next:
                return redirect(_next)
            return redirect('home')
        return render(request, 'login.html', {'form': form})
    return render(request, 'login.html', {'form': form})


def logout_attempt(request):
    logout(request)
    return redirect('Login')


def register_attempt(request):
    form = UserRegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_active = False
            instance.save()
            user = EmailConfirmed.objects.get(user=instance)
            site = get_current_site(request)
            email_body = render_to_string(
                'verify_email.html',
                {
                    'first_name': instance.first_name,
                    'last_name': instance.last_name,
                    'email': instance.email,
                    'domain': site.domain,
                    'activation_key': user.activation_key
                }
            )
            send_mail(
                subject='Email Confirmation',
                message=email_body,
                from_email='koushiksarker3030@gmail.com',
                recipient_list=[instance.email],
                fail_silently=True
            )
            return render(request, 'confirmationPage.html')
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def email_confirmation_attempt(request, activation_key):
    user = get_object_or_404(EmailConfirmed, activation_key=activation_key)
    if user is not None:
        user.email_confirm = True
        user.save()
        instance = User.objects.get(email=user)
        instance.is_active = True
        instance.save()
        return render(request, 'register_complete.html')

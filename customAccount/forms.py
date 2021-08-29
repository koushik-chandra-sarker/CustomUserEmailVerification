from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1')
        pass2 = self.cleaned_data.get('password2')
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError("Password doesn't match")
        return pass2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'is_active', 'is_staff', 'is_admin')

    def clean_password(self):
        return self.initial['password']


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'email',
                'placeholder': 'Email Address'
            }
        )
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'email',
                'id': 'firstName',
                'type': 'text',
                'placeholder': 'First Name'
            }
        )
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'lastName',
                'type': 'text',
                'placeholder': 'Last Name'
            }
        )
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'password1',
                'type': 'password',
                'placeholder': 'Password'
            }
        )
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'password2',
                'type': 'password',
                'placeholder': 'Confirm Password'
            }
        )
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        error_massages = {
            'duplicate_email': 'Email already taken.'

        }
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            raise forms.ValidationError(
                error_massages['duplicate_email'],
                code='duplicate_email'
            )
        except ObjectDoesNotExist:
            return email


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'email',
                'placeholder': 'Email Address'
            }
        )
    )
    password = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'password',
                'type': 'password',
                'placeholder': 'Password'
            }
        )
    )

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = User.objects.filter(Q(email__iexact=email)).distinct()
        if not user.exists() and user.count != 1:
            raise forms.ValidationError('User dose not exist.')
        user = user.first()
        if not (user.check_password(password)):
            raise forms.ValidationError('Bad credentials')
        self.cleaned_data['user'] = user
        return super(UserLoginForm, self).clean(*args, **kwargs)

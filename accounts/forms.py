from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
            max_length=100,
            label='Username',
            widget=forms.TextInput(
                    attrs={
                        'class': 'my-input',
                        'placeholder': 'Enter username',
                    }
                )
        )

    email = forms.CharField(
            max_length=100,
            label='Email',
            widget=forms.TextInput(
                    attrs={
                        'class': 'my-input',
                        'placeholder': 'Enter email',
                    }
                )
        )

    password1 = forms.CharField(
            max_length=100,
            label='Password',
            widget=forms.PasswordInput(
                    attrs={
                        'class': 'my-input',
                        'placeholder': 'Enter password',
                    }
                )
        )

    password2 = forms.CharField(
    max_length=100,
    label='',
    widget=forms.PasswordInput(
            attrs={
                'class': 'my-input',
                'placeholder': 'Enter password one more time',
                }
            )
        )
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
            max_length=100,
            label='',
            widget=forms.TextInput(
                    attrs={
                        'class': 'my-input',
                        'placeholder': 'Enter username',
                    }
                )
        )
    password = forms.CharField(
            max_length=100,
            label='',
            widget=forms.PasswordInput(
                    attrs={
                        'class': 'my-input',
                        'placeholder': 'Enter password',
                    }
                )
        )
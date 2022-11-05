from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm
)
from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class UserRegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        username_field = self.fields['username']
        username_field.widget.attrs['class'] = 'form-control'
        username_field.widget.attrs['placeholder'] = "Username"

        password1_field = self.fields['password1']
        password1_field.widget.attrs['class'] = 'form-control'
        password1_field.widget.attrs['placeholder'] = "Password"

        password2_field = self.fields['password2']
        password2_field.widget.attrs['class'] = 'form-control'
        password2_field.widget.attrs['placeholder'] = "Confirm password"


class UserLoginForm(AuthenticationForm):

    def __init__(self, request = ..., *args, **kwargs) -> None:
        super().__init__(request, *args, **kwargs)
        username_field = self.fields['username']
        username_field.widget.attrs['class'] = 'form-control'
        username_field.widget.attrs['placeholder'] = "Username"

        password_field = self.fields['password']
        password_field.widget.attrs['class'] = 'form-control'
        password_field.widget.attrs['placeholder'] = "Password"
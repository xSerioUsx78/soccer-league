from urllib import request
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.utils.translation import gettext_lazy as _
from .forms import (
    UserRegisterForm
)
from .decorators import unauthenticated_user

# Create your views here.

@method_decorator([unauthenticated_user], 'dispatch')
class RegisterView(View):

    def get(self, *args, **kwargs):
        form = UserRegisterForm()
        ctx = {
            'form': form,
            'title': "Register"
        }
        return render(self.request, 'users/auth/register.html', ctx)

    def post(self, *args, **kwargs):
        form = UserRegisterForm(
            data=self.request.POST
        )
        if form.is_valid():
            form.save()
            return redirect('login')
            
        ctx = {
            'form': form,
            'title': "Register"
        }
        return render(self.request, 'users/auth/register.html', ctx)
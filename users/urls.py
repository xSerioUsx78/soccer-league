from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView
from .forms import UserLoginForm


urlpatterns = [
    # AUTH
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/auth/login.html',
                                                authentication_form=UserLoginForm, 
                                                redirect_authenticated_user=True),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(),
         name='logout'),
]

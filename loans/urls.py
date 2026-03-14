from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),
    path('', views.dashboard, name='dashboard'),
    path('apply/', views.apply_loan, name='apply_loan'),
    path('register/', views.register, name='register'),

    

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'auth'
urlpatterns = [
    path('register/', views.register_page, name="reg"),
    path('login/', views.login_page, name='login'),
    path('reset_password/', view=auth_views.PasswordResetView.as_view(template_name='authentication/password_reset.html'), name='reset_password'),
    path('logout/', views.logout_page, name='logout'),
    path('users/', views.UsersView.as_view(), name='users'),
    path('profile<int:pk>/', views.profile_page, name='profile'),
    path('profile<int:pk>/authentication/customer', views.customers_page, name='customers'),
]
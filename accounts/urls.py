from django.urls import path
from accounts.views.account import *
from accounts.views.applications import *

app_name = 'accounts'
urlpatterns = [
    path('accounts/login', custom_login, name="login"),
    path('accounts/register', register, name="register"),
    path('accounts/logout', custom_logout, name='logout'),
    path('account/<username>', get_account, name='get-account'),
]


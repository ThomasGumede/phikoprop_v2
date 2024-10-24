from django.urls import path
from accounts.views.account import *
from accounts.views.password import password_change

app_name = 'accounts'
urlpatterns = [
    path('accounts/login', custom_login, name="login"),
    path('accounts/register', register, name="register"),
    path('accounts/logout', custom_logout, name='logout'),
    path('dashboard/account/<username>', get_account, name='get-account'),
    path('dashboard/account/applications/<username>', user_applications, name='user-applications'),
    path('dashboard/account/update-profile/<username>', update_profile, name='update-profile'),
    path('dashboard/account/update-password/<username>', password_change, name='update-password'),
]


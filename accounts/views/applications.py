from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def create_application(request):
    return render(request, "accounts/applications/create-application.html")
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib import messages
from npi_home.forms import EmailForm
from npi_home.tasks import send_email_to_admin

from django.contrib.auth.decorators import login_required

from properties.models import Property

def npi_home(request):
    properties = Property.objects.all()
    return render(request, "npi_home/home/home.html", {"properties": properties})

def about_npi(request):
    return render(request, "npi_home/home/about.html")

def npi_locations(request):
    return render(request, "npi_home/home/location.html")

def comming_soon(request):
    return render(request, "npi_home/comming-soon.html")

def contact_npi(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            send_email_to_admin(form.cleaned_data["subject"], form.cleaned_data["message"], form.cleaned_data["from_email"], form.cleaned_data["name"])
            messages.success(request, "We have successfully receive your email, will be in touch soon")
            return redirect("npi_home:contact-npi")
        else:
            messages.error(request, "Something went wrong, please fix errors below")
            for err in form.errors:
                messages.error(request, f"{err}")
                return render(request, "npi_home/home/contact.html", {"form": form})
            
    form = EmailForm()
    return render(request, "npi_home/home/contact.html", {"form": form})

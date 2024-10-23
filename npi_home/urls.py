from django.urls import path
from npi_home.views import *

app_name = "npi_home"
urlpatterns = [
    path("", npi_home, name="npi-home"),
    path("about-us", about_npi, name="about-npi"),
    path("about-us/locations", npi_locations, name="npi-locations"),
    path("about-us/contact-us", contact_npi, name="contact-npi")
]

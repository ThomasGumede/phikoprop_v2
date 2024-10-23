from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from properties.models import Property

def get_property(request, property_slug):
    property = get_object_or_404(Property, slug=property_slug)
    return render(request, "properties/property.html", {"property": property})
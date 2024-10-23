from django.contrib import admin
from properties.models import Property, PropertyGallery, Application, PropertyAminities

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    pass

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass

@admin.register(PropertyGallery)
class PropertyGalleryAdmin(admin.ModelAdmin):
    pass

@admin.register(PropertyAminities)
class PropertyAminitiesAdmin(admin.ModelAdmin):
    pass
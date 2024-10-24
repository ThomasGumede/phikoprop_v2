import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from accounts.utils.choices import PROVINCES, TITLE_CHOICES, EmployementStatus, Gender, HomeLanguage, RelationShip, StatusChoices
from accounts.utils.file_handlers import handle_profile_upload
from accounts.utils.validators import verify_rsa_phone

PHONE_VALIDATOR = verify_rsa_phone()


class Account(AbstractUser):
    profile_image = models.ImageField(help_text=_("Upload profile image"), upload_to="profile/", null=True, blank=True)
    title = models.CharField(max_length=30, choices=TITLE_CHOICES)
    gender = models.CharField(max_length=30, choices=Gender.choices)
    prefered_name = models.CharField(max_length=300, blank=True, null=True)
    biography = models.TextField(blank=True)
    address = models.CharField(max_length=300, blank=True)
    phone = models.CharField(help_text=_("Enter cellphone number"), max_length=15, validators=[PHONE_VALIDATOR], unique=True, null=True, blank=True)

    def get_full_name(self):
        if self.title:
            return f"{self.title} {self.first_name[0]} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"



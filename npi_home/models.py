from django.db import models
from properties.models import AbstractCreate
from django.utils.translation import gettext as _

class ContactEmail(AbstractCreate):
    subject = models.CharField(max_length=70)
    from_email = models.EmailField()
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    message = models.TextField(max_length=500)
    task_id = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'
        ordering = ["created"]

    def __str__(self) -> str:
        return self.subject

    def save(self, *args, **kwargs):
        super(ContactEmail, self).save(*args, **kwargs)



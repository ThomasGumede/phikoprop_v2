from django import forms

from npi_home.models import ContactEmail

class EmailForm(forms.ModelForm):
    class Meta:
        model = ContactEmail
        fields = ('from_email', 'name', 'message', 'subject', "phone")

        widgets = {
            "from_email": forms.EmailInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:opacity-60 placeholder:text-sm placeholder:text-paragraph-color", "placeholder": "Enter email address"}),
            "subject": forms.TextInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:opacity-60 placeholder:text-sm placeholder:text-paragraph-color", "placeholder": "Email subject"}),
            "name": forms.TextInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:opacity-60 placeholder:text-sm placeholder:text-paragraph-color", "placeholder": "Enter your name"}),
            "phone": forms.TextInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:opacity-60 placeholder:text-sm placeholder:text-paragraph-color", "placeholder": "Your phone"}),
            "message": forms.Textarea(attrs={"class": "min-h-[150px] text-paragraph-color pl-5 pr-50px py-15px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:opacity-60 placeholder:text-sm placeholder:text-paragraph-color", "placeholder": "Enter message", "row": "6"}),
        }
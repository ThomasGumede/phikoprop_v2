from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm,  UserCreationForm)

class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "phone", "title", "gender", "biography", "profile_image", "email", "address")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field_value in self.initial.items():
            if field_value is None:
                self.initial[field_name] = ''

    def clean_email(self):
        email = self.cleaned_data["email"]

        if get_user_model().objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(f'This email: {email} is already in use.')
        
        return email
    
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm placeholder:text-opacity-60", 'placeholder': 'Email', 'id': 'id_username'}), label="Email*")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm placeholder:text-opacity-60", 'placeholder': 'Password', 'id': 'id_password'}))


class RegistrationForm(UserCreationForm):
    confirm_email = forms.EmailField(help_text="Confirm your email address", required=True, widget=forms.EmailInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm placeholder:text-opacity-60"}))

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username or Email', "class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm placeholder:text-opacity-60"}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email*', "class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm placeholder:text-opacity-60"}),
            'confirm_email': forms.EmailInput(attrs={'placeholder': 'Confrim Your Email*', "class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm placeholder:text-opacity-60"}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Full Name(s)*', "class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm placeholder:text-opacity-60"}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Surname*', "class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm placeholder:text-opacity-60"}),
            #'hobbies': forms.TextInput(attrs={'placeholder': 'Username or Email', "class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm placeholder:text-opacity-60"}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password*', "class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm placeholder:text-opacity-60"}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm password*', "class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm placeholder:text-opacity-60"}),
            
        }

    def clean_email(self):
        email = self.cleaned_data["email"]

        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(f'This email: {email} is already in use.')
        
        return email
    
    def clean(self):
        clean = super().clean()
        second_email = clean.get("confirm_email", None)
        mail = clean.get("email", None)

        if second_email and mail and mail != second_email:
            raise forms.ValidationError(f'This email: {mail} does not match with confirmation email.')
        
        

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        
        if commit:
            user.save()

        return user
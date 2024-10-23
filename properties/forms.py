from django import forms
from properties.models import *

class StudentDetailsForm(forms.ModelForm):
    class Meta:
        model = StudentDetails
        fields = ("title", "first_names", "last_name", "prefered_name", "id_number",
                  "phone", "email", "address_one", "address_two", "surbub", "city", "province", "zipcode",
                  "gender", "place_of_birth", "date_of_birth", "home_language", "biography", "school_name",
                  "year_of_enrollment", "grade"
                  )
        
        widgets = {            
            'first_names': forms.TextInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm", "placeholder": "*First Name(s)"}),
            'last_name': forms.TextInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm", "placeholder": "*Last Name"}),
            'prefered_name': forms.TextInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm", "placeholder": "Preferred name"}),
            'id_number': forms.NumberInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm", "placeholder": "*ID Number"}),
            'phone': forms.TextInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm", "placeholder": "*Phone Number"}),
            'email': forms.EmailInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm", "placeholder": "Email"}),
            'address_one': forms.TextInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm", "placeholder": "*Address One"}),
            'address_two': forms.TextInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm", "placeholder": "Preferred name"}),
            'prefered_name': forms.TextInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm", "placeholder": "Preferred name"}),
        }
        
class StudentMedicalDetailsForm(forms.ModelForm):
    class Meta:
        model = StudentMedicalDetails
        fields = ("family_doctor_name", "family_doctor_telephone", "medical_aid_name", "known_allergies", "known_disabilities_or_illnesses", "additional_health_information",
                  "emergency_contact_name", "emergency_contact_number", "emergency_contact_relationship", "medical_aid_plan")
        
class GuardianForm(forms.ModelForm):
    class Meta:
        model = Guardian
        fields = ("guardian_or_father_title", "guardian_or_father_initials", "guardian_or_father_first_names", "guardian_or_father_last_name", "guardian_or_father_prefered_name", "guardian_or_father_id_number", "guardian_or_father_work_tel",
                  "guardian_or_father_phone", "guardian_or_father_email", "guardian_or_father_address",
                  "guardian_or_father_relationship", "guardian_or_father_employment_status", "guardian_or_father_place_of_work")

class GuardianTwoForm(forms.ModelForm):
    class Meta:
        model = GuardianTwo
        fields = ("guardian_or_mother_title", "guardian_or_mother_initials", "guardian_or_mother_first_names", "guardian_or_mother_last_name", "guardian_or_mother_prefered_name", "guardian_or_mother_id_number", "guardian_or_mother_work_tel",
                  "guardian_or_mother_phone", "guardian_or_mother_email", "guardian_or_mother_address",
                  "guardian_or_mother_relationship", "guardian_or_mother_employment_status", "guardian_or_mother_place_of_work")

class AccountHandlerForm(forms.ModelForm):
    class Meta:
        model = AccountHandler
        fields = ("account_handler_title", "account_handler_initials", "account_handler_first_names", "account_handler_last_name", "account_handler_prefered_name", "account_handler_id_number", "account_handler_work_tel",
                  "account_handler_phone", "account_handler_email", "account_handler_address",
                  "account_handler_relationship", "account_handler_employment_status", "account_handler_place_of_work")
        
class ApplicationDocumentForm(forms.ModelForm):
    class Meta:
        model = ApplicationDocument
        fields = ("guardian_or_father_id_copy", "guardian_or_mother_id_copy", "student_id_copy", "proof_of_resident")

        widgets = {            
            'guardian_or_father_id_copy': forms.FileInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm", "placeholder": "*First Name(s)"}),
            'guardian_or_mother_id_copy': forms.FileInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm", "placeholder": "*Last Name"}),
            'student_id_copy': forms.FileInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm", "placeholder": "Preferred name"}),
            'proof_of_resident': forms.FileInput(attrs={"class": "text-paragraph-color pl-5 pr-50px outline-none border-2 border-border-color-9 focus:border focus:border-secondary-color h-65px block w-full rounded-none placeholder:text-paragraph-color placeholder:text-sm", "placeholder": "*Phone Number"}),
            }
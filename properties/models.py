import uuid
from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from accounts.models import Account
from django.utils.translation import gettext as _
from accounts.utils.choices import PROVINCES, TITLE_CHOICES, EmployementStatus, Gender, HomeLanguage, RelationShip, StatusChoices
from accounts.utils.validators import verify_rsa_phone
from django.template.defaultfilters import slugify

from properties.utils.file_handlers import handle_content_upload, handle_cover_upload


PHONE_VALIDATOR = verify_rsa_phone()

class AbstractCreate(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AbstractPerson(models.Model):
    title = models.CharField(max_length=30, choices=TITLE_CHOICES)
    initials = models.CharField(max_length=50, blank=True, null=True)
    first_names = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    prefered_name = models.CharField(max_length=300, blank=True, null=True)
    id_number = models.CharField(max_length=300, blank=True, null=True)

    address_one = models.CharField(max_length=300)
    address_two = models.CharField(max_length=300)
    surbub = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    province = models.CharField(max_length=300, choices=PROVINCES)
    country = models.CharField(max_length=300, default="South Africa")
    zipcode = models.BigIntegerField()
    address_id = models.CharField(max_length=300, null=True, blank=True)

    phone = models.CharField(max_length=15, validators=[PHONE_VALIDATOR])
    work_tel = models.CharField(max_length=15, validators=[PHONE_VALIDATOR], null=True, blank=True)
    email = models.EmailField()


    class Meta:
        abstract = True

class Property(AbstractCreate):
    ROOM_TYPES = (
        ("SHARING", "Sharing"),
        ("SINGLE", "Single"),
    )
    PROPERY_TYPES = (
        ("boys_hostel", "Boys Hostel"),
        ("girls_hostel", "Girls Hostel"),
        ("mixed_gender_hostel", "Mixed Gender Hostel"),
    )
    property_id = models.CharField(max_length=50, unique=True)
    cover_image = models.ImageField(upload_to=handle_cover_upload)
    title = models.CharField(max_length=350, unique=True)
    property_type = models.CharField(max_length=150, choices=PROPERY_TYPES, default=PROPERY_TYPES[0])
    slug = models.SlugField(max_length=350, unique=True)
    details = models.TextField(help_text=_("Enter additional details about this property"), null=True, blank=True)
    description = HTMLField()
    address_one = models.CharField(max_length=300, null=True, blank=True)
    address_two = models.CharField(max_length=300, null=True, blank=True)
    surbub = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=300, null=True, blank=True)
    province = models.CharField(max_length=300, choices=PROVINCES, null=True)
    country = models.CharField(max_length=300, default="South Africa")
    zipcode = models.BigIntegerField(null=True, blank=True)
    map_coordinates = models.CharField(max_length=300, null=True, blank=True)
    map_url = models.CharField(max_length=300, null=True, blank=True)
    number_of_rooms = models.IntegerField(default=0)
    room_type = models.CharField(max_length=150, choices=ROOM_TYPES)
    
    number_of_beds = models.IntegerField(default=0)
    number_of_baths = models.IntegerField(default=0)
    room_area = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=1000, decimal_places=2)
    property_video_link = models.URLField(null=True, blank=True)
    aminities = models.ManyToManyField('PropertyAminities', related_name="properties")

    def __str__(self):
        return self.title

    def get_full_address(self):
        return f"{self.address_one}, {self.surbub}, {self.city}, {self.province}, {self.zipcode}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Property, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

class PropertyAminities(AbstractCreate):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Property Aminity'
        verbose_name_plural = 'Property Aminities'

class PropertyGallery(AbstractCreate):
    property = models.ForeignKey(Property, related_name="property_contents", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=handle_content_upload)

    def __str__(self):
        return self.property.title + "Content"

    class Meta:
        verbose_name = 'Property Content'
        verbose_name_plural = 'Property Contents'

class Application(AbstractCreate):
    property = models.ForeignKey(Property, related_name="applications", on_delete=models.CASCADE)
    applicant = models.ForeignKey(Account, related_name="applications", on_delete=models.CASCADE)
    application_id = models.CharField(max_length=150, unique=True, db_index=True)
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.HOLD)
    is_submitted = models.BooleanField(default=False)
    rules_and_terms_accepted = models.BooleanField(default=False)

    def is_application_finished(self):
        application_medical = StudentMedicalDetails.objects.filter(application__id=self.id).first()
        stn_details = StudentDetails.objects.filter(application__id=self.id).first()
        stn_guardian_one = Guardian.objects.filter(guardian_or_father_application__id=self.id).first()
        stn_guardian_two = GuardianTwo.objects.filter(guardian_or_mother_application__id=self.id).first()
        account_handler = AccountHandler.objects.filter(account_handler_application__id=self.id).first()
        documents = ApplicationDocument.objects.filter(application__id=self.id).first()
        if stn_details and application_medical and stn_guardian_one and stn_guardian_two and account_handler and documents and self.rules_and_terms_accepted:
            return True
        else:
            return False

    def generate_application_id(self) -> str:
        order_id_start = f'NPI{timezone.now().year}{timezone.now().month}'
        queryset = Application.objects.filter(application_id__iexact=order_id_start).count()
        
        count = 1
        application_id = order_id_start
        while(queryset):
            application_id = f'NPI{timezone.now().year}{timezone.now().month}{count}'
            count += 1
            queryset = Application.objects.all().filter(application_id__iexact=application_id).count()

        return application_id
    
    def save(self, *args, **kwargs):
        self.application_id = self.generate_application_id()
        return super(Application, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.application_id
    
    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
    
class StudentDetails(AbstractCreate, AbstractPerson):
    application = models.OneToOneField(Application, related_name="student_details", on_delete=models.CASCADE)
    gender = models.CharField(max_length=30, choices=Gender.choices)
    place_of_birth = models.CharField(max_length=300, blank=True, null=True)
    date_of_birth = models.DateField()
    religion = models.CharField(max_length=300, blank=True, null=True)
    home_language = models.CharField(max_length=50, choices=HomeLanguage.choices)
    biography = models.TextField(blank=True)

    # School Details
    school_name = models.CharField(max_length=300, blank=True, null=True)
    year_of_enrollment = models.IntegerField(blank=True, null=True)
    grade = models.IntegerField(blank=True, null=True)

class StudentMedicalDetails(AbstractCreate):
    application = models.OneToOneField(Application, related_name="student_medical_details", on_delete=models.CASCADE)
    family_doctor_name = models.CharField(max_length=255, blank=True)
    family_doctor_telephone = models.CharField(max_length=20, blank=True)
    medical_aid_name = models.CharField(max_length=255, blank=True)
    medical_aid_plan = models.CharField(max_length=255, blank=True)
    known_allergies = models.TextField(blank=True)
    known_disabilities_or_illnesses = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_number = models.CharField(max_length=20)
    emergency_contact_relationship = models.CharField(max_length=50, choices=RelationShip.choices)
    additional_health_information = models.TextField(blank=True)

class Guardian(AbstractCreate):
    guardian_or_father_title = models.CharField(max_length=30, choices=TITLE_CHOICES)
    guardian_or_father_initials = models.CharField(max_length=50, blank=True, null=True)
    guardian_or_father_first_names = models.CharField(max_length=300)
    guardian_or_father_last_name = models.CharField(max_length=300)
    guardian_or_father_prefered_name = models.CharField(max_length=300, blank=True, null=True)
    guardian_or_father_id_number = models.CharField(max_length=300, blank=True, null=True)
    guardian_or_father_phone = models.CharField(max_length=15, validators=[PHONE_VALIDATOR])
    guardian_or_father_work_tel = models.CharField(max_length=15, validators=[PHONE_VALIDATOR], null=True, blank=True)
    guardian_or_father_email = models.EmailField()
    guardian_or_father_address = models.TextField()
    guardian_or_father_application = models.OneToOneField(Application, related_name="guardian_one", on_delete=models.CASCADE)
    guardian_or_father_relationship = models.CharField(max_length=100, choices=RelationShip.choices)
    guardian_or_father_employment_status = models.CharField(max_length=150, choices=EmployementStatus.choices)
    guardian_or_father_place_of_work = models.CharField(max_length=150, null=True, blank=True)

class GuardianTwo(AbstractCreate):
    guardian_or_mother_title = models.CharField(max_length=30, choices=TITLE_CHOICES)
    guardian_or_mother_initials = models.CharField(max_length=50, blank=True, null=True)
    guardian_or_mother_first_names = models.CharField(max_length=300)
    guardian_or_mother_last_name = models.CharField(max_length=300)
    guardian_or_mother_prefered_name = models.CharField(max_length=300, blank=True, null=True)
    guardian_or_mother_id_number = models.CharField(max_length=300, blank=True, null=True)
    guardian_or_mother_phone = models.CharField(max_length=15, validators=[PHONE_VALIDATOR])
    guardian_or_mother_work_tel = models.CharField(max_length=15, validators=[PHONE_VALIDATOR], null=True, blank=True)
    guardian_or_mother_email = models.EmailField()
    guardian_or_mother_address = models.TextField()
    guardian_or_mother_application = models.OneToOneField(Application, related_name="guardian_two", on_delete=models.CASCADE)
    guardian_or_mother_relationship = models.CharField(max_length=100, choices=RelationShip.choices)
    guardian_or_mother_employment_status = models.CharField(max_length=150, choices=EmployementStatus.choices)
    guardian_or_mother_place_of_work = models.CharField(max_length=150, null=True, blank=True)

class AccountHandler(AbstractCreate):
    account_handler_title = models.CharField(max_length=30, choices=TITLE_CHOICES)
    account_handler_initials = models.CharField(max_length=50, blank=True, null=True)
    account_handler_first_names = models.CharField(max_length=300)
    account_handler_last_name = models.CharField(max_length=300)
    account_handler_prefered_name = models.CharField(max_length=300, blank=True, null=True)
    account_handler_id_number = models.CharField(max_length=300, blank=True, null=True)
    account_handler_phone = models.CharField(max_length=15, validators=[PHONE_VALIDATOR])
    account_handler_work_tel = models.CharField(max_length=15, validators=[PHONE_VALIDATOR], null=True, blank=True)
    account_handler_email = models.EmailField()
    account_handler_address = models.TextField()
    account_handler_application = models.OneToOneField(Application, related_name="account_handler", on_delete=models.CASCADE)
    account_handler_relationship = models.CharField(max_length=100, choices=RelationShip.choices)
    account_handler_employment_status = models.CharField(max_length=150, choices=EmployementStatus.choices)
    account_handler_place_of_work = models.CharField(max_length=150, null=True, blank=True)

class ApplicationDocument(AbstractCreate):
    guardian_or_father_id_copy = models.FileField(upload_to="applications/documents/")
    guardian_or_mother_id_copy = models.FileField(upload_to="applications/documents/")
    student_id_copy = models.FileField(upload_to="applications/documents/")
    proof_of_resident = models.FileField(upload_to="applications/documents/")

    application = models.OneToOneField(Application, related_name="application_document", on_delete=models.CASCADE)



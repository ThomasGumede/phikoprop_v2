from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from properties.models import Application, GuardianTwo, Property, StudentDetails, StudentMedicalDetails, Guardian, AccountHandler, ApplicationDocument
from properties.forms import GuardianTwoForm, StudentDetailsForm, StudentMedicalDetailsForm, GuardianForm, AccountHandlerForm, ApplicationDocumentForm

def get_started_with_application(request):
    properties = Property.objects.all()
    if request.user.is_authenticated and request.user.applications.count() > 1:
        for application in request.user.applications.all():
            if not application.is_application_finished():
                messages.info(request, "You have unfinished application, Please complete it and start new application")
                return redirect("properties:apply-student-details-with-id", property_slug=application.property.slug, application_id=application.id)
    return render(request, "properties/apply/get-started-with-applcation.html", {"properties": properties})

@login_required
def application_student_details(request, property_slug, application_id=None):
    
    property = get_object_or_404(Property, slug=property_slug)
    student_details = None
    if application_id:
        application = get_object_or_404(Application, id = application_id)
        student_details = StudentDetails.objects.filter(application=application).first()
    
    form = StudentDetailsForm(instance=student_details)

    if request.method == "POST":

        form = StudentDetailsForm(instance=student_details, data=request.POST)
        if form.is_valid():
            application = Application.objects.create(applicant=request.user, property=property)
            stn_details = form.save(commit=False)
            stn_details.application = application
            stn_details.save()
            messages.success(request, "Student Details successfully Added")
            return redirect("properties:applicant-guardians", application_id=application.id)
        else:
            messages.error(request, "Something Went Wrong, Fix Errors Below")
    return render(request, "properties/apply/student-details.html", {"form": form})

@login_required
def applicant_guardians(request, application_id):
    # property = get_object_or_404(Property, slug=property_slug)
    application = get_object_or_404(Application, id=application_id, applicant=request.user)
    stn_guardian_one = Guardian.objects.filter(guardian_or_father_application=application).first()
    stn_guardian_two = GuardianTwo.objects.filter(guardian_or_mother_application=application).first()
    account_handler = AccountHandler.objects.filter(account_handler_application=application).first()
    
    form3 = GuardianTwoForm(instance=stn_guardian_one)
    form2 = GuardianForm(instance=stn_guardian_two)
    form = AccountHandlerForm(instance=account_handler)

    if request.method == "POST":
        form3 = GuardianTwoForm(instance=stn_guardian_one, data=request.POST)
        form2 = GuardianForm(instance=stn_guardian_two, data=request.POST)
        form = AccountHandlerForm(instance=account_handler, data=request.POST)

        if form.is_valid() and form2.is_valid() and form3.is_valid():
            guardian_1 = form.save(commit=False)
            guardian_2 = form2.save(commit=False)
            guardian_3 = form3.save(commit=False)

            guardian_1.account_handler_application = application
            guardian_2.guardian_or_father_application = application
            guardian_3.guardian_or_mother_application = application

            guardian_1.save()
            guardian_2.save()
            guardian_3.save()
            messages.success(request, "Student Relatives Information Added Successfully")
            return redirect("properties:applicant-medical-details", application_id=application.id)
        else:
            messages.success(request, "Student Relatives Information Not Added Successfully")
        
    return render(request, "properties/apply/student-guardian.html", {"form": form, "form2": form2, "form3": form3, "application": application})


@login_required
def applicant_medical_details(request, application_id):
    application = get_object_or_404(Application, id=application_id, applicant=request.user)
    stn_medical_details = StudentMedicalDetails.objects.filter(application=application).first()
    form = StudentMedicalDetailsForm(instance=stn_medical_details)
    if request.method == "POST":
        form = StudentMedicalDetailsForm(instance=stn_medical_details, data=request.POST)
        if form.is_valid():
            stn_med_details = form.save(commit=False)
            stn_med_details.application = application
            stn_med_details.save()
            messages.success(request, "Student Medical Information Added")
            return redirect("properties:applicant-documents", application_id=application.id)
        else:
            messages.error(request, "Student Medical Information Not Added")

    return render(request, "properties/apply/student-medical-information.html", {"form": form, "application": application})

@login_required
def applicant_documents(request, application_id):
    application = get_object_or_404(Application, id=application_id, applicant=request.user)
    applicant_documents = ApplicationDocument.objects.filter(application=application).first()
    form = ApplicationDocumentForm(instance=applicant_documents)
    if request.method == "POST":
        form = ApplicationDocumentForm(instance=applicant_documents, data=request.POST, files=request.FILES)
        if form.is_valid() and form.is_multipart():
            applicant_document = form.save(commit=False)
            applicant_document.application = application
            applicant_document.save()
            messages.success(request, "Application Documents Added")
            return redirect("properties:application-declaration", application_id=application.id)
        else:
            messages.error(request, "Application Documents Not Added")

    return render(request, "properties/apply/application-documents.html", {"form": form, "application": application})

@login_required
def applicant_declaration(request, application_id):
    application = get_object_or_404(Application, id=application_id, applicant=request.user)
    
    if request.method == "POST":
        application.is_submitted = True
        application.rules_and_terms_accepted = True
        application.save()
        messages.success(request, "Application submitted successfully")
        return render(request, "properties/apply/application-submitted.html", {"application": application})

    return render(request, "properties/apply/application-declaration.html", {"application": application})


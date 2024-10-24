from django.urls import path
from properties.views.properties import get_property
from properties.views.applications import *

app_name = "properties"
urlpatterns = [
    path("property/<slug:property_slug>", get_property, name="get-property"),
    path("applications/get-started", get_started_with_application, name="get-started-with-application"),
    path("dashboard/admin/applications/<username>", get_all_applications, name="get-all-applications"),
    path("property/<slug:property_slug>/apply-step-one", application_student_details, name="apply-student-details"),
    path("property/<slug:property_slug>/apply-step-one/<uuid:application_id>", application_student_details, name="apply-student-details-with-id"),
    path("property/<uuid:application_id>/apply-step-two", applicant_guardians, name="applicant-guardians"),
    path("property/<uuid:application_id>/applicant-medical-details", applicant_medical_details, name="applicant-medical-details"),
    path("property/<uuid:application_id>/applicant-documents", applicant_documents, name="applicant-documents"),
    path("property/<uuid:application_id>/application-declaration", applicant_declaration, name="application-declaration"),
]


from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('owner',views.admin_login,name="admin_login"),
    path("A-home",views.admin_home,name="admin_home"),
    path("D-home",views.donor_home,name="donor_home"),
    path('P-home',views.patient_home,name="patient_home"),
    path('Donor-Login',views.donor_login,name="donor_login"),
    path('Patient-Login',views.patient_login,name="patient_login"),
    path('donor-reg',views.donor_registration,name="donor_registration"),
    path('Patient-reg',views.patient_registration,name="patient_registration"),
    path('patient-logout', views.patient_logout,name="patient_logout"),
    path('view-donor',views.view_donor,name='view_donor'),
    path('view-patient',views.view_patient,name='view_patient'),
    path('view-feedback',views.admin_feedback_view,name='view_feedback'),
    path('admin-logout',views.admin_logout,name='admin_logout'),
    path('blood-requst',views.blood_request,name='blood_request'),
    path('bloodreq-view',views.blood_request_view,name="blood_request_view"),
    path('view-request',views.view_requests,name="view_requests"),
    path('blood-approve/<int:pk>/', views.blood_approve, name='blood_approve'),
    path('donor-logout',views.donor_logout,name="donor_logout"),
    path('getbloodapprove-data',views.Blood_approve_data,name='Blood_approve_data'),
    path('viewMy-donations',views.view_donations,name="view_donations"),
    path('patient-feedback',views.patient_feedback,name='patient_feedback'),
    path('donor-feedback',views.donor_feedback,name='donor_feedback'),
    path('blood_request_accepted_details/<int:req_id>/', views.accepted_details_view, name='accepted_details_view'),
]



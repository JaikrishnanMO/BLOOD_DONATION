from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('owner',views.admin_login,name="admin_login"),
    path("A-home",views.admin_home,name="admin_home"),
    path('Donor-Login',views.donor_login,name="donor_login"),
    path('Patient-Login',views.patient_login,name="patient_login"),
    path('donor-reg',views.donor_registration,name="donor_registration"),
]



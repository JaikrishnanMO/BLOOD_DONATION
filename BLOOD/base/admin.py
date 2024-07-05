from django.contrib import admin
from .models import AdminModel,DonorModel,PatientModel
# Register your models here.

admin.site.register(AdminModel)
admin.site.register(DonorModel)
admin.site.register(PatientModel)



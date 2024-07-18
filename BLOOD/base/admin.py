from django.contrib import admin
from .models import AdminModel,DonorModel,PatientModel,BloodRequest,Blood_accept,Feedback
# Register your models here.

admin.site.register(AdminModel)
admin.site.register(DonorModel)
admin.site.register(PatientModel)
admin.site.register(BloodRequest)
admin.site.register(Blood_accept)
admin.site.register(Feedback)



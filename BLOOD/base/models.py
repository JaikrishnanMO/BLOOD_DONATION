from django.db import models
# Create your models here.
class AdminModel(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=128)

    def __str__(self):
        return self.username



class DonorModel(models.Model):

    BLOOD_GROUP_CHOICES =[
        ('A+','A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    username=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    blood_group=models.CharField(max_length=3,choices=BLOOD_GROUP_CHOICES)
    phone_number=models.CharField(max_length=15)
    password=models.CharField(max_length=128)


    def __str__(self):
        return self.username 


class PatientModel(models.Model):

    BLOOD_GROUP_CHOICES =[
        ('A+','A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    username=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    blood_group=models.CharField(max_length=3,choices=BLOOD_GROUP_CHOICES)
    address=models.TextField(max_length=300, blank=True ,null=True) #optional
    phone_number=models.CharField(max_length=15)
    illness=models.TextField(max_length=400)
    password=models.CharField(max_length=128)

    def __str__(self):
        return self.username
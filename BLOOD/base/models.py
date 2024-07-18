from django.db import models
# Create your models here.
class AdminModel(models.Model):
    username=models.CharField(max_length=200,primary_key=True)
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
    email=models.EmailField(max_length=200,primary_key=True)
    blood_group=models.CharField(max_length=3,choices=BLOOD_GROUP_CHOICES)
    phone_number=models.CharField(max_length=15)
    password=models.CharField(max_length=128)
    status=models.BooleanField(default=1)


    def __str__(self):
        return self.username 


class PatientModel(models.Model):

    email=models.EmailField(max_length=200,primary_key=True)
    username=models.CharField(max_length=200)
    address=models.TextField(max_length=300, blank=True ,null=True) #optional
    phone_number=models.CharField(max_length=15)
    illness=models.TextField(max_length=400)
    password=models.CharField(max_length=128)
    status=models.BooleanField(default=1)

    def __str__(self):
        return self.username
    


class BloodRequest(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    username = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    email=models.ForeignKey(PatientModel,on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    unit = models.IntegerField()
    description = models.TextField(max_length=3000)
    hospital = models.CharField(max_length=300)
    needed_date_time = models.DateTimeField()
    requested = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username} needs {self.unit} unit(s) of {self.blood_group} blood at {self.hospital} on {self.needed_date_time}'
    


class Blood_accept(models.Model):
    blood_request_id=models.ForeignKey(BloodRequest,on_delete=models.CASCADE)
    Donor_name=models.CharField(max_length=200)
    email = models.ForeignKey(DonorModel,on_delete=models.CASCADE)
    phone=models.CharField(max_length=200)
    accepted = models.BooleanField(default=False)
    unit=models.IntegerField()
    needed_unit=models.IntegerField()
    updated= models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.Donor_name} - {self.unit} units"
    

class Feedback(models.Model):
    username=models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return f"{self.text}"
from django.shortcuts import render, redirect, get_object_or_404
from .models import AdminModel, DonorModel, PatientModel,BloodRequest,Blood_accept,Feedback
from django.http import JsonResponse
from django.urls import reverse
from django.core.serializers import serialize
from django.db.models import Sum
# Create your views here.

def home(request):
    return render(request, 'base/Home.html')

def admin_home(request):
    if 'admin_username' not in request.session:
        return redirect('admin_login')

    admin_info = AdminModel.objects.all()
    patient_info = PatientModel.objects.all()
    return render(request, "base/AdminHome.html", {'patient_info': patient_info, 'admin_info': admin_info})

def donor_home(request):
    if 'donor_email' not in request.session:
        return redirect('donor_login')
    
    donor_email=request.session['donor_email']

    try:
        donor_obj= DonorModel.objects.get(email=donor_email)
        context={'donor':donor_obj}
        return render(request,"base/DonorHome.html",context)
    except DonorModel.DoesNotExist:
        return redirect('some_error_message')
    
    

def view_donor(request):
    donor = DonorModel.objects.all()
    return render(request, "base/ViewDonor.html", {'donor': donor})

def view_patient(request):
    patient = PatientModel.objects.all()
    return render(request, "base/ViewPatient.html", {'patient': patient})

def view_feedback(request):
    return render(request, "base/ViewFeedback.html")


def patient_home(request):
    if 'patient_email' not in request.session:
        return redirect('patient_login')
    
    patient_email = request.session['patient_email']
    try:
        patient_obj = PatientModel.objects.get(email=patient_email)
        context = {'patient': patient_obj}
        return render(request, 'base/PatientHome.html', context)
    except PatientModel.DoesNotExist:
        return redirect('some_error_page')



    

def admin_login(request):
    if "admin_username" in request.session:
        return redirect('admin_home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = AdminModel.objects.filter(username=username, password=password).first()
        
        if user is not None:
            request.session['admin_username'] = username
            return JsonResponse({'success': True}, safe=False)
        else:
            return JsonResponse({'success': False}, safe=False)
    return render(request, 'base/AdminLogin.html')

def donor_login(request):
    if 'donor_email' in request.session:
        return redirect('donor_home')
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        donor = DonorModel.objects.filter(email=email, password=password,status=1).first()

        if donor is not None:
            request.session['donor_email'] = email
            return JsonResponse({'success': True}, safe=False)
        else:
            donor_banned=DonorModel.objects.filter(email=email,status=0).exists()
            if donor_banned:
                return JsonResponse({"success": False, "message": "Account is banned."}, safe=False)
            else:
                return JsonResponse({'success': False}, safe=False)
            
    return render(request, 'base/DonorLogin.html')

def patient_login(request):
    if 'patient_email' in request.session:
        return redirect('patient_home')
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        patient = PatientModel.objects.filter(email=email, password=password, status=1).first()

        if patient is not None:
            request.session["patient_email"] = email
            return JsonResponse({"success": True}, safe=False)
        else:
            patient_banned = PatientModel.objects.filter(email=email, status=0).exists()
            if patient_banned:
                return JsonResponse({"success": False, "message": "Account is banned."}, safe=False)
            else:
                return JsonResponse({"success": False, "message": "Invalid credentials."}, safe=False)
    
    return render(request, "base/PatientLogin.html")

def patient_logout(request):
    if 'patient_email' in request.session:
        request.session.pop('patient_email')
    return redirect('home')
    

def admin_logout(request):
    if 'admin_username' in request.session:
        request.session.flush()
    return redirect('home')

def donor_logout(request):
    if 'donor_email' in request.session:
        request.session.pop('donor_email')
    return redirect('home')

def donor_registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        blood_group = request.POST.get('blood_group')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        if DonorModel.objects.filter(email=email).exists():
            response = {'success': False, 'message': 'Email already Exists'}
        else:
            donor_obj = DonorModel(username=username, email=email, blood_group=blood_group, phone_number=phone_number, password=password)
            donor_obj.save()
            response = {'success': True, 'message': 'User registered successfully'}
        return JsonResponse(response)

    return render(request, "base/DonorRegistration.html")

def patient_registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        illness = request.POST.get('illness')
        password = request.POST.get('password')

        if PatientModel.objects.filter(email=email).exists():
            response = {'success': False, 'message': 'Email already Exists'}
        else:
            patient_obj = PatientModel(username=username, email=email,  address=address, phone_number=phone_number, illness=illness, password=password)
            patient_obj.save()
            response = {'success': True, 'message': 'User registered successfully'}
        return JsonResponse(response)
        
    return render(request, "base/PatientRegistration.html")



def blood_request(request):
    if request.method == "POST":
        username = request.POST.get('username')
        blood_group = request.POST.get('blood_group')
        description = request.POST.get('description')
        unit = request.POST.get('unit')
        hospital = request.POST.get('hospital')
        needed_date_time = request.POST.get('needed_date_time')
        
        try:
            patient_email=request.session['patient_email']
            patient=PatientModel.objects.get(email=patient_email)
        except PatientModel.DoesNotExist:
            response={'success':False,'message':'Patient not found'}
            return JsonResponse(response)


        if BloodRequest.objects.filter(username=username,blood_group=blood_group,requested=False).exists():
            response = {'success': False, 'message': 'Similar request already exists'}
        else:
            blood_obj = BloodRequest(
            username=username,
            phone_number=patient.phone_number,
            email=patient,
            blood_group=blood_group,
            description=description,
            unit=unit,
            hospital=hospital,
            needed_date_time=needed_date_time
            )
            blood_obj.save()
            response = {'success': True, 'message': 'Request Posted Successfully'}
            return JsonResponse(response)
    
    return render(request,"base/BloodRequest.html")


def blood_request_view(request):
    patient_email= request.session.get('patient_email')

    try:
        blood_accept=Blood_accept.objects.filter(accepted=True)
        status=BloodRequest.objects.filter(email=patient_email)
        accepted_ids=[]
        for i in blood_accept:
            blood_accepted=BloodRequest.objects.get(id=i.blood_request_id.id)
            accepted_ids.append(blood_accepted.id)
        context={'status':status,'accepted_ids':accepted_ids}
        return render(request,"base/BloodReqView.html",context)
    except BloodRequest.DoesNotExist:
        return redirect('some_error_messages')
    
#To get accepted Details

def accepted_details_view(request, req_id):
    try:
        blood_accept_det = Blood_accept.objects.filter(blood_request_id=req_id)
        accepted_details = []

        for accept in blood_accept_det:
            accepted_details.append({
                'donor_name': accept.Donor_name,
                'donor_phone':accept.phone,
                'accepted_unit': accept.unit
            })
        context = {'accepted_details': accepted_details}
        return render(request, "base/bloodacceptdetailed.html", context)
    except Blood_accept.DoesNotExist:
        return redirect('some_error_messages')







def view_requests(request):
    donor = request.session.get('donor_email')
    try:
        blood_accept = Blood_accept.objects.filter(accepted=True)
        user = DonorModel.objects.get(email=donor)
        blood_group = user.blood_group
        blood_request = BloodRequest.objects.filter(blood_group=blood_group)
        accepted_ids = []

        for i in blood_accept:
            blood_accepted = BloodRequest.objects.get(id=i.blood_request_id.id)
            accepted_ids.append(blood_accepted.id)
        context = {
            'bloodreq': blood_request,
            'blood_accept': blood_accept,
            'accepted_ids': accepted_ids
        }
        return render(request, "base/view-request.html", context)
    except DonorModel.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Some error message'})




def blood_approve(request, pk):
    try:
        blood_request = BloodRequest.objects.get(id=pk)
    except BloodRequest.DoesNotExist:
        return redirect('some_error_message') 

    context = {'blood_id': pk}

    if request.method == "POST":
        unit = int(request.POST.get('unit'))

        try:
            donor_email = request.session.get('donor_email')
            donor = DonorModel.objects.get(email=donor_email)
            print("Donor Found:", donor.username)  
        except DonorModel.DoesNotExist:
            return redirect('some_error_message')  
        
        unit_needed = blood_request.unit
        print("Unit needed:", unit_needed)

        total_accepted_units = Blood_accept.objects.filter(blood_request_id=blood_request).aggregate(Sum('unit'))['unit__sum'] or 0
        print("Total accepted units so far:", total_accepted_units)

        if total_accepted_units >= unit_needed:
            response = {'success': False, 'message': 'Request already fully accepted'}
        else:
            remaining_units = unit_needed - total_accepted_units
            print("Remaining units needed:", remaining_units)

            if unit > remaining_units:
                response = {'success': False, 'message': f'You can only donate up to {remaining_units} units'}
            else:
                accepted_units = min(unit, remaining_units)
                remaining_units -= accepted_units

                blood_donate = Blood_accept(
                    blood_request_id=blood_request,
                    Donor_name=donor.username,
                    email=donor,
                    phone=donor.phone_number,
                    accepted=(remaining_units == 0),
                    unit=accepted_units,
                    needed_unit=remaining_units
                )
                print("Blood donation object:", blood_donate)
                blood_donate.save()

                if remaining_units == 0:
                    blood_request.accepted = True
                    blood_request.save()
                    
                response = {'success': True, 'message': 'Donation made successfully'}
                context['blood_donate'] = blood_donate
                return JsonResponse(response)

    return render(request, "base/DonorAcceptReq.html", context)

def Blood_approve_data(request):
    if request.method == "GET":
        approve = Blood_accept.objects.all().values('id', 'accepted') 
        return JsonResponse({"approve": list(approve)})
    

        

def view_donations(request):
        donor_email= request.session.get('donor_email')
        donor=DonorModel.objects.get(email=donor_email)
        donation_data=Blood_accept.objects.filter(email=donor.email)
        context={'donation_data':donation_data}
        print(donation_data)
        return render(request,"base/View-Donations.html",context)
    

def patient_feedback(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')
        username = request.session.get('patient_email')
        print('username',username)

        feedback_obj = Feedback(
            username=username,
            text=feedback
        )
        feedback_obj.save()
        return JsonResponse({'success': True, 'message': 'Feedback added successfully'})

    return render(request, "base/feedback.html")



def donor_feedback(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')
        username = request.session.get('donor_email')

        feedback_obj = Feedback(
            username=username,
            text=feedback
        )
        feedback_obj.save()
        return JsonResponse({'success': True, 'message': 'Feedback added successfully'})

    return render(request, "base/DonorFeedback.html")



def admin_feedback_view(request):
        feedback=Feedback.objects.all()
        context={'feedback':feedback}
        return render(request,"base/ViewFeedback.html",context)


def ban_patient(request, p_email):
    try:
        patient = PatientModel.objects.get(email=p_email)
        patient.status = 0  
        patient.save()
        # response = JsonResponse({'success': True, "message": "Account banned successfully"})
        return redirect('view_patient')
    except PatientModel.DoesNotExist:
        response = JsonResponse({'success': False, "message": "Patient not found"})
        return response


def unban_patient(request,pU_email):
    try:
        patient = PatientModel.objects.get(email=pU_email)
        patient.status=1
        patient.save()
        return redirect('view_patient')
    except PatientModel.DoesNotExist:
        response = JsonResponse({'success': False, "message": "Patient not found"})
    return response


def ban_donor(request,d_email):
    try:
        donor= DonorModel.objects.get(email=d_email)
        donor.status=0
        donor.save()
        return redirect('view_donor')
    except PatientModel.DoesNotExist:
        response = JsonResponse({'success': False, "message": "Donor not found"})
    return response


def unban_donor(request,dU_email):
    try:
        donor= DonorModel.objects.get(email=dU_email)
        donor.status=1
        donor.save()
        return redirect('view_donor')
    except PatientModel.DoesNotExist:
        response = JsonResponse({'success': False, "message": "Donor not found"})
    return response
    


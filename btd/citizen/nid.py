from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse
from django.http import HttpResponse
import pdfkit
from .models import (
    Citizen, Applicant, Division, District, Subdistrict, 
    Healthcare, Vaccine, VaccinationSchedule, Volunteer, 
    Admin, NIDApplicant, NIDVerification, VaccineStatus,PassportApplicant
)
from django.contrib.auth.hashers import make_password, check_password
import random
import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
import json
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from datetime import datetime
from .utils import send_nid_status_email, send_nid_number_email
import logging
import os
from django.core.files.base import ContentFile
import base64

def check_birth_certificate(request):
    if 'citizen_id' not in request.session:
        return redirect("citizen:citizen_login")

    # Get citizen data
    citizen = Citizen.objects.get(id=request.session['citizen_id'])
    
    if request.method == 'POST':
        has_birth_certificate = request.POST.get('has_birth_certificate')
        print('____________________________ has id')
        if has_birth_certificate == 'yes':
            birth_application_id = request.POST.get('birth_application_id')
            try:
                print('____________________________hghf')
                # Check vaccination status
                vaccination_schedules = VaccinationSchedule.objects.filter(
                    application_id=birth_application_id
                )
                print('____________________________3')
                print(vaccination_schedules)
                if not vaccination_schedules.exists():
                    print('________________________________no shedule')
                    messages.error(request, 'No vaccination records found.')
                    return redirect('citizen:check_birth_certificate')

                # Check if all vaccinations are completed
                all_vaccinations_done = all(
                    schedule.status == "Done" 
                    for schedule in vaccination_schedules
                )
                print('____________________________1')
                print(all_vaccinations_done)
                if all_vaccinations_done:
                    print('________________________________________________________________2')
                    return redirect(f"{reverse('citizen:nid_application_existing')}?birth_application_id={birth_application_id}")
                else:
                    messages.error(request, 'Please complete all vaccinations first.')
                    return redirect('citizen:check_birth_certificate')

            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
                return redirect('citizen:check_birth_certificate')
        else:
            return redirect('citizen:nid_application')
            
    return render(request, 'citizen/check_birth_certificate.html', {
        'citizen': citizen
    })



logger = logging.getLogger(__name__)

def nid_application_existing(request):
    if 'citizen_id' not in request.session:
        return redirect("citizen:citizen_login")

    citizen = Citizen.objects.get(id=request.session['citizen_id'])
    birth_application_id = request.GET.get('birth_application_id')
    
    if not birth_application_id:
        messages.error(request, 'Birth certificate ID is required')
        return redirect('citizen:check_birth_certificate')
        
    try:
        applicant = get_object_or_404(Applicant, application_id=birth_application_id)
        districts = District.objects.all()

        subdistricts = Subdistrict.objects.all()
        
        if request.method == "POST":
            try:
                data = {
                    'name': request.POST.get('name'),
                    'father_name': request.POST.get('father_name'),
                    'mother_name': request.POST.get('mother_name'),
                    'birth_id': birth_application_id,
                    'birth_date': applicant.birth_date,
                    'birth_place': request.POST.get('birth_place'),
                    'gender': applicant.gender,
                    'marital_status': request.POST.get('marital_status'),
                    'occupation': request.POST.get('occupation'),
                    'email': request.POST.get('email'),
                    'blood_group': request.POST.get('blood_group'),
                    'subdistrict_id': request.POST.get('subdistrict'),
                }
                
                nid_applicant = NIDApplicant.objects.create(**data)
                nid_applicant.status = 'pending'
                nid_applicant.save()
                
                messages.success(request, 'Application submitted successfully')
                return redirect('citizen:citizen_panel')
                
            except Exception as e:
                messages.error(request, f'Error submitting application: {str(e)}')
                # return redirect('citizen:nid_application_existing')
        
        return render(request, 'citizen/nid_application_existing.html', {
            'applicant': applicant,
            'districts': districts,
            'subdistricts': subdistricts,
            'citizen': citizen
        })
        
    except Applicant.DoesNotExist:
        messages.error(request, 'Invalid birth certificate ID')
        return redirect('citizen:check_birth_certificate')
def nid_application(request):
    if 'citizen_id' not in request.session:
        return redirect("citizen:citizen_login")
        
    if request.method == "POST":
        try:
            data = {
                'name': request.POST.get('name'),
                'father_name': request.POST.get('father_name'),
                'father_nid': request.POST.get('father_nid'),
                'mother_name': request.POST.get('mother_name'),
                'mother_nid': request.POST.get('mother_nid'),
                'birth_id': request.POST.get('birth_id'),
                'birth_date': request.POST.get('birth_date'),
                'birth_place': request.POST.get('birth_place'),
                'gender': request.POST.get('gender'),
                'marital_status': request.POST.get('marital_status'),
                'husband_name': request.POST.get('husband_name', ''),
                'wife_name': request.POST.get('wife_name', ''),
                'occupation': request.POST.get('occupation'),
                'email': request.POST.get('email'),
                'blood_group': request.POST.get('blood_group'),
                'subdistrict_id': request.POST.get('subdistrict'),
                'academic_certificate': request.FILES.get('academic_certificate'),
            }
            
            academic_certificate = request.FILES.get('academic_certificate')
            if not academic_certificate:
                messages.error(request, 'Academic certificate is required')
                return redirect('citizen:nid_application')
            
            if not academic_certificate.name.endswith('.pdf'):
                messages.error(request, 'Only PDF files are allowed')
                return redirect('citizen:nid_application')
                
            if academic_certificate.size > 5242880:  # 5MB
                messages.error(request, 'File size must be under 5MB')
                return redirect('citizen:nid_application')

            subdistrict = Subdistrict.objects.get(id=data['subdistrict_id'])
            
            applicant = NIDApplicant.objects.create(**data)
            applicant.subdistrict = subdistrict
            applicant.status = 'pending'
            applicant.save()
            messages.success(request, 'Application submitted successfully')
            return redirect('citizen:citizen_panel')
        except Exception as e:
            messages.error(request, f'Error submitting application: {str(e)}')
            return redirect('citizen:nid_application')

    subdistricts = Subdistrict.objects.all()
    return render(request, 'citizen/nid_app.html', {'subdistricts': subdistricts})

def calculate_age(birth_date):
    today = date.today()
    # Convert string to datetime object if it's a string
    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
    elif isinstance(birth_date, datetime):
        birth_date = birth_date.date()
    
    age = relativedelta(today, birth_date).years
    return age

def view_nid_applications(request):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
    
    admin_id = request.session['admin_id']
    admin = Admin.objects.get(id=admin_id)
    
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    
    # Base queryset
    applications = NIDApplicant.objects.filter(subdistrict_id=admin.subdistrict_id)
    
    # Apply filters
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    if search_query:
        applications = applications.filter(
            Q(name__icontains=search_query) |
            Q(birth_id__icontains=search_query) |
            Q(father_name__icontains=search_query) |
            Q(mother_name__icontains=search_query)
        )
    
    # Order by latest first
    applications = applications.order_by('-id')
    
    context = {
        'applications': applications,
        'admin': admin,
        'status_filter': status_filter,
        'search_query': search_query,
        'status_choices': ['pending', 'approved', 'rejected']
    }
    
    return render(request, 'citizen/view_nid.html', context)

def update_nid_status(request, application_id):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
        
    admin = Admin.objects.get(id=request.session['admin_id'])
    try:
        application = NIDApplicant.objects.get(id=application_id, subdistrict_id=admin.subdistrict_id)
        
        if request.method == 'POST':
            status = request.POST.get('status')
            if status in ['approve', 'reject']:
                application.status = 'approved' if status == 'approve' else 'rejected'
                application.save()
            
            # Create verification record
            user_id = f"BTD{str(application_id).zfill(8)}"
            verification_date = date.today() + timedelta(days=1)
            
            verification = NIDVerification.objects.create(
                user_id=user_id,
                name=application.name,
                father_name=application.father_name,
                mother_name=application.mother_name,
                birth_date=application.birth_date,
                blood_group=application.blood_group,
                verification_date=verification_date
            )
            
            # Send approval email
            email_sent = send_nid_status_email(
                applicant=application,
                status='approved',
                user_id=user_id,
                verification_date=verification_date
            )
            
            success_msg = f'Application approved successfully. User ID: {user_id}'
            if not email_sent:
                success_msg += ' (Email notification failed)'
            messages.success(request, success_msg)
            
        else:
            messages.error(request, 'Invalid action')
            
    except NIDApplicant.DoesNotExist:
        messages.error(request, 'Application not found')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    
    return redirect('citizen:view_nid_applications')

def verification_management(request):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
        
    verifications = NIDVerification.objects.all().order_by('-created_at')
    return render(request, 'citizen/verification_management.html', {
        'verifications': verifications
    })

def update_verification_status(request, verification_id):
    print(verification_id)
    if 'admin_id' not in request.session:
        messages.error(request, 'Not authorized')
        return redirect('citizen:admin_login')
    
    if request.method != 'POST':
        return redirect('citizen:verification_management')
    
    try:
        status_type = request.POST.get('type')
        verification = get_object_or_404(NIDVerification, id=verification_id)
        
        if status_type == 'fingerprint':
            verification.fingerprint_status = 'completed'
            success_msg = 'Fingerprint status updated successfully'
        elif status_type == 'face':
            verification.face_status = 'completed'
            success_msg = 'Face status updated successfully'
        else:
            messages.error(request, 'Invalid status type')
            return redirect('citizen:verification_management')
            
        verification.save()
        messages.success(request, success_msg)
        
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    
    return redirect('citizen:verification_management')

def generate_nid(request, verification_id):
    if 'admin_id' not in request.session:
        messages.error(request, 'Not authorized')
        return redirect('citizen:admin_login')
    
    if request.method != 'POST':
        return redirect('citizen:verification_management')
    
    try:
        verification = get_object_or_404(NIDVerification, id=verification_id)
        
        if verification.fingerprint_status != 'completed' or verification.face_status != 'completed':
            messages.error(request, 'Both fingerprint and face verification must be completed')
            return redirect('citizen:verification_management')
            
        nid_number = NIDVerification.generate_nid_number(verification.birth_date)
        verification.nid_number = nid_number
        verification.verification_status = 'verified'
        verification.save()
        
        # Send email notification with NID number
        email_sent = send_nid_number_email(verification)
        
        success_msg = f'NID Generated successfully: {nid_number}'
        if not email_sent:
            success_msg += ' (Email notification failed)'
        messages.success(request, success_msg)
        
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    
    return redirect('citizen:verification_management')

def download_nid(request):
    if 'citizen_id' not in request.session:
        return redirect("citizen:citizen_login")
        
    citizen = Citizen.objects.get(id=request.session['citizen_id'])
    
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        try:
            verification = NIDVerification.objects.get(user_id=user_id)
            if verification.verification_status == 'verified':
                return render(request, 'citizen/nid_template.html', {
                    'verification': verification
                })
            else:
                messages.error(request, 'Your NID is not verified yet')
        except NIDVerification.DoesNotExist:
            messages.error(request, 'No NID found with this User ID')
            
    return render(request, 'citizen/download_nid.html', {'citizen': citizen})

def check_application_status(request):
    if 'citizen_id' not in request.session:
        return redirect("citizen:citizen_login")
        
    citizen = Citizen.objects.get(id=request.session['citizen_id'])
    
    if request.method == "POST":
        application_type = request.POST.get('application_type')
        
        if application_type == 'nid':
            user_id = request.POST.get('user_id')
            try:
                verification = NIDVerification.objects.get(user_id=user_id)
                return render(request, 'citizen/status_result.html', {
                    'verification': verification,
                    'type': 'nid',
                    'citizen': citizen
                })
            except NIDVerification.DoesNotExist:
                messages.error(request, 'No NID application found')
                return redirect('citizen:nid_status_check')
                
        elif application_type == 'passport':
            tracking_number = request.POST.get('tracking_number')
            try:
                passport = PassportApplicant.objects.get(tracking_number=tracking_number)
                return render(request, 'citizen/status_result.html', {
                    'passport': passport,
                    'type': 'passport',
                    'citizen': citizen
                })
            except PassportApplicant.DoesNotExist:
                messages.error(request, 'No passport application found')
                return redirect('citizen:passport_status_check')
    
    return render(request, 'citizen/track_status.html', {'citizen': citizen})
def update_face_photo(request, verification_id):
    if 'admin_id' not in request.session:
        return JsonResponse({'success': False, 'error': 'Not authorized'})
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})
        
    try:
        verification = get_object_or_404(NIDVerification, id=verification_id)
        
        if 'face_photo' not in request.FILES:
            return JsonResponse({'success': False, 'error': 'No photo provided'})
            
        # Save the photo
        verification.face_photo = request.FILES['face_photo']
        verification.face_status = 'completed'
        verification.save()
        
        return JsonResponse({
            'success': True,
            'photo_url': verification.face_photo.url
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
def face_verification(request, verification_id):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
        
    verification = get_object_or_404(NIDVerification, id=verification_id)
    return render(request, 'citizen/face_verfication.html', {
        'verification': verification
    })
def search_nid(request):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
        
    admin = Admin.objects.get(id=request.session['admin_id'])
    
    
    search_query = request.GET.get('nid', '')
    result = None
    search_performed = False
    
    if search_query:
        search_performed = True
        try:
            result = NIDVerification.objects.get(nid_number=search_query)
        except NIDVerification.DoesNotExist:
            pass
    
    context = {
        'admin': admin,
        'search_query': search_query,
        'result': result,
        'search_performed': search_performed
    }
    
    return render(request, 'citizen/search_nid.html', context)

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PassportApplicant, District, Subdistrict,PassportVerification,Admin
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from django.http import JsonResponse
from .utils import send_passport_application_email
from django.core.files.storage import FileSystemStorage
import os
from django.utils import timezone
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404


from django.utils.dateparse import parse_date

def passport_application(request):
    if 'citizen_id' not in request.session:
        return redirect('citizen:citizen_login')
        
    if request.method == "POST":
        try:
            # Get citizen_id from session
            citizen_id = request.session.get('citizen_id')
            
            # Get form data - Personal Information
            name_en = request.POST['name_en']
            name_bn = request.POST['name_bn']
            father_name = request.POST['father_name']
            father_nationality = request.POST['father_nationality']
            mother_name = request.POST['mother_name']
            mother_nationality = request.POST['mother_nationality']
            spouse_name = request.POST.get('spouse_name', '')
            spouse_nationality = request.POST.get('spouse_nationality', '')
            nid_number = request.POST['nid_number']
            birth_certificate_number = request.POST['birth_certificate_number']
            birth_date = parse_date(request.POST['birth_date'])
            birth_place = request.POST['birth_place']
            birth_country = request.POST['birth_country']
            gender = request.POST['gender']
            marital_status = request.POST['marital_status']
            profession = request.POST['profession']
            
            # Contact Information
            present_address = request.POST['present_address']
            present_district_id = request.POST['present_district']
            present_subdistrict_id = request.POST['present_subdistrict']
            permanent_address = request.POST['permanent_address']
            permanent_district_id = request.POST['permanent_district']
            permanent_subdistrict_id = request.POST['permanent_subdistrict']
            phone = request.POST['phone']
            email = request.POST['email']
            
            # Passport Details
            passport_type = request.POST['passport_type']
            page_type = request.POST['page_type']
            delivery_type = request.POST['delivery_type']
            
            # Previous Passport Details (if any)
            old_passport_number = request.POST.get('old_passport_number', '')
            old_passport_issue_date = parse_date(request.POST.get('old_passport_issue_date', None))
            old_passport_expiry_date = parse_date(request.POST.get('old_passport_expiry_date', None))
            
            # File Handling
            nid_scan = request.FILES.get('nid_scan')
            birth_certificate_scan = request.FILES.get('birth_certificate_scan')
            old_passport_scan = request.FILES.get('old_passport_scan', None)
            
            # Validate files
            if not nid_scan or not birth_certificate_scan:
                messages.error(request, 'Please upload all required documents')
                return redirect('citizen:passport_application')
                
            # Create Passport Application
            application = PassportApplicant.objects.create(
                citizen_id=citizen_id,
                name_en=name_en,
                name_bn=name_bn,
                father_name=father_name,
                father_nationality=father_nationality,
                mother_name=mother_name,
                mother_nationality=mother_nationality,
                spouse_name=spouse_name,
                spouse_nationality=spouse_nationality,
                nid_number=nid_number,
                birth_certificate_number=birth_certificate_number,
                birth_date=datetime.combine(birth_date, datetime.min.time()) if birth_date else None,
                birth_place=birth_place,
                birth_country=birth_country,
                gender=gender,
                marital_status=marital_status,
                profession=profession,
                
                present_address=present_address,
                present_district_id=present_district_id,
                present_subdistrict_id=present_subdistrict_id,
                permanent_address=permanent_address,
                permanent_district_id=permanent_district_id,
                permanent_subdistrict_id=permanent_subdistrict_id,
                phone=phone,
                email=email,
                
                passport_type=passport_type,
                page_type=page_type,
                delivery_type=delivery_type,
                
                old_passport_number=old_passport_number if old_passport_number else None,
                old_passport_issue_date=datetime.combine(old_passport_issue_date, datetime.min.time()) if old_passport_issue_date else None,
                old_passport_expiry_date=datetime.combine(old_passport_expiry_date, datetime.min.time()) if old_passport_expiry_date else None,
                
                nid_scan=nid_scan,
                birth_certificate_scan=birth_certificate_scan,
                old_passport_scan=old_passport_scan
            )
            
            # Send confirmation email
            email_sent = send_passport_application_email(application)
            
            success_msg = f'Application submitted successfully. Your tracking number is: {application.tracking_number}'
            if not email_sent:
                success_msg += ' (Email notification could not be sent)'
            
            messages.success(request, success_msg)
            return redirect('citizen:citizen_panel')
            
        except Exception as e:
            print(f"Error in passport application: {str(e)}")
            messages.error(request, 'Error submitting application. Please try again.')
            return redirect('citizen:passport_application')
    
    # For GET request, show the form
    districts = District.objects.all().order_by('name')
    subdistricts = Subdistrict.objects.all().order_by('name')
    
    context = {
        'districts': districts,
        'subdistricts': subdistricts,
    }
    return render(request, 'citizen/passport_app.html', context)
def load_subdistricts(request):
    district_id = request.GET.get('district_id')
    subdistricts = Subdistrict.objects.filter(district_id=district_id).order_by('name')
    return JsonResponse(list(subdistricts.values('id', 'name')), safe=False)



def generate_transaction_id():
    """Generate a unique transaction ID"""
    prefix = "TRX"
    timestamp = timezone.now().strftime("%Y%m%d%H%M")
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}{timestamp}{random_str}"

def send_payment_confirmation_email(application):
    """Send payment confirmation email"""
    subject = 'Passport Application Payment Confirmation'
    message = f"""
    Dear {application.name_en},

    Your payment for passport application has been successfully processed.

    Details:
    - Tracking Number: {application.tracking_number}
    - Amount Paid: ৳{application.payment_amount}
    - Transaction ID: {application.transaction_id}
    - Payment Method: {application.payment_method}
    - Payment Date: {application.payment_date.strftime('%d %B %Y')}

    Your application is now being processed. You will receive further updates via email.

    Thank you for using our service.

    Best regards,
    BTD Passport Services
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [application.email],
        fail_silently=False,
    )

def process_payment(request, tracking_number):
    if request.method != 'POST':
        return redirect('citizen:pay_fees')
        
    try:
        # Get the application
        application = PassportApplicant.objects.get(
            tracking_number=tracking_number,
            citizen_id=request.session['citizen_id']
        )
        
        # Get payment details
        bkash_number = request.POST.get('bkash_number')
        transaction_id = request.POST.get('transaction_id')
        amount = float(request.POST.get('amount', 0))
        
        # Validate payment details
        if not bkash_number or not transaction_id:
            messages.error(request, 'Please provide all payment details')
            return redirect('citizen:pay_fees')
        
        # Update application payment status
        application.payment_status = 'paid'  # Change to 'processing' instead of 'paid'
        application.payment_date = timezone.now()
        application.payment_amount = amount
        application.transaction_id = transaction_id
        application.payment_method = 'bkash'
        application.bkash_number = bkash_number
        application.save()
        
        # Send confirmation email
        try:
            send_payment_confirmation_email(application)
        except Exception as e:
            print(f"Error sending email: {str(e)}")
        
        messages.success(request, 'Payment submitted successfully! Admin will verify your payment shortly.')
        
    except PassportApplicant.DoesNotExist:
        messages.error(request, 'Invalid application or unauthorized access')
    except Exception as e:
        messages.error(request, f'Error processing payment: {str(e)}')
    
    return redirect('citizen:pay_fees')

def pay_fees(request):
    if 'citizen_id' not in request.session:
        return redirect('citizen:citizen_login')
        
    citizen_id = request.session['citizen_id']
    print(f"Citizen ID: {citizen_id}")  # Debug print
    
    applications = PassportApplicant.objects.filter(
        citizen_id=citizen_id
    ).order_by('-created_at')
    
    context = {
        'applications': applications,
    }
    return render(request, 'citizen/pay_fees.html', context)
           
        

def passport_face_verification(request, verification_id): 
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
        
    verification = get_object_or_404(PassportVerification, id=verification_id)
    return render(request, 'citizen/face_passport.html', {
        'verification': verification
    })

def update_passport_face_photo(request, verification_id):
    if 'admin_id' not in request.session:
        return JsonResponse({'success': False, 'error': 'Not authorized'})
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})
        
    try:
        verification = get_object_or_404(PassportVerification, id=verification_id)
        
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
    


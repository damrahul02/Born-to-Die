from django.shortcuts import render, redirect
from django.contrib import messages
from .models import NIDVerification, NIDApplicant, AllowanceApplicant, Subdistrict, Admin,Citizen
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.utils import timezone  # Add this import for timezone awareness


def allowance_application(request):
    if 'citizen_id' not in request.session:
        return redirect('citizen:citizen_login')
    return render(request, 'citizen/allowance_application.html')

def verify_allowance_eligibility(request):
    if 'citizen_id' not in request.session:
        return redirect('citizen:citizen_login')
        
    if request.method != 'POST':
        return redirect('citizen:allowance_application')
        
    nid_number = request.POST.get('nid_number')
    birth_date = request.POST.get('birth_date')
    
    try:
        # Check if NID exists and is verified
        nid_verification = NIDVerification.objects.get(
            nid_number=nid_number,
            birth_date=birth_date,
            verification_status='verified'
        )
        
        # Calculate age
        today = datetime.now().date()
        age = relativedelta(today, nid_verification.birth_date).years
        
        if age < 60:
            messages.error(request, f'You must be 60 years or older to apply for allowance. Your current age is {age} years.')
            return redirect('citizen:allowance_application')
            
        # Check if already applied
        if AllowanceApplicant.objects.filter(nid_number=nid_number).exists():
            messages.error(request, 'You have already applied for allowance.')
            return redirect('citizen:allowance_application')
            
        # Get applicant details from NIDApplicant
        nid_applicant = NIDApplicant.objects.get(
            Q(birth_id=nid_verification.user_id) |
            Q(birth_date=birth_date, name=nid_verification.name)
        )
        
        # Prepare applicant info for the template
        applicant_info = {
            'nid_number': nid_number,
            'name': nid_applicant.name,
            'father_name': nid_applicant.father_name,
            'mother_name': nid_applicant.mother_name,
            'birth_date': nid_applicant.birth_date,
            'gender': nid_applicant.gender,
            'present_address': nid_applicant.subdistrict.name,
            'permanent_address': nid_applicant.subdistrict.name,
            'subdistrict_id': nid_applicant.subdistrict.id
        }
        
        return render(request, 'citizen/allowance_application.html', {'applicant_info': applicant_info})
        
    except NIDVerification.DoesNotExist:
        messages.error(request, 'Invalid NID number or birth date.')
    except NIDApplicant.DoesNotExist:
        messages.error(request, 'Applicant details not found.')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        
    return redirect('citizen:allowance_application')

def submit_allowance_application(request):
    if 'citizen_id' not in request.session:
        return redirect('citizen:citizen_login')
        
    if request.method != 'POST':
        return redirect('citizen:allowance_application')
        
    try:
        nid_number = request.POST.get('nid_number')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        documents = request.FILES.get('documents')
       
        if not documents:
            messages.error(request, 'Please upload the required documents.')
            return redirect('citizen:allowance_application')

        # Get NID verification record
        nid_verification = NIDVerification.objects.get(nid_number=nid_number)
        
        # Get NID applicant details
        nid_applicant = NIDApplicant.objects.get(
            Q(birth_id=nid_verification.user_id) |
            Q(birth_date=nid_verification.birth_date, name=nid_verification.name)
        )
        
        # Get the citizen instance
        citizen = Citizen.objects.get(id=request.session['citizen_id'])
        
        # Create folder name based on username and NID
        folder_name = f"{nid_applicant.name.replace(' ', '')}{nid_number}"
        file_path = f'allowance_documents/{folder_name}/{documents.name}'
        
        # Create allowance application with the correct birth_date
        allowance = AllowanceApplicant.objects.create(
            citizen=citizen,
            nid_number=nid_number,
            name=nid_applicant.name,
            father_name=nid_applicant.father_name,
            mother_name=nid_applicant.mother_name,
            birth_date=nid_applicant.birth_date,  # Use the actual birth date from nid_applicant
            gender=nid_applicant.gender,
            present_address=nid_applicant.subdistrict.name,
            permanent_address=nid_applicant.subdistrict.name,
            mobile_number=mobile_number,
            email=email,
            subdistrict_id=nid_applicant.subdistrict.id,
            documents=documents
        )
        
        # Get subdistrict name for success message
        subdistrict = Subdistrict.objects.get(id=nid_applicant.subdistrict.id)
        messages.success(request, 'Your allowance application has been submitted successfully.')
        return render(request, 'citizen/allowance_application.html', {'subdistrict_name': subdistrict.name})
        
    except NIDVerification.DoesNotExist:
        messages.error(request, 'Invalid NID number.')
    except NIDApplicant.DoesNotExist:
        messages.error(request, 'Applicant details not found.')
    except Exception as e:
        messages.error(request, f'Error submitting application: {str(e)}')
        
    return redirect('citizen:allowance_application')        
def manage_allowance_requests(request):
    try:
        # Get admin details from session
        admin_id = request.session.get('admin_id')
        
        if not admin_id:
            messages.error(request, 'Please login as a subdistrict admin')
            return redirect('citizen:admin_login')
            
        # Get admin from database
        admin = Admin.objects.get(id=admin_id)
        
        # Verify this is a subdistrict admin
       
        
        # Get all allowance applications for this subdistrict
        applications = AllowanceApplicant.objects.filter(
            subdistrict_id=admin.subdistrict_id
        ).order_by('-application_date')
        
        # Debug: Print document paths
        for app in applications:
            if app.documents:
                print(f"Document path: {app.documents.path}")
                print(f"Document URL: {app.documents.url}")
        
        context = {
            'applications': applications,
            'admin': admin
        }
        
        return render(request, 'citizen/manage_allowance_requests.html', context)
        
    except Admin.DoesNotExist:
        messages.error(request, 'Admin account not found')
        return redirect('citizen:admin_login')

def approve_allowance(request):
    if request.method != 'POST':
        return redirect('citizen:manage_allowance_requests')
        
    try:
        admin = Admin.objects.get(id=request.session['admin_id'])
        nid_number = request.POST.get('nid_number')
        
        # Get application
        application = AllowanceApplicant.objects.get(
            nid_number=nid_number,
            subdistrict_id=admin.subdistrict_id
        )
        
        # Update status
        application.status = 'approved'
        application.save()
        
        # Send approval email
        from .utils import send_allowance_status_email
        if send_allowance_status_email(application, 'approved'):
            messages.success(request, 'Application approved and email sent successfully.')
        else:
            messages.warning(request, 'Application approved but failed to send email notification.')
            
    except (Admin.DoesNotExist, AllowanceApplicant.DoesNotExist):
        messages.error(request, 'Application not found or you do not have permission to approve it.')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        
    return redirect('citizen:manage_allowance_requests')

def reject_allowance(request):
    if request.method != 'POST':
        return redirect('citizen:manage_allowance_requests')
        
    try:
        admin = Admin.objects.get(id=request.session['admin_id'])
        nid_number = request.POST.get('nid_number')
        rejection_reason = request.POST.get('rejection_reason')
        
        if not rejection_reason:
            messages.error(request, 'Rejection reason is required.')
            return redirect('citizen:manage_allowance_requests')
            
        # Get application
        application = AllowanceApplicant.objects.get(
            nid_number=nid_number,
            subdistrict_id=admin.subdistrict_id
        )
        
        # Send rejection email before deleting
        from .utils import send_allowance_status_email
        if send_allowance_status_email(application, 'rejected', rejection_reason):
            # Delete the application after sending email
            application.delete()
            messages.success(request, 'Application rejected and email sent successfully.')
        else:
            messages.error(request, 'Failed to send rejection email. Please try again.')
            
    except (Admin.DoesNotExist, AllowanceApplicant.DoesNotExist):
        messages.error(request, 'Application not found or you do not have permission to reject it.')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        
    return redirect('citizen:manage_allowance_requests')
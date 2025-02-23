from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from .models import NIDApplicant
from django.template.loader import render_to_string

def send_nid_status_email(applicant, status, user_id=None, verification_date=None):
    """
    Send email notification for NID application status
    """
    subject = f'NID Application Status Update - {status.upper()}'
    
    if status == 'approved':
        message = f"""Dear {applicant.name},

Your NID application has been approved. Here are your details:

User ID: {user_id}
Verification Date: {verification_date.strftime('%d %B, %Y')}

Please visit your nearest verification center on the verification date with your original documents.

Best regards,
BTD Admin Team"""

    else:  
        message = f"""Dear {applicant.name},

We regret to inform you that your NID application has been rejected.

You can submit a new application after addressing any issues with your documentation.

Best regards,
BTD Admin Team"""

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[applicant.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def send_nid_number_email(verification):
    """
    Send email notification when NID number is generated
    """
    subject = 'Your NID Number Has Been Generated'
    
    message = f"""Dear {verification.name},

Your National ID (NID) number has been generated successfully.

NID Number: {verification.nid_number}

Please keep this number safe as it will be required for various official purposes.

Best regards,
BTD Admin Team"""

    try:
        # Get the original application to get the email address
        applicant = NIDApplicant.objects.get(name=verification.name, birth_date=verification.birth_date)
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[applicant.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending NID number email: {str(e)}")
        return False

def send_passport_application_email(application):
    """
    Send email notification for passport application
    """
    subject = 'Passport Application Submitted Successfully'
    
    message = f"""Dear {application.name_en},

Your passport application has been submitted successfully.

Application Details:
Tracking Number: {application.tracking_number}
Passport Type: {application.get_passport_type_display()}
Delivery Type: {application.get_delivery_type_display()}

You can track your application status using the tracking number.

Best regards,
BTD Admin Team"""

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[application.email],
            fail_silently=False,
        )
        print(f"Email sent successfully to {application.email}")  # Debug print
        return True
    except Exception as e:
        print(f"Error sending passport application email: {str(e)}")  # Debug print
        return False

def send_verification_status_email(application):
    """Send email notification about police verification status update"""
    
    status_messages = {
        'in_progress': 'Your passport application is currently under police verification.',
        'verified': 'Your passport application has passed police verification.',
        'rejected': 'Your passport application has been rejected in police verification.'
    }
    
    subject = f'Passport Application - Police Verification Update'
    
    message = f"""
    Dear {application.name_en},

    {status_messages.get(application.police_verification_status, 'Your passport application status has been updated.')}

    Application Details:
    - Tracking Number: {application.tracking_number}
    - Verification Status: {application.police_verification_status.title()}
    - Verification Date: {application.police_verification_date.strftime('%d %B %Y')}
    - Police Station: {application.police_station}
    
    Additional Information:
    {application.police_comments if application.police_comments else 'No additional comments.'}

    Please log in to your account to view more details.

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

def send_passport_number_email(verification):
    """Send email notification when passport number is generated"""
    subject = 'Your Passport Number Has Been Generated'
    
    message = f"""Dear {verification.application.name_en},

Your passport has been generated successfully.

Passport Number: {verification.passport_number}
Issue Date: {verification.verification_date.strftime('%d %B %Y')}
Expiry Date: {(verification.verification_date + timedelta(days=3650)).strftime('%d %B %Y')}

Please visit your nearest passport office to collect your passport.

Best regards,
BTD Passport Services"""

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[verification.application.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending passport number email: {str(e)}")
        return False

def send_passport_ready_email(verification):
    """Send email notification when passport is ready for collection"""
    subject = 'Your Passport is Ready for Collection'
    
    message = f"""Dear {verification.application.name_en},

Your passport has been printed and is ready for collection.

Passport Details:
- Passport Number: {verification.passport_number}
- Issue Date: {verification.verification_date.strftime('%d %B %Y')}
- Expiry Date: {(verification.verification_date + timedelta(days=3650)).strftime('%d %B %Y')}

Please visit your nearest passport office to collect your passport. 
Don't forget to bring your original documents and application receipt.

Best regards,
BTD Passport Services"""

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[verification.application.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending passport ready email: {str(e)}")
        return False 
    

def send_police_admin_credentials(admin_name, admin_email, admin_password):
    """Send email with login credentials to new police admin"""
    subject = 'Your Police Admin Account Credentials'
    
    message = f"""Dear {admin_name},

Your police admin account has been created successfully.

Login Details:
Email: {admin_email}
Password: {admin_password}
Login URL: http://127.0.0.1:8000/admins/login/

Please change your password after your first login for security purposes.

Best regards,
BTD Admin Team"""

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending police admin credentials email: {str(e)}")
        return False
def send_allowance_status_email(application, status, rejection_reason=None):
    """
    Send email notification for allowance application status
    """
    subject = f'Old Age Allowance Application Status Update - {status.upper()}'
    
    if status == 'approved':
        message = f"""Dear {application.name},

We are pleased to inform you that your Old Age Allowance application has been approved.

Your application details:
NID Number: {application.nid_number}
Application Date: {application.application_date.strftime('%d %B, %Y')}

You will be contacted by your local subdistrict office regarding the next steps and allowance disbursement process.

Best regards,
BTD Admin Team"""

    else:  # rejected
        message = f"""Dear {application.name},

We regret to inform you that your Old Age Allowance application has been rejected.

Reason for rejection:
{rejection_reason}

If you believe this decision was made in error or if you have additional documentation to support your application, you may submit a new application.

Best regards,
BTD Admin Team"""

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[application.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending allowance status email: {str(e)}")
        return False
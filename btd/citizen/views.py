from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Citizen, Applicant, Division, District, Subdistrict, Healthcare,Vaccine,VaccinationSchedule,Volunteer,Admin,NIDApplicant, PassportApplicant, PassportVerification, BabyReg,MonthlyReport
from django.contrib.auth.hashers import make_password, check_password
import random
import datetime
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
import json
from django.core.paginator import Paginator
from datetime import datetime, timedelta, date
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from .utils import send_verification_status_email, send_passport_number_email, send_passport_ready_email
from django.template.loader import render_to_string
import pdfkit
from django.db.models import Count
from django.db.models import Sum
import ast
from .utils import send_police_admin_credentials

def home(request):
    return render(request, 'citizen/index.html')
def about(request):
    return render(request, 'citizen/about.html')

def citizen_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            citizen = Citizen.objects.get(username=username)
            if check_password(password, citizen.password):
                # Successful login
                request.session['citizen_id'] = citizen.id  # Store citizen ID in session
                request.session['username'] = citizen.username  # Store username in session
                return redirect('citizen:citizen_panel')  # Redirect to citizen panel after login
            else:
                messages.error(request, 'Invalid username or password')
        except Citizen.DoesNotExist:
            messages.error(request, 'Invalid username or password')
    return render(request, 'citizen/citizen_login.html')

def citizen_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if Citizen.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('citizen:citizen_register')

        if Citizen.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('citizen:citizen_register')

        # Hash the password before saving
        hashed_password = make_password(password)
        Citizen.objects.create(
            name=name,
            username=username,
            email=email,
            password=hashed_password
        )
        messages.success(request, 'Registration successful. You can now login.')
        return redirect('citizen:citizen_login')

    return render(request, 'citizen/citizen_register.html')

def citizen_panel(request):
    if 'citizen_id' not in request.session:
        return redirect('citizen:citizen_login')
        
    citizen_id = request.session['citizen_id']
    citizen = Citizen.objects.get(id=citizen_id)
    # Only fetch basic fields until the new columns are added
    passport_applications = PassportApplicant.objects.filter(
        citizen_id=citizen_id
    ).only(
        'tracking_number', 
        'name_en', 
        'application_status', 
        'created_at'
    ).order_by('-created_at')
    
    context = {
        'citizen': citizen,
        'passport_applications': passport_applications,
    }
    return render(request, 'citizen/citizen_panel.html', context)

def citizen_profile(request):
    # Check if the user is logged in
    if 'citizen_id' not in request.session:
        return redirect('citizen:citizen_login')  # Redirect to login if not logged in

    citizen_id = request.session['citizen_id']
    citizen = Citizen.objects.get(id=citizen_id)  # Get the logged-in citizen's details

    return render(request, 'citizen/citizen_panel.html', {'citizen': citizen})

def citizen_pass(request):
    if 'citizen_id' not in request.session:
        return redirect('citizen:citizen_login')

    citizen_id = request.session['citizen_id']
    citizen = Citizen.objects.get(id=citizen_id)

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Verify current password
        if not check_password(current_password, citizen.password):
            messages.error(request, 'Current password is incorrect')
            return redirect('citizen:citizen_pass')

        # Verify new passwords match
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match')
            return redirect('citizen:citizen_pass')

        # Update password
        citizen.password = make_password(new_password)
        citizen.save()

        messages.success(request, 'Password updated successfully')
        return redirect('citizen:citizen_panel')

    return render(request, 'citizen/change_password.html', {'citizen': citizen})

def citizen_update(request):
    if 'citizen_id' not in request.session:
        return redirect('citizen:citizen_login')

    citizen_id = request.session['citizen_id']
    citizen = Citizen.objects.get(id=citizen_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Check if email already exists for another user
        if Citizen.objects.filter(email=email).exclude(id=citizen_id).exists():
            messages.error(request, 'Email already exists')
            return redirect('citizen:citizen_update')

        # Update profile
        citizen.name = name
        citizen.email = email
        citizen.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('citizen:citizen_panel')

    return render(request, 'citizen/update_profile.html', {'citizen': citizen})

def logout(request):
    # Clear the session
    request.session.flush()  # This will remove all session data
    messages.success(request, 'You have been logged out successfully.')
    return redirect('citizen:citizen_login')  # Redirect to login page after logout

def admin_logout(request):
    # Clear the session
    request.session.flush()  # This will remove all session data
    messages.success(request, 'You have been logged out successfully.')
    return redirect('citizen:admin_login')  # Redirect to login page after logout

def register_vaccine_part1(request):
    if request.method == 'POST':
        division_id = request.POST.get('division')
        district_id = request.POST.get('district')
        subdistrict_id = request.POST.get('subdistrict')
        healthcare_id = request.POST.get('healthcare')

        # Validate input
        if not all([division_id, district_id, subdistrict_id, healthcare_id]):
            messages.error(request, 'All fields are required.')
            return redirect('citizen:register_vaccine_part1')

        # Store data in session
        request.session['division_id'] = division_id
        request.session['district_id'] = district_id
        request.session['subdistrict_id'] = subdistrict_id
        request.session['healthcare_id'] = healthcare_id

        # Redirect to the baby registration page
        return redirect('citizen:register_baby')

    # Load divisions for the dropdown
    divisions = Division.objects.all()
    return render(request, 'citizen/register_vaccine_part1.html', {'divisions': divisions})

def register_baby(request):
    if request.method == 'POST':
        # Collect form data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        full_name = request.POST['full_name']
        gender = request.POST['gender']
        religion = request.POST['religion']
        birth_country = request.POST['birth_country']
        birth_division_id = request.POST['birth_division']
        birth_district_id = request.POST['birth_district']
        birth_subdistrict_id = request.POST['birth_subdistrict']
        division_id = request.session.get('division_id')
        district_id = request.session.get('district_id')
        subdistrict_id = request.session.get('subdistrict_id')
        birth_date = datetime.strptime(request.POST['birth_date'], '%Y-%m-%d').date()
        
        #print('_________________________________________________________________________________1')
        # # Prepare birth date - Fixed date handling
        # try:
        #     year = int(request.POST['selectYear'])
        #     month = request.POST['selectMonth']
        #     day = int(request.POST['selectDay'])

        #      Create date object using date class directly
        #     print("wadrxufdsghajfbdg")
        #     # birth_date = date(year, month, day)
        #     print(birth_date)
        # except (ValueError, KeyError, TypeError) as e:
        #     messages.error(request, f'Invalid date: {str(e)}')
        #     return redirect('citizen:register_baby')

        # birth_date = datetime.strptime(request.POST['birth_date'], '%Y-%m-%d').date()
        present_address = request.POST['present_address']
        permanent_address = request.POST['permanent_address']
        father_name = request.POST['fatherName']
        father_nid = request.POST['fatherNid']
        mother_name = request.POST['motherName']
        mother_nid = request.POST['motherNid']
        contact_number = request.POST['contact']
        relationship = request.POST['relationship']
        healthcare_id = request.session.get('healthcare_id')
        username = request.session.get('username')
        
        #print('_________________________________________________________________________________2')
        # print('birthdate: %s' % birth_date)
        try:
            # Create an Applicant instance
            
            #print('_________________________________________________________________________________3')
            applicant = Applicant(
                application_id=generate_application_id(),
                first_name=first_name,
                last_name=last_name,
                full_name=full_name,
                gender=gender,
                religion=religion,
                birth_country=birth_country,
                birth_division_id=birth_division_id,
                birth_district_id=birth_district_id,
                birth_subdistrict_id=birth_subdistrict_id,
                present_address=present_address,
                permanent_address=permanent_address,
                father_name=father_name,
                father_nid=father_nid,
                mother_name=mother_name,
                mother_nid=mother_nid,
                contact_number=contact_number,
                relationship=relationship,
                division_id=division_id,
                district_id=district_id,
                subdistrict_id=subdistrict_id,
                healthcare_id=healthcare_id,
                user_name=username,
                birth_date= birth_date
            )
            #print('_________________________________________________________________________________4')

            applicant.save()
            #print('_________________________________________________________________________________5')

            # Schedule vaccinations
            vaccines = Vaccine.objects.all()
            if vaccines.exists():
                for vaccine in vaccines:
                    time_intervals = ast.literal_eval(str(vaccine.time_intervals))
                    # time_intervals = vaccine.time_intervals.split(',')  # Split string into list
                    for dose in range(1, vaccine.doses + 1):
                        #print('_________________________________________________________________________________6')
                        # Calculate scheduled date for each dose
                        interval_days = int(time_intervals[dose - 1].strip())
                        #print('_________________________________________________________________________________7')
                        scheduled_date = birth_date + timedelta(days=interval_days)  # Now works with date object
                        #print('_________________________________________________________________________________8')
                        # Create v  accination schedule
                        schedule = VaccinationSchedule(
                            application_id=applicant.application_id,
                            vaccine_id=vaccine.id,
                            dose_number=dose,
                            scheduled_date=scheduled_date,
                            healthcare_id=healthcare_id,
                            status="Pending"
                        )
                        schedule.save()

            messages.success(request, 'Baby registered successfully and vaccinations scheduled!')
            

        except Exception as e:
            messages.error(request, f'Error registering baby: {str(e)}')
            print(f"Error in register_baby: {str(e)}")  # For debugging
            # return redirect('citizen:register_baby')

    # GET request - render form
    divisions = Division.objects.all()
    return render(request, 'citizen/register_baby.html', {
        'divisions': divisions,
        'division_id': request.session.get('division_id'),
        'district_id': request.session.get('district_id'),
        'subdistrict_id': request.session.get('subdistrict_id'),
        'healthcare_id': request.session.get('healthcare_id'),
    })
def generate_application_id():
    prefix = "BTD"
    # Fix datetime usage
    
    #print('_________________________________________________________________________________88')
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    #print('_________________________________________________________________________________99')
    
    random_number = random.randint(1000, 9999)
    return f"{prefix}{timestamp}{random_number}"

def load_districts(request):
    division_id = request.GET.get('division_id')
    districts = District.objects.filter(division_id=division_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)

def load_subdistricts(request):
    district_id = request.GET.get('district_id')
    subdistricts = Subdistrict.objects.filter(district_id=district_id).values('id', 'name')
    return JsonResponse(list(subdistricts), safe=False)

def load_healthcare_centers(request):
    subdistrict_id = request.GET.get('subdistrict_id')
    healthcare_centers = Healthcare.objects.filter(subdistrict__id=subdistrict_id).values('id', 'name')
    return JsonResponse(list(healthcare_centers), safe=False)

def notification(request):
    # Check if the user is logged in
    if 'citizen_id' not in request.session:
        return redirect('citizen:citizen_login')  # Redirect to login if not logged in

    # Get the username from the session
    username = request.session.get('username')

    # Fetch all applicants associated with the logged-in user
    applicants = Applicant.objects.filter(user_name=username)

    if request.method == 'POST':
        selected_applicant_id = request.POST.get('applicant')
        if selected_applicant_id:
            # Fetch vaccination schedule for the selected applicant
            vaccination_schedules = VaccinationSchedule.objects.filter(application_id=selected_applicant_id)

            # Fetch vaccine details for the vaccination schedules
            vaccine_details = []
            for schedule in vaccination_schedules:
                vaccine = Vaccine.objects.get(id=schedule.vaccine_id)
                vaccine_details.append({
                    'vaccine_id': vaccine.id,
                    'vaccine_name': vaccine.vaccine_name,
                    'dose_number': schedule.dose_number,
                    'scheduled_date': schedule.scheduled_date,
                    'status': schedule.status,
                })

            return render(request, 'citizen/notification.html', {
                'applicants': applicants,
                'vaccine_details': vaccine_details,
                'selected_applicant_id': selected_applicant_id,
                
            })
        else:
            messages.error(request, 'Please select an applicant.')

    return render(request, 'citizen/notification.html', {
        'applicants': applicants,
    })

def generate_birth_certificate(request):
    # Check if the user is logged in
    if 'citizen_id' not in request.session:
        return redirect('citizen:citizen_login')  # Redirect to login if not logged in

    # Get the username from the session
    username = request.session.get('username')
    
    # Fetch all applicants associated with the logged-in user
    applicants = Applicant.objects.filter(user_name=username)

    if request.method == 'POST':
        selected_applicant_id = request.POST.get('applicant')
        if selected_applicant_id:
            # Fetch vaccination schedules for the selected applicant
            vaccination_schedules = VaccinationSchedule.objects.filter(application_id=selected_applicant_id)

            # Check if all vaccinations are done
            all_done = all(schedule.status == "Done" for schedule in vaccination_schedules)

            if all_done:
                # Generate birth certificate data
                applicant = Applicant.objects.get(application_id=selected_applicant_id)
                return render(request, 'citizen/birth_certificate.html', {
                    'applicant': applicant,
                    'vaccination_schedules': vaccination_schedules,
                })
            else:
                messages.error(request, 'Please complete all vaccinations before generating the birth certificate.')
                return redirect('citizen:generate_birth_certificate')

    return render(request, 'citizen/generate_birth_certificate.html', {
        'applicants': applicants,
    })

def volunteer_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            volunteer = Volunteer.objects.get(email=email)
            # if check_password(password, volunteer.password):
            if (password==volunteer.password):
                request.session['volunteer_id'] = volunteer.id
                request.session['volunteer_name'] = volunteer.name
                request.session['volunteer_email'] = volunteer.email
                request.session['volunteer_healthcare'] = volunteer.healthcare
                request.session['volunteer_subdistrict_id'] = volunteer.subdistrict_id
                request.session['healthcare_id'] = volunteer.healthcare_id
                # messages.success(request, 'Login successful!')
                # print("xd")
                return redirect('citizen:volunteer_panel')
            else:
                messages.error(request, "Invalid email or password.")
                # print("fuck")
        except Volunteer.DoesNotExist:
            messages.error(request, "Invalid email or password.")
    return render(request, 'citizen/volenteer.html')


def volunteer_panel(request):
    if 'volunteer_id' not in request.session:
        return redirect('citizen:volunteer_login')  

    volunteer_id = request.session['volunteer_id']
    volunteer = Volunteer.objects.get(id=volunteer_id) 

    context = {
        'volunteer': volunteer,  # Pass the volunteer object directly
        'volunteer_name': volunteer.name,  # Also pass the name separately if needed
    }

    return render(request, 'citizen/volunteer_panel.html', context)
def volunteer_profile(request):
    if 'volunteer_id' not in request.session:
        return redirect('citizen:volunteer_login')
        
    volunteer = Volunteer.objects.get(id=request.session['volunteer_id'])
    healthcare = Healthcare.objects.get(id=volunteer.healthcare_id)
    subdistrict = Subdistrict.objects.get(id=volunteer.subdistrict_id)
    
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            
           
            if Volunteer.objects.filter(email=email).exclude(id=volunteer.id).exists():
                messages.error(request, 'Email already exists')
                return redirect('citizen:volunteer_profile')
            
            volunteer.name = name
            volunteer.email = email
            
            if current_password and new_password:
                if current_password == volunteer.password:
                    volunteer.password = new_password
                else:
                    messages.error(request, 'Current password is incorrect')
                    return redirect('citizen:volunteer_profile')
            
            volunteer.save()
            messages.success(request, 'Profile updated successfully')
            
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
            
    context = {
        'volunteer': volunteer,
        'healthcare': healthcare,
        'subdistrict': subdistrict
    }
    return render(request, 'citizen/volunteer_profile.html', context)
def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        try:
            # Check if an admin with this email and role exists
            admin = Admin.objects.get(email=email, role=role)
            
            # Verify the password
            # if check_password(password, admin.password):
            if (password==admin.password):
                # Store admin session details
                request.session['admin_id'] = admin.id
                request.session['admin_name'] = admin.name
                request.session['admin_role'] = admin.role
                request.session['district_id'] = admin.district_id
                request.session['division_id'] = admin.division_id
               
                # Redirect based on role
                if role == 'Division':
                    return redirect('/dashboard/divisional')
                elif role == 'District':
                  return redirect('citizen:district_dashboard') 
                elif role == 'Sub district':
                    return redirect('citizen:subdistrict_dashboard')
                elif role == 'Police':
                    return redirect('citizen:police_verification')
            else:
                messages.error(request, 'Invalid password. Please try again.')
        except Admin.DoesNotExist:
            messages.error(request, 'Invalid credentials or role. Please try again.')

    return render(request, 'citizen/admin_login.html')

def district_dashboard(request):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
    
    admin_id = request.session['admin_id']
    admin = Admin.objects.get(id=admin_id)
    subdistricts = Subdistrict.objects.all()

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        subdistrict_id = request.POST['subdistrict_id']
        
        
        if Admin.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists for another admin.')
        else:
          
            new_admin = Admin(
                name=name,
                email=email,
                password=password,
                role='Sub district',
                district_id=request.session['district_id'],
                division_id=request.session['division_id'],
                subdistrict_id=subdistrict_id
            )
            new_admin.save()
            messages.success(request, 'Subdistrict admin added successfully.')

        return redirect('citizen:district_dashboard')
    
    # Fetch all subdistrict admins
    subdistrict_admins = Admin.objects.filter(role='Sub district')

    for admin in subdistrict_admins:
        subdistrict = Subdistrict.objects.get(id=admin.subdistrict_id)
        admin.subdistrict_name = subdistrict.name 
    
    context = {
        'admin': admin,
        'subdistricts': subdistricts,
        'subdistrict_admins': subdistrict_admins
    }
    
    return render(request, 'citizen/district_admin.html', context)

def manage_police_admins(request):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
    
    admin = Admin.objects.get(id=request.session['admin_id'])
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            if Admin.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                new_police = Admin.objects.create(
                    name=name,
                    email=email,
                    password=password,
                    role='Police',
                    district_id=admin.district_id
                )
                
                # Send credentials via email
                if send_police_admin_credentials(name, email, password):
                    messages.success(request, 'Police admin added successfully. Login credentials sent to email.')
                else:
                    messages.warning(request, 'Police admin added but failed to send email notification.')
                    
        except Exception as e:
            messages.error(request, f'Error adding police admin: {str(e)}')
    
    police_admins = Admin.objects.filter(
        district_id=admin.district_id,
        role='Police'
    ).order_by('name')
    
    return render(request, 'citizen/manage_police.html', {
        'admin': admin,
        'police_admins': police_admins
    })

def edit_police_admin(request, admin_id):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
    
    district_admin = Admin.objects.get(id=request.session['admin_id'])
    if district_admin.role != 'District':
        messages.error(request, 'Unauthorized access')
        return redirect('citizen:admin_login')
    
    police_admin = get_object_or_404(Admin, id=admin_id, role='Police')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            if Admin.objects.filter(email=email).exclude(id=admin_id).exists():
                messages.error(request, 'Email already exists')
            else:
                police_admin.name = name
                police_admin.email = email
                if password:
                    police_admin.password = password
                police_admin.save()
                messages.success(request, 'Police admin updated successfully')
        except Exception as e:
            messages.error(request, f'Error updating police admin: {str(e)}')
    
    return redirect('citizen:manage_police_admins')

def delete_police_admin(request, admin_id):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
    
    district_admin = Admin.objects.get(id=request.session['admin_id'])
    if district_admin.role != 'District':
        messages.error(request, 'Unauthorized access')
        return redirect('citizen:admin_login')
    
    police_admin = get_object_or_404(Admin, id=admin_id, role='Police')
    
    try:
        police_admin.delete()
        messages.success(request, 'Police admin deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting police admin: {str(e)}')
    
    return redirect('citizen:manage_police_admins')
def subdistrict_dashboard(request):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')

    admin_id = request.session['admin_id']
    admin = Admin.objects.get(id=admin_id)
    
    # Get counts for the dashboard
    nid_applications = NIDApplicant.objects.filter(subdistrict_id=admin.subdistrict_id).count()
    healthcare_centers = Healthcare.objects.filter(subdistrict_id=admin.subdistrict_id).count()
    volunteers = Volunteer.objects.filter(subdistrict_id=admin.subdistrict_id).count()
    
    # Get recent applications
    recent_applications = NIDApplicant.objects.filter(subdistrict_id=admin.subdistrict_id).order_by('-id')[:5]
    
    context = {
        'admin': admin,
        'nid_applications': nid_applications,
        'healthcare_centers': healthcare_centers,
        'volunteers': volunteers,
        'recent_applications': recent_applications
    }

    return render(request, 'citizen/subdistrict_admin.html', context)
    
def add_healthcare_center(request):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
    
    admin_id = request.session['admin_id']
    admin = Admin.objects.get(id=admin_id)
    
    if request.method == 'POST':
        name = request.POST.get('healthcare_name')
        
        if not name:
            messages.error(request, 'Healthcare center name is required.')
            return render(request, 'citizen/add_healthcare_center.html', {'admin': admin})
        
        try:
            new_healthcare = Healthcare(
                name=name,
                subdistrict_id=admin.subdistrict_id
            )
            new_healthcare.save()
            messages.success(request, 'Healthcare center added successfully.')
            return render(request, 'citizen/add_healthcare_center.html', {'admin': admin})
            
        except Exception as e:
            messages.error(request, f'Error adding healthcare center: {str(e)}')
            return render(request, 'citizen/add_healthcare_center.html', {'admin': admin})
    
    return render(request, 'citizen/add_healthcare_center.html', {'admin': admin})

def view_healthcare(request):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
    
    admin_id = request.session['admin_id']
    admin = Admin.objects.get(id=admin_id)
    
    # Get search query
    search_query = request.GET.get('search', '')
    
    # Filter healthcare centers by subdistrict and search query
    healthcare_centers = Healthcare.objects.filter(subdistrict_id=admin.subdistrict_id)
    
    if search_query:
        healthcare_centers = healthcare_centers.filter(
            Q(name__icontains=search_query) |
            Q(subdistrict__name__icontains=search_query)
        )
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(healthcare_centers, 10)  # 10 items per page
    
    try:
        healthcare_centers = paginator.page(page)
    except:
        healthcare_centers = paginator.page(1)
    
    context = {
        'healthcare_centers': healthcare_centers,
        'admin': admin,
        'search_query': search_query
    }
    
    return render(request, 'citizen/view_healthcare.html', context)

def edit_healthcare(request, center_id):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
    
    healthcare = get_object_or_404(Healthcare, id=center_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            try:
                healthcare.name = name
                healthcare.save()
                messages.success(request, 'Healthcare center updated successfully.')
            except Exception as e:
                messages.error(request, f'Error updating healthcare center: {str(e)}')
        else:
            messages.error(request, 'Healthcare center name is required.')
    
    return redirect('citizen:view_healthcare')

def delete_healthcare(request, center_id):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
    
    healthcare = get_object_or_404(Healthcare, id=center_id)
    
    try:
        # First update all related applicants to set healthcare_id to NULL
        Applicant.objects.filter(healthcare_id=center_id).update(healthcare_id=None)
        
        # Then delete the healthcare center
        healthcare.delete()
        messages.success(request, 'Healthcare center and related records updated successfully.')
    except Exception as e:
        messages.error(request, f'Error deleting healthcare center: {str(e)}')
    
    return redirect('citizen:view_healthcare')

def manage_volunteers(request):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
    
    admin_id = request.session['admin_id']
    admin = Admin.objects.get(id=admin_id)
    
    # Get search query
    search_query = request.GET.get('search', '')
    
    # Filter volunteers by subdistrict and search query
    volunteers = Volunteer.objects.filter(subdistrict_id=admin.subdistrict_id)
    
    if search_query:
        volunteers = volunteers.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(healthcare__icontains=search_query)
        )
    
    # Get healthcare centers for the subdistrict
    healthcare_centers = Healthcare.objects.filter(subdistrict_id=admin.subdistrict_id)
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(volunteers, 9)  # 9 items per page (3x3 grid)
    
    try:
        volunteers = paginator.page(page)
    except:
        volunteers = paginator.page(1)
    
    context = {
        'volunteers': volunteers,
        'healthcare_centers': healthcare_centers,
        'admin': admin,
        'search_query': search_query
    }
    
    return render(request, 'citizen/manage_volunteer.html', context)

def add_volunteer(request):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        healthcare_id = request.POST.get('healthcare_id')
        
        try:
            # Check if email already exists
            if Volunteer.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('citizen:manage_volunteers')
            
            # Get healthcare center
            healthcare = Healthcare.objects.get(id=healthcare_id)
            
            # Create new volunteer
            volunteer = Volunteer(
                name=name,
                email=email,
                password=password,  # Consider hashing the password
                healthcare=healthcare.name,
                healthcare_id=healthcare_id,
                subdistrict_id=healthcare.subdistrict_id
            )
            volunteer.save()
            messages.success(request, 'Volunteer added successfully')
            
        except Exception as e:
            messages.error(request, f'Error adding volunteer: {str(e)}')
    
    return redirect('citizen:manage_volunteers')

def edit_volunteer(request, volunteer_id):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
    
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        healthcare_id = request.POST.get('healthcare_id')
        
        try:
            # Check if email exists for other volunteers
            if Volunteer.objects.filter(email=email).exclude(id=volunteer_id).exists():
                messages.error(request, 'Email already exists')
                return redirect('citizen:manage_volunteers')
            
            # Get healthcare center
            healthcare = Healthcare.objects.get(id=healthcare_id)
            
            # Update volunteer
            volunteer.name = name
            volunteer.email = email
            if password:  # Update password only if provided
                volunteer.password = password  # Consider hashing the password
            volunteer.healthcare = healthcare.name
            volunteer.healthcare_id = healthcare_id
            volunteer.subdistrict_id = healthcare.subdistrict_id
            
            volunteer.save()
            messages.success(request, 'Volunteer updated successfully')
            
        except Exception as e:
            messages.error(request, f'Error updating volunteer: {str(e)}')
    
    return redirect('citizen:manage_volunteers')

def delete_volunteer(request, volunteer_id):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
    
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)
    
    try:
        # Check if volunteer has any active assignments
        if VaccinationSchedule.objects.filter(volunteer_id=volunteer_id, status='Pending').exists():
            messages.error(request, 'Cannot delete volunteer with pending vaccinations')
            return redirect('citizen:manage_volunteers')
        
        volunteer.delete()
        messages.success(request, 'Volunteer deleted successfully')
        
    except Exception as e:
        messages.error(request, f'Error deleting volunteer: {str(e)}')
    
    return redirect('citizen:manage_volunteers')

def police_verification(request):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
        
    admin = Admin.objects.get(id=request.session['admin_id'])
    # if admin.role != 'District':
    #     messages.error(request, 'Unauthorized access')
    #     return redirect('citizen:admin_login')
    
    # Get applications with completed payment
    applications = PassportApplicant.objects.filter(
        payment_status='paid',
        present_district_id=admin.district_id
    ).order_by('-created_at')
    
    context = {
        'applications': applications,
        'admin': admin
    }
    return render(request, 'citizen/police_verification.html', context)
def police_change_password(request):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
    
    admin = Admin.objects.get(id=request.session['admin_id'])
    if admin.role != 'Police':
        messages.error(request, 'Unauthorized access')
        return redirect('citizen:admin_login')
    
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if current_password != admin.password:
            messages.error(request, 'Current password is incorrect')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match')
        else:
            try:
                admin.password = new_password
                admin.save()
                messages.success(request, 'Password updated successfully')
                return redirect('citizen:police_verification')
            except Exception as e:
                messages.error(request, f'Error updating password: {str(e)}')
    
    return render(request, 'citizen/police_change_password.html', {'admin': admin})
def get_applicant_details(request, tracking_number):
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    try:
        applicant = PassportApplicant.objects.get(tracking_number=tracking_number)
        data = {
            'name_en': applicant.name_en,
            'name_bn': applicant.name_bn,
            'father_name': applicant.father_name,
            'mother_name': applicant.mother_name,
            'birth_date': applicant.birth_date.strftime('%d %b %Y'),
            'birth_place': applicant.birth_place,
            'gender': applicant.gender,
            'marital_status': applicant.marital_status,
            'nid_number': applicant.nid_number,
            'present_address': applicant.present_address,
            'permanent_address': applicant.permanent_address,
            'phone': applicant.phone,
            'email': applicant.email,
            'tracking_number': applicant.tracking_number,
            'passport_type': applicant.passport_type,
            'application_date': applicant.created_at.strftime('%d %b %Y'),
            'payment_status': applicant.payment_status
        }
        return JsonResponse(data)
    except PassportApplicant.DoesNotExist:
        return JsonResponse({'error': 'Applicant not found'}, status=404)

def update_verification(request):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
        
    tracking_number = request.POST.get('tracking_number')
    try:
        application = PassportApplicant.objects.get(tracking_number=tracking_number)
        
        # Update verification details
        application.police_verification_status = request.POST.get('verification_status')
        application.police_verification_date = timezone.now()
        application.police_station = request.POST.get('police_station')
        application.police_officer = request.POST.get('police_officer')
        application.criminal_records_found = 'criminal_records' in request.POST
        application.address_verified = 'address_verified' in request.POST
        application.police_comments = request.POST.get('police_comments')
        
        application.save()
        
        # Send email notification
        try:
            send_verification_status_email(application)
            messages.success(request, 'Verification status updated and notification sent successfully')
        except Exception as e:
            messages.warning(request, f'Verification updated but failed to send email: {str(e)}')
        
    except PassportApplicant.DoesNotExist:
        messages.error(request, 'Application not found')
    except Exception as e:
        messages.error(request, f'Error updating verification: {str(e)}')
    
    return redirect('citizen:police_verification')

def passport_verification(request):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
        
    admin = Admin.objects.get(id=request.session['admin_id'])
    
    # Get eligible applications
    eligible_applications = PassportApplicant.objects.filter(
        payment_status='paid',
        police_verification_status='verified',
        criminal_records_found=False,
        present_district_id=admin.district_id
    )
    
    # Create verification records if they don't exist
    for application in eligible_applications:
        PassportVerification.objects.get_or_create(
            application=application
        )
    
    verifications = PassportVerification.objects.filter(
        application__present_district_id=admin.district_id,
        passport_number__isnull=True
    ).select_related('application')
    
    context = {
        'verifications': verifications,
        'admin': admin
    }
    return render(request, 'citizen/passport_verify.html', context)

def update_passport_verification(request, verification_id):
    if request.method != 'POST' or 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
        
    try:
        verification_type = request.POST.get('type')
        verification = PassportVerification.objects.get(id=verification_id)
        
        if verification_type == 'fingerprint':
            verification.fingerprint_status = 'completed'
        elif verification_type == 'face':
            verification.face_status = 'completed'
            
        verification.save()
        messages.success(request, f'{verification_type.title()} verification completed')
        
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        
    return redirect('citizen:passport_verification')

def generate_passport(request, verification_id):
    if request.method != 'POST' or 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
        
    try:
        verification = PassportVerification.objects.get(id=verification_id)
        
        if verification.fingerprint_status != 'completed' or verification.face_status != 'completed':
            messages.error(request, 'Complete both fingerprint and face verification first')
            return redirect('citizen:passport_verification')
            
        passport_number = PassportVerification.generate_passport_number(
            verification.application.birth_date
        )
        verification.passport_number = passport_number
        verification.verification_status = 'verified'
        verification.verification_date = timezone.now()
        verification.save()
        
        # Send email notification
        send_passport_number_email(verification)
        
        messages.success(request, f'Passport generated successfully: {passport_number}')
        
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        
    return redirect('citizen:passport_verification')

def print_passport_list(request):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
        
    admin = Admin.objects.get(id=request.session['admin_id'])
    
    verifications = PassportVerification.objects.filter(
        verification_status='verified',
        print_status='pending',
        application__present_district_id=admin.district_id
    ).select_related('application')
    
    context = {
        'verifications': verifications,
        'admin': admin
    }
    return render(request, 'citizen/print_passport.html', context)

def mark_passport_printed(request, verification_id):
    if request.method != 'POST' or 'admin_id' not in request.session:
        return JsonResponse({'success': False})
        
    try:
            verification = PassportVerification.objects.get(id=verification_id)
            verification.is_printed = True
            verification.print_date = timezone.now()
            verification.save()
            return JsonResponse({'success': True})
    except PassportVerification.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Verification not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def generate_passport_pdf(request, verification_id):
    verification = get_object_or_404(PassportVerification, id=verification_id)
    
    # Render passport template to HTML
    html_string = render_to_string('citizen/passport_template.html', {
        'verification': verification,
        'application': verification.application
    })
    
    # Convert HTML to PDF using pdfkit
    pdf = pdfkit.from_string(html_string, False)
    
    # Create HTTP response with PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=passport_{verification.passport_number}.pdf'
    return response

def get_passport_data(request, verification_id):
    if 'admin_id' not in request.session:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    try:
        verification = PassportVerification.objects.select_related('application').get(id=verification_id)
        data = {
            'passport_number': verification.passport_number,
            'application': {
                'name_en': verification.application.name_en,
                'birth_date': verification.application.birth_date.strftime('%d %b %Y'),
                'birth_place': verification.application.birth_place,
            },
            'verification_date': verification.verification_date.strftime('%d %b %Y'),
            'expiry_date': verification.expiry_date.strftime('%d %b %Y'),
        }
        return JsonResponse(data)
    except PassportVerification.DoesNotExist:
        return JsonResponse({'error': 'Verification not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def show_passport(request, verification_id):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
        
    verification = get_object_or_404(PassportVerification, id=verification_id)
    
    return render(request, 'citizen/show_passport.html', {
        'verification': verification
    })
def view_reports(request):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')

    admin_id = request.session['admin_id']
    admin = Admin.objects.get(id=admin_id)

    # Get date ranges
    today = timezone.now().date()
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)

    # NID Application Statistics
    nid_stats = {
        'total': NIDApplicant.objects.filter(subdistrict_id=admin.subdistrict_id).count(),
        'pending': NIDApplicant.objects.filter(subdistrict_id=admin.subdistrict_id, status='pending').count(),
        'approved': NIDApplicant.objects.filter(subdistrict_id=admin.subdistrict_id, status='approved').count(),
        'rejected': NIDApplicant.objects.filter(subdistrict_id=admin.subdistrict_id, status='rejected').count()
    }

    # Monthly Reports Statistics by Healthcare Center
    healthcare_centers = Healthcare.objects.filter(subdistrict_id=admin.subdistrict_id)
    monthly_stats = []
    
    for center in healthcare_centers:
        current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        report = MonthlyReport.objects.filter(
            healthcare_center=center,
            month__year=current_month.year,
            month__month=current_month.month
        ).first()

        monthly_stats.append({
            'name': center.name,
            'births': report.births if report else 0,
            'vaccinations': report.vaccinations if report else 0,
            'deaths': report.deaths if report else 0
        })

    # Yearly Statistics
    yearly_stats = []
    current_year = timezone.now().year
    for month in range(1, 13):
        month_data = MonthlyReport.objects.filter(
            healthcare_center__subdistrict_id=admin.subdistrict_id,
            month__year=current_year,
            month__month=month
        ).aggregate(
            total_births=Sum('births'),
            total_vaccinations=Sum('vaccinations'),
            total_deaths=Sum('deaths')
        )
        
        yearly_stats.append({
            'month': datetime(2000, month, 1).strftime('%B'),
            'births': month_data['total_births'] or 0,
            'vaccinations': month_data['total_vaccinations'] or 0,
            'deaths': month_data['total_deaths'] or 0
        })

    context = {
        'admin': admin,
        'nid_stats': json.dumps(nid_stats),
        'monthly_stats': json.dumps(monthly_stats),
        'yearly_stats': json.dumps(yearly_stats),
        'total_applications': nid_stats['total'],
        'total_births': sum(stat['births'] for stat in monthly_stats),
        'total_vaccinations': sum(stat['vaccinations'] for stat in monthly_stats),
        'healthcare_centers_count': healthcare_centers.count()
    }

    return render(request, 'citizen/view_reports.html', context)
# views.py
def district_reports(request):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')

    admin = Admin.objects.get(id=request.session['admin_id'])

    # Get subdistricts under this district
    subdistricts = Subdistrict.objects.filter(district_id=admin.district_id)
    
    # Healthcare and volunteer stats
    healthcare_stats = []
    for subdistrict in subdistricts:
        healthcare_centers = Healthcare.objects.filter(subdistrict=subdistrict)
        for center in healthcare_centers:
            volunteer_count = Volunteer.objects.filter(healthcare=center.name).count()
            healthcare_stats.append({
                'name': center.name,
                'volunteers': volunteer_count
            })

    # Passport application stats
    passport_stats = {
        'total': PassportApplicant.objects.filter(present_district_id=admin.district_id).count(),
        'police_verified': PassportApplicant.objects.filter(
            present_district_id=admin.district_id,
            police_verification_status='verified'
        ).count(),
        'printed': PassportVerification.objects.filter(
            application__present_district_id=admin.district_id,
            print_status='printed'
        ).count()
    }

    # Subdistrict stats
    subdistrict_stats = []
    for subdistrict in subdistricts:
        subdistrict_stats.append({
            'name': subdistrict.name,
            'passport_count': PassportApplicant.objects.filter(present_subdistrict=subdistrict).count(),
            'healthcare_count': Healthcare.objects.filter(subdistrict=subdistrict).count(),
            'volunteer_count': Volunteer.objects.filter(subdistrict_id=subdistrict.id).count()
        })

    context = {
        'admin': admin,
        'healthcare_stats': json.dumps(healthcare_stats),
        'passport_stats': json.dumps(passport_stats),
        'subdistrict_stats': json.dumps(subdistrict_stats)
    }

    return render(request, 'citizen/district_reports.html', context)

def manage_subdistrict_admins(request):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
    
    admin = Admin.objects.get(id=request.session['admin_id'])
    
    subdistrict_admins = Admin.objects.filter(
        district_id=admin.district_id,
        role='Sub district'
    )
    
    # Get subdistricts for dropdown
    subdistricts = Subdistrict.objects.filter(district_id=admin.district_id)
    
    context = {
        'admin': admin,
        'subdistrict_admins': subdistrict_admins,
        'subdistricts': subdistricts
    }
    return render(request, 'citizen/manage_subdistrict_admins.html', context)
def edit_subdistrict_admin(request, admin_id):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
        
    subdistrict_admin = get_object_or_404(Admin, id=admin_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subdistrict_id = request.POST.get('subdistrict_id')
        
        try:
            # Check if email exists for other admins
            if Admin.objects.filter(email=email).exclude(id=admin_id).exists():
                messages.error(request, 'Email already exists')
                return redirect('citizen:manage_subdistrict_admins')
            
            subdistrict_admin.name = name
            subdistrict_admin.email = email
            subdistrict_admin.subdistrict_id = subdistrict_id
            subdistrict_admin.save()
            
            messages.success(request, 'Admin updated successfully')
            
        except Exception as e:
            messages.error(request, f'Error updating admin: {str(e)}')
    
    return redirect('citizen:manage_subdistrict_admins')

def delete_subdistrict_admin(request, admin_id):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
        
    subdistrict_admin = get_object_or_404(Admin, id=admin_id)
    
    try:
        subdistrict_admin.delete()
        messages.success(request, 'Admin deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting admin: {str(e)}')
    
    return redirect('citizen:manage_subdistrict_admins')
def process_payment(request, tracking_number):
    if 'citizen_id' not in request.session:
        return redirect('citizen:citizen_login')
        
    if request.method == 'POST':
        try:
            application = PassportApplicant.objects.get(tracking_number=tracking_number)
            payment_method = request.POST.get('payment_method')
            
            # Update payment status
            application.payment_status = 'paid'
            application.payment_method = payment_method
            application.payment_date = timezone.now()
            
            # Set amount based on passport type
            application.payment_amount = 5500 if application.passport_type else 3500
            
            application.save()
            
            messages.success(request, 'Payment processed successfully')
            
        except PassportApplicant.DoesNotExist:
            messages.error(request, 'Application not found')
        except Exception as e:
            messages.error(request, f'Error processing payment: {str(e)}')
            
    return redirect('citizen:pay_fees')
def update_vaccine(request):
    if 'volunteer_id' not in request.session:
        return redirect('citizen:volunteer_login')
        
    volunteer = Volunteer.objects.get(id=request.session['volunteer_id'])
    searched_baby = None
    vaccination_schedule = None
    
    if request.method == 'POST':
        if 'search' in request.POST:
            application_id = request.POST.get('application_id')
            try:
                # Get baby details
                searched_baby = Applicant.objects.get(
                    application_id=application_id,  
                    healthcare_id=volunteer.healthcare_id
                )
                
                # Get vaccination schedule with vaccine names
                vaccination_schedule = VaccinationSchedule.objects.filter(
                    application_id=application_id
                ).order_by('scheduled_date')
                
                # Get vaccine names
                for schedule in vaccination_schedule:
                    schedule.vaccine_name = Vaccine.objects.get(
                        id=schedule.vaccine_id
                    ).vaccine_name
                    
            except Applicant.DoesNotExist:
                messages.error(request, 'Baby not found or not registered in your healthcare center')
                return render(request, 'citizen/update_vaccine.html', {
                    'volunteer': volunteer
                })
                
        elif 'update_status' in request.POST:
            schedule_id = request.POST.get('schedule_id')
            new_status = request.POST.get('status')
            
            try:
                schedule = VaccinationSchedule.objects.get(id=schedule_id)

                if schedule.status == 'Done':
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Vaccine has already been given'
                    })

                # Update the status without date checking
                schedule.status = new_status
                if new_status == 'Done':
                    schedule.volunteer_id = volunteer.id
                    schedule.given_date = timezone.now()
                schedule.save()
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Vaccination status updated successfully'
                })

            except VaccinationSchedule.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Schedule not found'
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'error', 
                    'message': str(e)
                })

    context = {
        'volunteer': volunteer,
        'searched_baby': searched_baby,
        'vaccination_schedule': vaccination_schedule
    }
    return render(request, 'citizen/update_vaccine.html', context)

def monthly_report(request):
    if 'volunteer_id' not in request.session:
        return redirect('citizen:volunteer_login')
        
    volunteer = Volunteer.objects.get(id=request.session['volunteer_id'])
    
    if request.method == 'POST':
        try:
            # Check if report already exists for this month
            current_month = datetime.now().replace(day=1)
            existing_report = MonthlyReport.objects.filter(
                volunteer=volunteer,
                month=current_month
            ).exists()
            
            if existing_report:
                messages.error(request, 'Report for this month already submitted')
                return redirect('citizen:monthly_report')
            
            # Create new report using volunteer's healthcare_id
            report = MonthlyReport(
                volunteer=volunteer,
                healthcare_center_id=Volunteer.healthcare_id,  # Use volunteer instance
                subdistrict_id=Volunteer.subdistrict_id,
                month=current_month,
                births=request.POST.get('births'),
                vaccinations=request.POST.get('vaccinations'),
                deaths=request.POST.get('deaths'),
                notes=request.POST.get('notes')
            )
            report.save()
            messages.success(request, 'Monthly report submitted successfully')
            return redirect('citizen:volunteer_panel')
            
        except Exception as e:
            messages.error(request, f'Error submitting report: {str(e)}')
    
    context = {
        'volunteer': volunteer,
        'current_month': datetime.now().strftime('%B %Y'),
        'healthcare_name': volunteer.healthcare  # Use volunteer instance attribute
    }
    return render(request, 'citizen/monthly_report.html', context)

def manage_vaccines(request):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
    
    admin = Admin.objects.get(id=request.session['admin_id'])
    vaccines = Vaccine.objects.all().order_by('vaccine_name')
    
    context = {
        'admin': admin,
        'vaccines': vaccines
    }
    return render(request, 'citizen/manage_vaccines.html', context)

def add_vaccine(request):
    if 'admin_id' not in request.session:
        return JsonResponse({'success': False, 'error': 'Unauthorized'})
    
    if request.method == 'POST':
        try:
            vaccine_data = {
                'vaccine_name': request.POST.get('vaccine_name'),
                'vaccine_code': request.POST.get('vaccine_code'),
                'doses': request.POST.get('doses'),
                'time_intervals': request.POST.getlist('intervals[]'),
                'manufactured_country': request.POST.get('manufactured_country'),
                'disease': request.POST.get('disease'),
                'storage_temperature': request.POST.get('storage_temperature')
            }
            
            vaccine = Vaccine.objects.create(**vaccine_data)
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def edit_vaccine(request, vaccine_id):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
        
    try:
        vaccine = Vaccine.objects.get(id=vaccine_id)
        
        if request.method == 'POST':
            vaccine.vaccine_name = request.POST.get('vaccine_name')
            vaccine.vaccine_code = request.POST.get('vaccine_code')
            vaccine.doses = request.POST.get('doses')
            vaccine.time_intervals = request.POST.getlist('intervals[]')
            vaccine.manufactured_country = request.POST.get('manufactured_country')
            vaccine.disease = request.POST.get('disease')
            vaccine.storage_temperature = request.POST.get('storage_temperature')
            vaccine.save()
            
            messages.success(request, 'Vaccine updated successfully')
            return redirect('citizen:manage_vaccines')
            
    except Vaccine.DoesNotExist:
        messages.error(request, 'Vaccine not found')
    except Exception as e:
        messages.error(request, f'Error updating vaccine: {str(e)}')
        
    return redirect('citizen:manage_vaccines')

def delete_vaccine(request, vaccine_id):
    if 'admin_id' not in request.session:
        return redirect('citizen:admin_login')
        
    try:
        vaccine = Vaccine.objects.get(id=vaccine_id)
        vaccine.delete()
        messages.success(request, 'Vaccine deleted successfully')
    except Vaccine.DoesNotExist:
        messages.error(request, 'Vaccine not found')
    except Exception as e:
        messages.error(request, f'Error deleting vaccine: {str(e)}')
        
    return redirect('citizen:manage_vaccines')
def get_vaccine(request, vaccine_id):
    if 'admin_id' not in request.session:
        return JsonResponse({'success': False, 'error': 'Unauthorized'})
        
    try:
        vaccine = Vaccine.objects.get(id=vaccine_id)
        data = {
            'success': True,
            'vaccine': {
                'vaccine_name': vaccine.vaccine_name,
                'vaccine_code': vaccine.vaccine_code,
                'doses': vaccine.doses,
                'manufactured_country': vaccine.manufactured_country,
                'disease': vaccine.disease,
                'storage_temperature': vaccine.storage_temperature,
                'time_intervals': vaccine.time_intervals
            }
        }
        return JsonResponse(data)
    except Vaccine.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Vaccine not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
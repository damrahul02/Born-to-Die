from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from datetime import date, timedelta,datetime
from django.conf import settings



class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)    
    division_id = models.IntegerField(null=True, blank=True)
    district_id = models.IntegerField(null=True, blank=True)
    subdistrict_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)
    role = models.CharField(
        max_length=255,
        choices=[
            ('Division', 'Division'),
            ('District', 'District'),
            ('Sub district', 'Sub district'),
            ('Police', 'Police') 
        ]
    )
 
    class Meta:
        db_table = 'admins'


class Applicant(models.Model):
    application_id = models.CharField(max_length=100, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=510)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    religion = models.CharField(max_length=255)
    birth_country = models.CharField(max_length=255, null=True, blank=True)
    birth_division_id = models.IntegerField()
    birth_district_id = models.IntegerField()
    birth_subdistrict_id = models.IntegerField()
    birth_date = models.DateField(null=True, blank=True)
    present_address = models.TextField()
    permanent_address = models.TextField()
    father_name = models.CharField(max_length=255)
    father_nid = models.CharField(max_length=20)
    mother_name = models.CharField(max_length=255)
    mother_nid = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=20)
    relationship = models.CharField(max_length=10, choices=[('mother', 'mother'), ('father', 'father'), ('brother', 'brother'), ('sister', 'sister')])
    division_id = models.IntegerField(null=True, blank=True)
    district_id = models.IntegerField(null=True, blank=True)
    subdistrict_id = models.IntegerField(null=True, blank=True)
    healthcare_id = models.IntegerField(null=True, blank=True)
    application_time = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'applicants'


class BabyReg(models.Model):
    reg_no = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    birth = models.CharField(max_length=20, null=True, blank=True)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    father_nid = models.CharField(max_length=255, null=True, blank=True)
    mother_name = models.CharField(max_length=255, null=True, blank=True)
    mother_nid = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    vaccine_centre = models.CharField(max_length=255, null=True, blank=True)
    user_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'baby_reg'


class Citizen(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    email = models.EmailField(null=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    father_nid = models.CharField(max_length=255, null=True, blank=True)
    mother_name = models.CharField(max_length=255, null=True, blank=True)
    mother_nid = models.CharField(max_length=255, null=True, blank=True)
    present_division = models.CharField(max_length=255, null=True, blank=True)
    present_district = models.CharField(max_length=255, null=True, blank=True)
    present_upazila = models.CharField(max_length=255, null=True, blank=True)
    permanent_division = models.CharField(max_length=255, null=True, blank=True)
    permanent_district = models.CharField(max_length=255, null=True, blank=True)
    permanent_upazila = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        db_table = 'citizen'


class District(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    division = models.ForeignKey('Division', on_delete=models.CASCADE, null=True,default=None)

    class Meta:
        db_table = 'districts'

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name


class Division(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(null=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'divisions'


class Healthcare(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    # healthcare = models.CharField(null=True,max_length=500)
    subdistrict = models.ForeignKey('Subdistrict', on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'healthcare'


class Subdistrict(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    district = models.ForeignKey('District', on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'subdistricts'


class VaccinationSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    application_id = models.CharField(max_length=100)
    vaccine_id = models.IntegerField()
    dose_number = models.IntegerField(null=True)
    scheduled_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=255, default='Scheduled')
    healthcare_id = models.IntegerField()
    volunteer_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'vaccination_schedule'


class Vaccine(models.Model):
    id = models.AutoField(primary_key=True)
    vaccine_name = models.CharField(max_length=255,default="none")
    vaccine_code = models.CharField(max_length=100, unique=True)
    doses = models.IntegerField(null=True)
    time_intervals = models.JSONField(null=True)
    manufactured_country = models.CharField(max_length=255, null=True, blank=True)
    disease = models.CharField(max_length=255, null=True, blank=True)
    storage_temperature = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vaccine'


class VaccineStatus(models.Model):
    application_id = models.CharField(max_length=100, primary_key=True)
    status = models.CharField(max_length=255)

    class Meta:
        db_table = 'vaccine_status'


class Volunteer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    healthcare = models.CharField(max_length=255,null=True)
    password = models.CharField(max_length=255, default='default_password')
    subdistrict_id = models.IntegerField(null=True)
    healthcare_id = models.IntegerField(null=True)

    class Meta:
        db_table = 'volunteers'


class NIDApplicant(models.Model):
    name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    father_nid = models.CharField(max_length=50, null=True, blank=True)
    mother_name = models.CharField(max_length=255)
    mother_nid = models.CharField(max_length=50, null=True, blank=True)
    husband_name = models.CharField(max_length=255, null=True, blank=True)
    wife_name = models.CharField(max_length=255, null=True, blank=True)
    birth_id = models.CharField(max_length=50)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    marital_status = models.CharField(
        max_length=15,
        choices=[('Married', 'Married'), ('Unmarried', 'Unmarried'), ('Widowed', 'Widowed'), ('Divorced', 'Divorced')]
    )
    occupation = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    blood_group = models.CharField(
        max_length=5,
        choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')]
    )
    subdistrict = models.ForeignKey(Subdistrict, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='pending')
    academic_certificate = models.FileField(
        upload_to='academic_certificates/',
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf'])
        ],
        db_column='academic_certificate'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.academic_certificate:
            if self.academic_certificate.size > 5242880:  # 5MB limit
                raise ValidationError('File size must be under 5MB')

    class Meta:
        db_table = 'nid_applicant'
        ordering = ['-created_at']


class NIDVerification(models.Model):
    user_id = models.CharField(max_length=11, unique=True)  # Format: BTD + 8 digits
    name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    blood_group = models.CharField(max_length=5)
    verification_date = models.DateField()
    fingerprint_status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('completed', 'Completed')],
        default='pending'
    )
    face_status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('completed', 'Completed')],
        default='pending'
    )
    face_photo = models.ImageField(
        upload_to='nid_faces/',
        null=True,
        blank=True,
        verbose_name='Face Photo'
    )
    nid_number = models.CharField(max_length=17, unique=True, null=True, blank=True)
    verification_status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('verified', 'Verified')],
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'nid_verification'

    @staticmethod
    def generate_user_id():
        # Get count of existing records and add 1
        count = NIDVerification.objects.count() + 1
        # Create unique 8-digit number
        unique_part = f"{count:08d}"
        return f"BTD{unique_part}"

    @staticmethod
    def generate_nid_number(birth_date):
        date_part = birth_date.strftime('%Y%m%d')
        count = NIDVerification.objects.filter(
            nid_number__startswith=date_part
        ).count() + 1
        unique_part = f"{count:08d}"
        return f"{date_part}{unique_part}"


class PassportApplicant(models.Model):
    id = models.AutoField(primary_key=True)
    citizen_id = models.IntegerField(null=True)
    name_en = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    father_nationality = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=255)
    mother_nationality = models.CharField(max_length=100)
    spouse_name = models.CharField(max_length=255, null=True, blank=True)
    spouse_nationality = models.CharField(max_length=100, null=True, blank=True)
    nid_number = models.CharField(max_length=20, unique=True)
    birth_certificate_number = models.CharField(max_length=20)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=255)
    birth_country = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    marital_status = models.CharField(max_length=10)
    profession = models.CharField(max_length=100)
    
    present_address = models.TextField()
    present_district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='present_passport_applications')
    present_subdistrict = models.ForeignKey(Subdistrict, on_delete=models.CASCADE, related_name='present_passport_applications')
    permanent_address = models.TextField()
    permanent_district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='permanent_passport_applications')
    permanent_subdistrict = models.ForeignKey(Subdistrict, on_delete=models.CASCADE, related_name='permanent_passport_applications')
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    
    PASSPORT_TYPE_CHOICES = [
        ('regular', 'Regular'),
        ('official', 'Official'),
        ('diplomatic', 'Diplomatic'),
    ]
    
    DELIVERY_TYPE_CHOICES = [
        ('regular', 'Regular'),
        ('urgent', 'Urgent'),
    ]
    
    passport_type = models.CharField(max_length=10, choices=PASSPORT_TYPE_CHOICES)
    page_type = models.CharField(max_length=2)
    delivery_type = models.CharField(max_length=10, choices=DELIVERY_TYPE_CHOICES)
    application_status = models.CharField(max_length=30, default='pending')
    tracking_number = models.CharField(max_length=20, unique=True, null=True)
    
    old_passport_number = models.CharField(max_length=20, null=True, blank=True)
    old_passport_issue_date = models.DateField(null=True, blank=True)
    old_passport_expiry_date = models.DateField(null=True, blank=True)
    
    nid_scan = models.CharField(max_length=255)
    birth_certificate_scan = models.CharField(max_length=255)
    old_passport_scan = models.CharField(max_length=255, null=True, blank=True)
    
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('paid', 'Paid'),
            ('failed', 'Failed')
        ],
        default='pending'
    )    
    payment_date = models.DateTimeField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    
    # Police Verification Fields
    police_verification_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected')
    ], default='pending')
    police_verification_date = models.DateTimeField(null=True, blank=True)
    police_station = models.CharField(max_length=255, null=True, blank=True)
    police_officer = models.CharField(max_length=255, null=True, blank=True)
    criminal_records_found = models.BooleanField(default=False)
    address_verified = models.BooleanField(default=False)
    police_comments = models.TextField(null=True, blank=True)
    
    payment_method = models.CharField(max_length=20, null=True, blank=True)
    card_number = models.CharField(max_length=20, null=True, blank=True)
    bkash_number = models.CharField(max_length=15, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'passport_applicant'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name_en} - {self.tracking_number}"

    def save(self, *args, **kwargs):
        # Generate tracking number for new applications
        if not self.tracking_number and not self.id:
            last_application = PassportApplicant.objects.order_by('id').last()
            if last_application:
                last_number = int(last_application.tracking_number[3:])
                new_number = last_number + 1
            else:
                new_number = 1
            self.tracking_number = f'BTD{str(new_number).zfill(8)}'

        # Handle payment date
        if self.payment_date and isinstance(self.payment_date, str):
            self.payment_date = timezone.now()

        super().save(*args, **kwargs)

    @classmethod
    def get_user_applications(cls, citizen_id):
        return cls.objects.filter(citizen_id=citizen_id).order_by('-created_at')

    def belongs_to_user(self, citizen_id):
        return self.citizen_id == citizen_id


class PassportVerification(models.Model):
    passport_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    application = models.ForeignKey(PassportApplicant, on_delete=models.CASCADE)
    fingerprint_status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('completed', 'Completed')],
        default='pending',
        db_column='fingerprint_status'
    )
    face_status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('completed', 'Completed')],
        default='pending',
        db_column='face_status'
    )
    face_photo = models.ImageField(
        upload_to='passport_faces/',
        null=True,
        blank=True,
        verbose_name='Face Photo'
    )
    verification_status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('verified', 'Verified')],
        default='pending',
        db_column='verification_status'
    )
    print_status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('printed', 'Printed')],
        default='pending'
    )
    verification_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'passport_verification'

    @staticmethod
    def generate_passport_number(birth_date):
        """Generate unique passport number"""
        date_part = birth_date.strftime('%Y%m')
        count = PassportVerification.objects.filter(
            passport_number__startswith=f"BD{date_part}"
        ).count() + 1
        return f"BD{date_part}{str(count).zfill(6)}"

    @property
    def expiry_date(self):
        """Return expiry date (10 years from verification date)"""
        if self.verification_date:
            try:
                return self.verification_date.replace(year=self.verification_date.year + 10)
            except ValueError:
                return self.verification_date + timedelta(days=3650)
        return None
class MonthlyReport(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    healthcare_center = models.ForeignKey(Healthcare, on_delete=models.CASCADE)  # Changed from healthcare_center_id
    subdistrict = models.ForeignKey(Subdistrict, on_delete=models.CASCADE)
    month = models.DateField()
    births = models.IntegerField()
    vaccinations = models.IntegerField()
    deaths = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'citizen_report'  
        unique_together = ['volunteer', 'healthcare_center', 'month']
        ordering = ['-month']

    def __str__(self):
        return f"Report for {self.healthcare_center.name} - {self.month.strftime('%B %Y')}"

    def clean(self):
        if self.births < 0:
            raise ValidationError('Number of births cannot be negative')
        if self.vaccinations < 0:
            raise ValidationError('Number of vaccinations cannot be negative')
        if self.deaths < 0:
            raise ValidationError('Number of deaths cannot be negative')
        
class AllowanceApplicant(models.Model):
    id = models.AutoField(primary_key=True)
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    
    nid_number = models.CharField(max_length=17, unique=True)
    name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    birth_date = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    present_address = models.TextField()
    permanent_address = models.TextField()
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    application_date = models.DateTimeField(auto_now_add=True)
    subdistrict_id = models.IntegerField()
    
    def get_document_upload_path(instance, filename):
        folder_name = f"{instance.name.replace(' ', '')}{instance.nid_number}"
        return f'allowance_documents/{folder_name}/{filename}'        
    documents = models.FileField(
        upload_to=get_document_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])]
    )
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )

    class Meta:
        db_table = 'allowance_applicant'

    def _str_(self):
        return f"{self.name} - {self.nid_number}"

    def save(self, *args, **kwargs):
        # Ensure birth_date is a timezone-aware datetime
        if self.birth_date:
            if isinstance(self.birth_date, date):
                self.birth_date = timezone.make_aware(
                    datetime.combine(self.birth_date, datetime.min.time())
                )
            elif isinstance(self.birth_date, datetime) and timezone.is_naive(self.birth_date):
                self.birth_date = timezone.make_aware(self.birth_date)
        super().save(*args, **kwargs)
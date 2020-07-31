from django.db import models
from datetime import datetime, date

# Create your models here.
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

YES_NO_OPTION = [
	('Yes', 'Yes'),
	('No', 'No')
]

# One Quote Shell with a given unique ID can have many quotes with different vehicles or drivers 
class QuoteShell(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ['created']

class Quote(models.Model):
	LIMIT_OPTION = [
		('Minimum', '$15,000/$30,000/$10,000 (Minimum)'),
		('Good', '$25,000/$50,000/$25,000 (Good)'),
		('Better', '$50,000/$100,000/$25,000 (Better)'),
		('Best', '$100,000/$300,000/$50,000 (Best)'),
		('Superior', '$100,000/$300,000/$50,000 (Superior)'),
	]

	UNSECURE_COVERAGE_OPTION = [
		('Decline Coverage', 'Decline Coverage'),
		('Minimum', '$15,000/$30,000/$3,500 (Minimum)')
	]

	quote_shell = models.ForeignKey(QuoteShell, related_name='quotes', on_delete=models.CASCADE)
	ip = models.CharField(max_length=100, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	homeowner = models.CharField(choices=YES_NO_OPTION, max_length=5, null=True, blank=True)
	prior_insurance  = models.CharField(choices=YES_NO_OPTION, max_length=5, null=True, blank=True)
	limit  = models.CharField(choices=LIMIT_OPTION, max_length=20, null=True, blank=True)
	uninsured_cov  = models.CharField(choices=UNSECURE_COVERAGE_OPTION, max_length=20, null=True, blank=True)
	professional_discount = models.BooleanField(default=False, null=True, blank=True)
	student_discount = models.BooleanField(default=False, null=True, blank=True)
	military_discount = models.BooleanField(default=False, null=True, blank=True)

	class Meta:
		ordering = ['created']

# Address 
class Address(models.Model):
	RESIDENCE_TYPE = [
		('Single Family Home', 'Single Family Home'),
		('Condominuim', 'Condominuim'),
		('Mobile Home', 'Mobile Home'),
		('Apartment', 'Apartment')
	]

	quote = models.ForeignKey(Quote, related_name='addresses', on_delete=models.CASCADE)
	street = models.CharField(max_length=100, blank=False)
	street2 = models.CharField(max_length=100, blank=True, default='')
	city = models.CharField(max_length=100, blank=False)
	state = models.CharField(max_length=100, blank=False)
	zip = models.CharField(max_length=100, blank=False)
	residence_type = models.CharField(choices=RESIDENCE_TYPE, max_length=30, null=True, blank=True)

	# class Meta:
	#	 ordering = ['created']

# Driver(s) are elements of a Quote, i.e. 
# A quote can contain 1 to N drivers
class Driver(models.Model):
	GENDER_TYPE = [
		('Male', 'Male'),
		('Female', 'Female'),
		('Nonbinary', 'Nonbinary'),
	]
	MARTIAL_TYPE = [
		('Married', 'Married'),
		('Single', 'Single'),
		('Widowed', 'Widowed'),
		('Divorced', 'Divorced'),
		('Domestic Partnership', 'Domestic Partnership')
	]
	OCCUPATION_TYPE = [
		('Administrative Clerical', 'Administrative Clerical'),
		('Architect', 'Architect'),
		('Business Owner', 'Business Owner'),
		('Certified Public Accountant', 'Certified Public Accountant'),
		('Clergy', 'Clergy'),
		('Construction Trades', 'Construction Trades')
	]

	LICENSE_STATUS_TYPE = [
		('Active', 'Active'),
		('Permit', 'Permit'),
		('Expired', 'Expired'),
		('Suspened', 'Suspened'),
		('Foreign', 'Foreign'),
	]

	quote = models.ForeignKey(Quote, related_name='drivers', on_delete=models.CASCADE)
	first_name = models.CharField(max_length=100, blank=False)
	last_name = models.CharField(max_length=100, blank=False)
	dob = models.DateField(blank=True, null=True, default=date.today)
	phone = models.CharField(max_length=16, blank=False)
	email = models.EmailField(max_length=100, blank=False)
	gender = models.CharField(choices=GENDER_TYPE, max_length=12, null=True, blank=True)
	marital = models.CharField(choices=MARTIAL_TYPE, max_length=20, null=True, blank=True)
	age_license = models.CharField(max_length=100, blank=True)
	occupation = models.CharField(choices=OCCUPATION_TYPE, max_length=100, null=True, blank=True)
	license_status = models.CharField(choices=LICENSE_STATUS_TYPE, max_length=100, null=True, blank=True)
	sr22 = models.CharField(choices=YES_NO_OPTION, max_length=5, null=True, blank=True)
	dui = models.CharField(choices=YES_NO_OPTION, max_length=5, null=True, blank=True)
	prev_lic_status = models.CharField(choices=YES_NO_OPTION, max_length=5, null=True, blank=True)
	incident_status3 = models.CharField(choices=YES_NO_OPTION, max_length=5, null=True, blank=True)


# Vehicles(s) are elements of a Quote, i.e. 
# A quote can contain 1 to N vehicles
class Vehicle(models.Model):
	USE_TYPE_CHOICES = [
		('Commute', 'Commute'),
		('Pleasure', 'Pleasure'),
		('Business', 'Business'),
		('Uber/Lyft', 'Uber/Lyft'),
	]
	WORK_MILES_CHOICES = [
		('05', '0-5'),
		('510', '5-10'),
		('1015', '10-15'),
		('1520', '15-20'),
		('2030', '20-30'),
		('30g', '30+'),
	]
	YEAR_MILES_CHOICES = [
		('5000', '5,000'),
		('12000', '12,000'),
		('15000', '15,000'),
		('25000', '25,000+'),
	]
	COVERAGE_TYPE = [
		('Full Coverage', 'Full Coverage'),
		('Liability Only', 'Liability Only'),
	]
	MODEL_CHOICES = [
		('Ford', 'Ford'),
		('Chevrolet', 'Chevrolet'),
		('Toyota', 'Toyota'),
		('Honda', 'Honda'),
	]
	YEAR_CHOICES = []
	cur_year = int(datetime.now().strftime('%y')) + 1
	for x in range(1981, cur_year):
		YEAR_CHOICES.append((x, x))
		
	quote = models.ForeignKey(Quote, related_name='vehicles', on_delete=models.CASCADE)
	year = models.CharField(choices=YEAR_CHOICES, max_length=4)
	make = models.CharField(choices=MODEL_CHOICES, max_length=100, null=True, blank=True)
	model = models.CharField(max_length=100, null=True, blank=True) 
	use_type = models.CharField(choices=USE_TYPE_CHOICES, max_length=20, null=True, blank=True)
	work_miles = models.CharField(choices=WORK_MILES_CHOICES, max_length=10, null=True, blank=True)
	year_miles = models.CharField(choices=YEAR_MILES_CHOICES, max_length=20, null=True, blank=True)
	coverage_type = models.CharField(choices=COVERAGE_TYPE, max_length=20, null=True, blank=True)


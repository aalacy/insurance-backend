from django.db import models
from datetime import datetime

# Create your models here.
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ['created']


# One Quote Shell with a given unique ID can have many quotes with different vehicles or drivers 
class QuoteShell(models.Model):
    pass

class Quote(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    quote_shell = models.ForeignKey(QuoteShell, related_name='quotes', on_delete=models.CASCADE)


# class Address(models.Model):
# 	created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['created']

# Driver(s) are elements of a Quote, i.e. 
# A quote can contain 1 to N drivers
class Driver(models.Model):
	GENDER_TYPE = [
		('M', 'Male'),
		('F', 'Female'),
		('N', 'Male'),
	]

	quote = models.ForeignKey(Quote, related_name='drivers', on_delete=models.CASCADE)
	first_name = models.CharField(max_length=100, blank=False, default='')
	last_name = models.CharField(max_length=100, blank=False, default='')
	dob = models.DateField(max_length=100, blank=False, default='')
	phone = models.CharField(max_length=16, blank=False, default='')
	email = models.EmailField(max_length=100, blank=False, default='')
	gender = models.CharField(choices=GENDER_TYPE, default=None, max_length=1)


# Vehicles(s) are elements of a Quote, i.e. 
# A quote can contain 1 to N vehicles
class Vehicle(models.Model):
	USE_TYPE_CHOICES = [
	    ('CO', 'Commute'),
	    ('PL', 'Pleasure'),
	    ('BU', 'Business'),
	    ('UL', 'Uber/Lyft'),
	]
	WORK_MILES_CHOICES = [
		('05', '0-5'),
		('510', '5-10'),
		('1015', '10-15'),
		('1520', '15-20'),
		('2030', '20-30'),
		('30g', '30+'),
	]
	COVERAGE_TYPE = [
		('FC', 'Full Coverage'),
		('LO', 'Liability Only'),
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
	year = models.CharField(choices=YEAR_CHOICES, blank=False, max_length=4,  default=None)
	make = models.CharField(choices=MODEL_CHOICES, max_length=100, default=None)
	model = models.CharField(max_length=100, blank=False, default='')
	use_type = models.CharField(choices=USE_TYPE_CHOICES, default=None, max_length=2)
	work_miles = models.CharField(choices=WORK_MILES_CHOICES, default=None, max_length=10)
	year_miles = models.IntegerField(blank=True, default='')
	coverage_type = models.CharField(choices=COVERAGE_TYPE, default=None, max_length=2)


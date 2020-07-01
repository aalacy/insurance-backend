from rest_framework import serializers
from django.contrib.auth.models import User, Group
from quotes.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from quotes.models import QuoteShell, Quote, Driver, Vehicle

import time
from datetime import datetime
import pdb

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class SnippetSerializer(serializers.ModelSerializer):
	class Meta:
		model = Snippet
		fields = ['id', 'title', 'code', 'linenos', 'language', 'style']

class VehicleSerializer(serializers.ModelSerializer):

	class Meta:
		model = Vehicle
		fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):

	class Meta:
		model = Driver
		fields = '__all__'

	# def update(self, instance, _validated_data):
	# 	data = self._context['request'].data

	# 	instance.first_name = data.get('first_name', instance.first_name)
	# 	instance.last_name = data.get('first_name', instance.last_name)
	# 	instance.dob = data.get('first_name', instance.dob)
	# 	instance.first_name = data.get('first_name', instance.first_name)
	# 	instance.first_name = data.get('first_name', instance.first_name)
	# 	return instance

class QuoteSerializer(serializers.ModelSerializer):
	drivers = DriverSerializer(many=True, read_only=True)
	vehicles = VehicleSerializer(many=True, read_only=True)

	class Meta:
		model = Quote
		fields = '__all__'

	# def update(self, instance, _validated_data):
	# 	validated_data = self._context['request'].data

	# 	return instance

class QuoteShellSerializer(serializers.ModelSerializer):
	# quotes = serializers.StringRelatedField(many=True)
	# quotes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	quotes = QuoteSerializer(many=True, read_only=True)

	class Meta:
		model = QuoteShell
		fields = ['quotes', 'id']

	def create(self, _validated_data):
		"""
			create the quote shell in the first step with 
			only initial driver data

			Request URL /api/quoteshell/
			{
                "first_name": "fddddgg",
                "last_name": "sdddddddf",
                "dob": "2120-06-27",
                "phone": "20700009344362",
                "email": "oma324234r555@live.co.uk",
                "gender": "M",
            }
		"""
		driver_data = self._context['request'].data

		quote_shell = QuoteShell.objects.create()

		quote = Quote.objects.create(quote_shell=quote_shell)

		driver = Driver.objects.create(quote=quote, **driver_data)

		return quote_shell

	def update_driver(self, driver):
		instance = Driver.objects.get(id=driver['id'])

		instance.first_name = driver.get('first_name', instance.first_name)
		instance.last_name = driver.get('last_name', instance.last_name)
		instance.dob = driver.get('dob', instance.dob)
		instance.dob = datetime.strptime(instance.dob, "%Y-%m-%d") 
		instance.phone = driver.get('phone', instance.phone)
		instance.email = driver.get('email', instance.email)

		instance.save()

	def update_vehicle(self, vehicle, quote):
		if vehicle.get('id'):
			"""
				Update the vehicle
			"""
			instance = Vehicle.objects.get(id=vehicle['id'])

			instance.year = vehicle.get('year', instance.year)
			instance.make = vehicle.get('make', instance.make)
			instance.model = vehicle.get('model', instance.model)
			instance.use_type = vehicle.get('use_type', instance.use_type)
			instance.work_miles = vehicle.get('work_miles', instance.work_miles)
			instance.year_miles = vehicle.get('year_miles', instance.year_miles)
			instance.coverage_type = vehicle.get('coverage_type', instance.coverage_type)

			instance.save()
		else:
			"""
				Create the vehicle
			"""
			quote_obj = Quote.objects.get(id=quote['id'])

			Vehicle.objects.create(quote=quote_obj, **vehicle)

	def update(self, instance, validated_data):
		"""
			Update the quoteshell

			Request URL /api/quoteshell/<quoteshell_id>/
			{
				{
				   "quotes": [
				        {
				            "id": 1,
				            "drivers": [
				                {
				                    "id": 1,
				                    "first_name": "fddddgg",
				                    "last_name": "sdddddddf",
				                    "dob": "2120-06-27",
				                    "phone": "20700009344362",
				                    "email": "oma324234r555@live.co.uk",
				                    "quote": 1
				                }
				            ],
				            "vehicles": [],
				            "date": "2020-06-27T08:18:22.264801Z",
				            "quote_shell": 1
				        }
				    ],
				    "id": 1
				}
			}
		"""
		quotes = self._context['request'].data.pop('quotes')
		for quote in quotes:

			# get the drivers
			drivers = quote.pop('drivers', [])
			for driver in drivers:
				self.update_driver(driver)

			# get the vehicles
			vehicles = quote.pop('vehicles', [])
			for vehicle in vehicles:
				self.update_vehicle(vehicle, quote)

		return instance


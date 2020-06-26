from rest_framework import serializers
from django.contrib.auth.models import User, Group
from quotes.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from quotes.models import QuoteShell, Quote, Driver, Vehicle


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

class QuoteSerializer(serializers.ModelSerializer):
	drivers = DriverSerializer(many=True, read_only=True)
	vehicles = VehicleSerializer(many=True, read_only=True)

	class Meta:
		model = Quote
		fields = '__all__'

class QuoteShellSerializer(serializers.ModelSerializer):
	# quotes = serializers.StringRelatedField(many=True)
	# quotes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	quotes = QuoteSerializer(many=True, read_only=True)

	class Meta:
		model = QuoteShell
		fields = ['quotes', 'id']


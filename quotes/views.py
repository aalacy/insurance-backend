from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from quotes.models import QuoteShell, Quote, Driver, Vehicle, Address
# from quotes.permissions import IsOwnerOrReadOnly
from quotes.serializers import QuoteShellSerializer
from quotes.serializers import QuoteSerializer
from quotes.serializers import DriverSerializer, VehicleSerializer, AddressSerializer
from quotes.serializers import UserSerializer, GroupSerializer

import pdb

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class AddressViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        serializer.save()

class DriverViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def perform_create(self, serializer):
        serializer.save()

class VehicleViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def perform_create(self, serializer):
        serializer.save()

class QuoteViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        quote_shell = self.get_object()
        return Response(quote_shell.highlighted)

    def perform_create(self, serializer):
        serializer.save()

class QuoteShellViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = QuoteShell.objects.all()
    serializer_class = QuoteShellSerializer

    def perform_create(self, serializer):
        serializer.save()
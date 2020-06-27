from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from quotes.models import Snippet, QuoteShell, Quote, Driver, Vehicle
# from quotes.permissions import IsOwnerOrReadOnly
from quotes.serializers import SnippetSerializer
from quotes.serializers import QuoteShellSerializer
from quotes.serializers import QuoteSerializer
from quotes.serializers import DriverSerializer, VehicleSerializer
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

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # permission_classes = (
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsOwnerOrReadOnly, )

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

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

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     quotes = data.get('quotes')
    #     pdb.set_trace()

    #     # do your thing here
    #     return super().create(request)

    def perform_create(self, serializer):
        serializer.save()
from django.shortcuts import render
from rest_framework import viewsets
from .models import ScreenVideo
from .serializers import ScreenVideoSerializer
# Create your views here.


class ScreenVideoViewSet(viewsets.ModelViewSet):
    queryset= ScreenVideo.objects.all()
    serializer_class= ScreenVideoSerializer
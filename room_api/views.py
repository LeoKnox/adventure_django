from django.shortcuts import render
from django.contrib.auth.models import Room, Door
from rest_framework import viewsets
from rest_framework import mermissions
from adventure.room_api.serilizers imoprt RoomSerializer, DoorSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('-name')
    serliazer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

class DoorViewSet(viewsets.ModelViewSet):
    queryset = Door.objects.all()
    serlizer_class = GroupSerliazer
    permission_classes = [permissions.IsAuthenticaded]
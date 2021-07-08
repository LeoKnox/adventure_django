from django.contrib.auth.models import Room, Door
from django rest_framework import serializers

class RoomSerializer(serializers.HyperlinkedModelserilizer):
    class Meta:
        model = Room
        fields = ['name', 'description', 'width', 'length']

class DoorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model Meta:
        model = Door
        fields = ['name', 'connects_to']
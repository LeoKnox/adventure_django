from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models

def validate_wall(value):
    print('value')
    if value > 9:
        raise ValidationError(
            _('%(value) is too great'),
            params ={'value': value},
        )

def unique_wall():
    pass

class DoorManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['next_room']) < 2:
            errors['next_room'] = "Door name should be more then 2 characters"
        if int(postData['location']) < 1:
            errors['minimum_location'] = "Location needs to be 1 or greater."
        #if int(postData['location']) >= Room.objects.get(id=postData['id']).location:
            #errors['maximum_location'] = "Door max exceeded" + str(Door.objects.filter(location=postData['location']).first().location)
        #if int(postData['location']) > Door.objects.get(id=postData['id']).location:
        if int(postData['location']) > Room.objects.get(id=postData['room_id']).width:
            print("error error err... ")
            errors['maximum_location'] = postData['location'] + "Door cannot exceed length " + str(Room.objects.get(id=postData['room_id']).width)
        return errors

class Room(models.Model):
    SHAPES = [('Room', 'Room'), ('Hallway', 'Hallway'), ('Stairs', 'Stairs')]
    name = models.CharField(max_length = 50)
    description = models.TextField()
    shape = models.CharField(max_length = 100, choices=SHAPES)
    width = models.IntegerField(validators=[validate_wall])
    height = models.IntegerField()
    doors = models.ManyToManyField('Door')

class Door(models.Model):
    WALLS = [(0, 'North'), (1, 'East'), (2, 'South'), (3, 'West')]
    next_room = models.CharField(max_length=50)
    location = models.IntegerField(null=True, default=0)
    wall = models.IntegerField(null=True, default=0)
    objects = DoorManager()

    def __location_max__(self):
        return self.location

    def __str__(self):
        return self.next_room

class Treasure(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
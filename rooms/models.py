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

class RoomManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if int(postData['width']) <= 0:
            errors['width'] = "Width cannot be zero or lower."
        if int(postData['height']) <= 0:
            errors['height'] = "Height cannot be zero or lower."
        return errors

class DoorManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['next_room']) < 2:
            errors['next_room'] = "Door name should be more then 2 characters"
        if int(postData['location']) < 1:
            errors['minimum_location'] = "Location needs to be 1 or greater."
        room_validator = Room.objects.get(id=postData['room_id'])
        #room_validator.width = postData['wall']
        print(str(room_validator.width) + "!!!!!!!!")
        if postData['wall'] == 0 or Door.objects.get(id=postData['id']).wall == 2:
        #if Door.objects.get(id=postData['id']).wall == 0 or Door.objects.get(id=postData['id']).wall == 2:
            print(str(room_validator.width) + "!!!!!!!!")
            if int(postData['location']) > room_validator.width:
                errors['maximum_location'] = "Door cannot exceed length " + str(Room.objects.get(id=postData['room_id']).width)
        else:
            if int(postData['location']) > room_validator.height:
                room_validator.width = postData['wall']
                errors['maximum_location'] = "Door cannot exceed length " + str(Room.objects.get(id=postData['room_id']).height)
        return errors

class Room(models.Model):
    SHAPES = [('Room', 'Room'), ('Hallway', 'Hallway'), ('Stairs', 'Stairs')]
    name = models.CharField(max_length = 50)
    description = models.TextField()
    shape = models.CharField(max_length = 100, choices=SHAPES)
    width = models.IntegerField(validators=[validate_wall])
    height = models.IntegerField()
    doors = models.ManyToManyField('Door')
    objects = RoomManager()

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
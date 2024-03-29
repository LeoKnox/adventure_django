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

class TreasureManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['treasure_name']) < 5:
            errors['treasure_name'] = "Name must be 5 characters or more."
        return errors

class RoomManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        print (postData['width'].isnumeric())
        if not postData['width'].isnumeric() or not postData['height'].isnumeric():
            errors['alphabet'] = "Please enter a character."
        if postData['width'] == "":
            errors['width'] = "Please enter width."
        elif postData['width'].isnumeric() and int(postData['width']) <= 0:
            errors['width'] = "Width cannot be zero or lower."
        if postData['height'] == "":
            errors['height'] = "Please enter height."
        elif postData['height'].isnumeric() and int(postData['height']) <= 0:
            errors['height'] = "Height cannot be zero or lower."
        if len(postData['name']) > 2:
            errors['name'] = "Room name must be at least 3 characters."
        return errors

class DoorManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData.get('next_room')) < 2:
            errors['next_room'] = "Door name should be more then 2 characters"
        if int(postData['location']) < 1:
            errors['minimum_location'] = "Location needs to be 1 or greater."
        room_validator = Room.objects.get(id=postData['room_id'])
        y = room_validator.doors.all()
        x = Door.objects.get(id = postData['id'])
        for z in y:
            if z.id != int(postData['id']) and z.wall == int(postData['wall']) and z.location == int(postData['location']):
                errors['duplicate_door'] = "Cannot have 2 doors in same location."
        if postData['wall'] == 0 or postData['wall'] == 2:
            if int(postData['location']) >= room_validator.width:
                errors['maximum_location'] = "Door cannot exceed length " + str(room_validator.width-1)
        else:
            if int(postData['location']) >= room_validator.height:
                errors['maximum_location'] = "Door cannot exceed length " + str(room_validator.height-1)
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
    objects = TreasureManager()
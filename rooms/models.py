from django.db import models

class Room(models.Model):
    SHAPES = [('Square', 'Square'), ('Circle', 'Circle'), ('Oval', 'Oval')]
    name = models.CharField(max_length = 50)
    description = models.TextField()
    shape = models.CharField(max_length = 100, choices=SHAPES)
    width = models.IntegerField()
    height = models.IntegerField()
    doors = models.ManyToManyField('Door')

class Door(models.Model):
    WALLS = [(0, 'North'), (1, 'East'), (2, 'South'), (3, 'West')]
    next_room = models.CharField(max_length=50)
    location = models.IntegerField(null=True, default=0)
    wall = models.IntegerField(null=True, default=0,choices=WALLS)

class Treasure(models.Model):
    name: models.CharField(max_length=50)
    descritpion: models.TextField()

    def __str__(self):
        return self.next_room
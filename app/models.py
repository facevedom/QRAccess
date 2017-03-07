"""
Definition of models.
"""

from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=100)
    telephone = models.IntegerField()

    def __str__(self):
        return self.name 


class Event(models.Model):
    # TODO perhaps add Sponsors for events?
    name = models.CharField(max_length=150)
    company = models.ForeignKey(Company)
    start_date = models.DateField()
    end_date = models.DateField()
    event_id = models.CharField(max_length=50)

    def __str__(self):
        return self.name 

    
class Room(models.Model):
    name = models.CharField(max_length=150)
    company = models.ForeignKey(Company)
    security_level = models.IntegerField()

    def __str__(self):
        return '%s @ %s' % (self.name, self.company)


class Permission(models.Model):
    user_id = models.CharField(max_length=150)
    event = models.ForeignKey(Event)
    room = models.ManyToManyField(Room)

    def __str__(self):
        return '%s @ %s' % (self.user_id, self.event)

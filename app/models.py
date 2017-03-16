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


class Room(models.Model):
    name = models.CharField(max_length=150)
    company = models.ForeignKey(Company)
    security_level = models.IntegerField()
    description = models.CharField(max_length=1000, default='No description')
    id = models.CharField(max_length=150, primary_key=True)

    def __str__(self):
        return '%s' % (self.name)


class Event(models.Model):
    # TODO perhaps add Sponsors for events?
    name = models.CharField(max_length=150)
    company = models.ForeignKey(Company)
    start_date = models.DateField()
    end_date = models.DateField()
    event_id = models.CharField(max_length=50, primary_key=True)
    rooms = models.ManyToManyField(Room, blank=True)

    def __str__(self):
        return self.name


class EndUser(models.Model):
    id = models.CharField(max_length=150, primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    def __str__(self):
        return '%s - %s %s' % (self.id, self.name, self.last_name)


class Permission(models.Model):
    user_id = models.ForeignKey(EndUser)
    event = models.ForeignKey(Event)
    id = models.CharField(max_length=150, primary_key=True)

    def __str__(self):
        return '%s @ %s' % (self.user_id, self.event)

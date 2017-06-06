"""
Definition of models.
"""

from django.db import models
from datetime import date
from datetime import datetime


class Company(models.Model):
    name = models.CharField(max_length=150, unique=True)
    address = models.CharField(max_length=150)
    email = models.EmailField(max_length=100, unique=True)
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
        return '%s @ %s' % (self.name, self.company)


class Event(models.Model):
    # TODO perhaps add Sponsors for events?
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    company = models.ForeignKey(Company)
    start_date = models.DateField()
    end_date = models.DateField()
    event_id = models.CharField(max_length=50, primary_key=True)
    rooms = models.ManyToManyField(Room, blank=True)

    @property
    def ongoing(self):
        return self.start_date <= date.today() <= self.end_date

    @property
    def past(self):
        return date.today() > self.end_date

    @property
    def future(self):
        return self.start_date > date.today()

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

class AccessLog(models.Model):
    room = models.ForeignKey(Room)
    permission = models.ForeignKey(Permission)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return '{room} @ {permission} - {date}'.format(room = self.room, permission = self.permission, date=self.date)

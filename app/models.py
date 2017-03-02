"""
Definition of models.
"""

from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=100)
    telephone = models.IntegerField()


class Event(models.Model):
    # TODO perhaps add Sponsors for events?
    name = models.CharField(max_length=150)
    company = models.ForeignKey(Company)
    start_date = models.DateField()
    end_date = models.DateField()
    event_id = models.CharField(max_length=50)



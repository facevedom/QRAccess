#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User

from app.forms import AttendeeRegistration
from app.models import EndUser
from app.models import Room
from app.models import Company
from app.models import Event
from app.models import Permission

from datetime import datetime
from datetime import timedelta


class UserRegistrationTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='testcompany', password='12345')
        user.save()

        self.company = Company.objects.create(name='PSL', email='contact@psl.com.co', telephone='2761234')
        self.company = Company.objects.create(name='testcompany', email='contact@test.com.co', telephone='2761234')

        Room.objects.create(id='r00m1', company=self.company, security_level=1)
        Room.objects.create(id='r00m2', company=self.company, security_level=2)
        Room.objects.create(id='r00m3', company=self.company, security_level=3)
        
        Event.objects.create(
            event_id='3v3nt',
            company=self.company,
            start_date=datetime.today(),
            end_date=datetime.today() + timedelta(days=3)
        )

        EndUser.objects.create(id='u53r')

    def test_user_registration_empty(self):
        # tests for validation failure if user's data is empty
        form_data = {'email': '', 'user_id': '', 'name': '', 'last_name': '', 'event_id': ''}
        form = AttendeeRegistration(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_registration_response_405_after_GET(self):
        response = self.client.get('/user/registration')
        self.assertEqual(response.status_code, 405)

    def test_user_registration_save_a_permission(self):
        self.client.post(
            '/user/registration',
            data={
                'user_id': 'u53r',
                'name': 'James',
                'last_name': 'Logan',
                'email': 'logan@xmen.com',
                'event_id': '3v3nt'
            }
        )
        self.assertEqual(Permission.objects.count(), 1)
        new_permission = Permission.objects.first()
        self.assertEqual(new_permission.user_id.pk, 'u53r')
        self.assertEqual(new_permission.event.pk, '3v3nt')

    def test_user_registration_save_a_new_user(self):
        self.client.post(
            '/user/registration',
            data={
                'user_id': 'n3wu53r',
                'name': 'James',
                'last_name': 'Logan',
                'email': 'logan@xmen.com',
                'event_id': '3v3nt'
            }
        )
        self.assertEqual(EndUser.objects.count(), 2)
        new_user = EndUser.objects.first()
        self.assertEqual(new_user.pk, 'n3wu53r')

    def test_user_registration_returns_permission_id(self):
        response = self.client.post(
            '/user/registration',
            data={
                'user_id': 'u53r',
                'name': 'James',
                'last_name': 'Logan',
                'email': 'logan@xmen.com',
                'event_id': '3v3nt'
            }
        )
        new_permission = Permission.objects.first()
        self.assertTemplateUsed(response, 'app/success.html')
        #self.assertEquals(response.content.decode(), new_permission.pk)

    def test_user_registration_invalid(self):
        response = self.client.post(
            '/user/registration',
            data={
                'user_id': '',
                'name': 'James',
                'last_name': 'Logan',
                'email': 'logan@xmen.com',
                'event_id': '3v3nt'
            }
        )
        self.assertEquals(response.content.decode(), 'False')
        
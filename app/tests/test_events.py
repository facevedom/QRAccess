from django.test import TestCase

from app.models import Permission
from app.models import EndUser
from app.models import Room
from app.models import Company
from app.models import Event
from django.contrib.auth.models import User
from app.forms import EventCreation
from app.views import create_event
from datetime import datetime
from datetime import timedelta
from datetime import date


class AccessTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='testcompany', password='12345')
        user.save()
        self.company = Company.objects.create(name='testcompany', email='contact@test.com.co', telephone='2761234')
        self.first_room = Room.objects.create(id='r00m1', company=self.company, security_level=1)
        self.second_room = Room.objects.create(id='r00m2', company=self.company, security_level=2)
        self.third_room = Room.objects.create(id='r00m3', company=self.company, security_level=3)

    def test_login_required_on_GET_for_creation(self):
        response = self.client.get('/create/event')
        self.assertEqual(response.status_code, 302)

    def test_rendering_on_GET_and_logged_in_for_creation(self):
        logged_in = self.client.login(username='testcompany', password='12345')
        response = self.client.get('/create/event')
        self.assertTemplateUsed(response, 'event/create.html')
    
    def test_create_valid_event(self):
        self.client.login(username='testcompany', password='12345')
        start_date = datetime.today(),
        end_date = datetime.today() + timedelta(days=3)
        form_data = {
                        'name': 'test event',
                        'description': 'description for test event',
                        'event_id': 'asjdfkldfj-aKJG9',
                        'start_date': datetime.today(),
                        'end_date': datetime.today() + timedelta(days=3),
                        'company': self.company,
                        'allowed_rooms': 'OUAsdoi8908'
                    }
        form = EventCreation(data=form_data)
        self.assertTrue(form.is_valid())

    def test_save_event(self):
        self.client.login(username='testcompany', password='12345')
        self.client.post(
            '/create/event',
            data={
                'name': 'gadejo',
                'description': 'gen desc',
                'start_date': '03/20/2017',
                'end_date': '03/25/2017'
                # TODO we need to test for rooms!
            }
        )
        self.assertEqual(Event.objects.count(), 1)
        new_event = Event.objects.first()
        self.assertEqual(new_event.name, 'gadejo')
        self.assertEqual(new_event.description, 'gen desc')
        self.assertEqual(new_event.start_date, date(2017, 3, 20))
        self.assertEqual(new_event.end_date, date(2017, 3, 25))

    def test_login_required_on_GET_for_listing(self):
        response = self.client.get('/list/events')
        self.assertEqual(response.status_code, 302)

    def test_rendering_on_GET_and_logged_in_for_listing(self):
        logged_in = self.client.login(username='testcompany', password='12345')
        Event.objects.create(
            event_id='3v3nt',
            name='Test Event',
            description='Test Event desc',
            company=self.company,
            start_date=datetime(2017, 4, 12),
            end_date=datetime(2017, 4, 15)
        )
        response = self.client.get('/list/events')
        self.assertTemplateUsed(response, 'event/list.html')

    def test_listing_empty_events_list(self):
        self.client.login(username='testcompany', password='12345')
        response = self.client.get('/list/events')
        self.assertTemplateUsed(response, 'app/error.html')

    def test_listing_proper_events(self):
        Event.objects.create(
            event_id='3v3nt',
            name='Test Event',
            description='Test Event desc',
            company=self.company,
            start_date=datetime(2017, 4, 12),
            end_date=datetime(2017, 4, 15)
        )
        Event.objects.create(
            event_id='3v3nt_2',
            name='Second Test Event',
            description='Second Test Event desc',
            company=self.company,
            start_date=datetime(2017, 4, 12),
            end_date=datetime(2017, 4, 15)
        )
        self.client.login(username='testcompany', password='12345')
        response = self.client.get('/list/events')
        self.assertContains(response, 'Test Event')
        self.assertContains(response, 'Second Test Event')
    
    def test_delete_not_logged(self):
        Event.objects.create(
            event_id='3v3nt',
            name='Test Event',
            description='Test Event desc',
            company=self.company,
            start_date=datetime(2017, 4, 12),
            end_date=datetime(2017, 4, 15)
        )
        response = self.client.get('/delete/event/3v3nt')
        self.assertEqual(response.status_code, 302)

    def test_delete_invalid_event(self):
        self.client.login(username='testcompany', password='12345')
        response = self.client.get('/delete/event/invalidid90380384092834')
        self.assertTemplateUsed(response, 'app/error.html')

    def test_delete_event(self):
        self.client.login(username='testcompany', password='12345')
        Event.objects.create(
            event_id='3v3nt',
            name='Test Event',
            description='Test Event desc',
            company=self.company,
            start_date=datetime(2017, 4, 12),
            end_date=datetime(2017, 4, 15)
        )
        response = self.client.get('/delete/event/3v3nt')
        self.assertEqual(Event.objects.count(), 0)
        self.assertTemplateUsed(response, 'app/success.html')
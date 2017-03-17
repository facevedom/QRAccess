from django.test import TestCase
from django.http import HttpRequest

from app.forms import User_self_registration
from app.views import user_registration
from app.models import EndUser
from app.models import Room
from app.models import Company
from app.models import Event
from app.models import Permission

from datetime import datetime


class UserRegistrationTest(TestCase):
    """
        Tests for user story: EVE5
    """
    def setUp(self):
        Company.objects.create(name='PSL', email='contact@psl.com.co', telephone='2761234')
        self.company = Company.objects.first()

        Room.objects.create(id='r00m1', company=self.company, security_level=1)
        Room.objects.create(id='r00m2', company=self.company, security_level=2)
        Room.objects.create(id='r00m3', company=self.company, security_level=3)

        Event.objects.create(event_id='3v3nt', company=self.company, start_date=datetime(2017,4,12), end_date=datetime(2017,4,15))        

        EndUser.objects.create(id='u53r')

    def test_user_registration_empty(self):
        # tests for validation failure if user's data is empty
        form_data = {'email': '', 'user_id': '', 'name': '', 'last_name': '', 'event_id': '', 'rooms': ''}
        form = User_self_registration(data=form_data)
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
                'event_id': '3v3nt',
                'rooms': 'r00m1,r00m2,r00m3'
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
                'event_id': '3v3nt',
                'rooms': 'r00m1,r00m2,r00m3'
            }
        )
        self.assertEqual(EndUser.objects.count(), 2)
        new_user = EndUser.objects.first()
        self.assertEqual(new_user.pk, 'n3wu53r')

    def test_user_registration_redirects_to_generate_qr(self):
        response = self.client.post(
            '/user/registration',
            data={
                'user_id': 'u53r',
                'name': 'James',
                'last_name': 'Logan',
                'email': 'logan@xmen.com',
                'event_id': '3v3nt',
                'rooms': 'r00m1,r00m2,r00m3'
            }
        )
        new_permission = Permission.objects.first()
        self.assertRedirects(response, '/generate/%s' % new_permission.pk)

    def test_user_access_the_link_received(self):
        # tests for validation failure if user's data is empty
        form_data = {'email': '', 'id': '', 'name': '', 'last_name': '', 'event_id': ''}
        form = User_self_registration(data=form_data)
        self.assertFalse(form.is_valid())

    def test_generate_qr_returns_correct_html(self):
        """Tests generate QR page."""
        permission = Permission.objects.create(pk='93rm15s10n',
                                  user_id=EndUser.objects.get(pk='u53r'),
                                  event=Event.objects.get(pk='3v3nt')
            )
        response = self.client.get('/generate/%s' % permission.pk)
        self.assertTemplateUsed(response, 'end_user/generate_qr.html')
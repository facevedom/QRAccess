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


class EVE5Test(TestCase):
    """
        Tests for user story: EVE5
    """
    def setUp(self):
        Company.objects.create(name='PSL', email='contact@psl.com.co', telephone='2761234')
        company = Company.objects.first()

        Room.objects.create(id='r00m1', company=company, security_level=1)
        Room.objects.create(id='r00m2', company=company, security_level=2)
        Room.objects.create(id='r00m3', company=company, security_level=3)

        Event.objects.create(event_id='3v3nt', company=company, start_date=datetime(2017,4,12), end_date=datetime(2017,4,15))
        EndUser.objects.create(id='u53r')

    def test_user_registration_empty(self):
        # tests for validation failure if user's data is empty
        form_data = {'email': '', 'user_id': '', 'name': '', 'last_name': '', 'event_id': '', 'rooms': ''}
        form = User_self_registration(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_registration_response_405_after_GET(self):
        request = HttpRequest()
        request.method = 'GET'
        response = user_registration(request)
        self.assertEqual(response.status_code, 405)

    def test_user_registration_save_a_permission(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['user_id'] = 'u53r'
        request.POST['name'] = 'James'
        request.POST['last_name'] = 'Logan'
        request.POST['email'] = 'logan@xmen.com'
        request.POST['event_id'] = '3v3nt'
        request.POST['rooms'] = 'r00m1,r00m2,r00m3'

        response = user_registration(request)
        self.assertEqual(Permission.objects.count(), 1)
        new_permission = Permission.objects.first()
        self.assertEqual(new_permission.user_id.pk, 'u53r')
        self.assertEqual(new_permission.event.pk, '3v3nt')
        self.assertCountEqual([room.pk for room in new_permission.rooms.all()], ['r00m1', 'r00m2', 'r00m3'])

    def test_user_registration_redirects_to_generate_qr(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['user_id'] = 'u53r'
        request.POST['name'] = 'James'
        request.POST['last_name'] = 'Logan'
        request.POST['email'] = 'logan@xmen.com'
        request.POST['event_id'] = '3v3nt'
        request.POST['rooms'] = 'r00m1,r00m2,r00m3'

        response = user_registration(request)
        new_permission = Permission.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '../generate/%s' % new_permission.pk)
        
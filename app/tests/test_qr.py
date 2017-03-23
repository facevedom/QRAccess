from django.test import TestCase
from app.forms import AttendeeRegistration
from app.models import EndUser
from app.models import Room
from app.models import Company
from app.models import Event
from app.models import Permission

from datetime import datetime


class UserRegistrationTest(TestCase):

    def setUp(self):
        Company.objects.create(name='PSL', email='contact@psl.com.co', telephone='2761234')
        self.company = Company.objects.first()

        Room.objects.create(id='r00m1', company=self.company, security_level=1)
        Room.objects.create(id='r00m2', company=self.company, security_level=2)
        Room.objects.create(id='r00m3', company=self.company, security_level=3)

        Event.objects.create(
            event_id='3v3nt',
            company=self.company,
            start_date=datetime(2017, 4, 12),
            end_date=datetime(2017, 4, 15)
        )

        EndUser.objects.create(id='u53r')

    def test_generate_qr_returns_correct_html(self):
        """Tests generate QR page."""
        permission = Permission.objects.create(
                        pk='93rm15s10n',
                        user_id=EndUser.objects.get(pk='u53r'),
                        event=Event.objects.get(pk='3v3nt')
                    )
        response = self.client.get('/generate/%s' % permission.pk)
        self.assertTemplateUsed(response, 'end_user/generate_qr.html')

    def test_generate_qr_invalid_code_requested(self):
        response = self.client.get('/generate/%s' % 'inv4l1dCo_dE')
        self.assertTemplateUsed(response, 'app/error.html')

    def test_scan_qr_proper_html(self):
        response = self.client.get('/scan')
        self.assertTemplateUsed(response, 'end_user/scan.html')
    
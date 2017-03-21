from django.test import TestCase

from app.models import Permission
from app.models import EndUser
from app.models import Room
from app.models import Company
from app.models import Event

from datetime import datetime
from datetime import timedelta


class AccessTest(TestCase):

    def setUp(self):
        self.company = Company.objects.create(name='PSL', email='contact@psl.com.co', telephone='2761234')
        self.first_room = Room.objects.create(id='r00m1', company=self.company, security_level=1)
        self.second_room = Room.objects.create(id='r00m2', company=self.company, security_level=2)
        self.third_room = Room.objects.create(id='r00m3', company=self.company, security_level=3)
        self.event = Event.objects.create(
                        event_id='3v3nt',
                        company=self.company,
                        start_date=datetime.today(),
                        end_date=datetime.today() + timedelta(days=3)
                    )
        self.finished_event = Event.objects.create(
                        event_id='old-3v3nt',
                        company=self.company,
                        start_date=datetime.today() - timedelta(days=20),
                        end_date=datetime.today() - timedelta(days=3)
                    )
        self.event.rooms.add(self.first_room)
        self.event.rooms.add(self.second_room)
        self.enduser = EndUser.objects.create(id='u53r')

        self.permission = Permission.objects.create(pk='permission1', user_id=self.enduser, event=self.event)
        self.expired_permission = Permission.objects.create(
                                    pk='permission2',
                                    user_id=self.enduser,
                                    event=self.finished_event
                                   )

    def test_check_room_access(self):
        response = self.client.post(
                        '/check-access',
                        data={
                            'permission_id': self.permission.pk,
                            'room_id': self.first_room.pk
                        }
                    )
        self.assertEquals(response.content.decode(), 'True')

    def test_check_permission_does_not_exists(self):
        response = self.client.post(
                        '/check-access',
                        data={
                            'permission_id': 'permission3',
                            'room_id': self.first_room.pk
                        }
                    )

        self.assertEquals(response.content.decode(), 'False')

    def test_check_room_does_not_exists(self):
        response = self.client.post(
                        '/check-access',
                        data={
                            'permission_id': self.permission.pk,
                            'room_id': 'r00m4'
                        }
                    )
        self.assertEquals(response.content.decode(), 'False')

    def test_invalid_date(self):
        response = self.client.post(
                        '/check-access',
                        data={
                            'permission_id': self.expired_permission.pk,
                            'room_id': self.first_room.pk
                        }
                    )
        self.assertEquals(response.content.decode(), 'False')

    def test_no_GET_request(self):
        response = self.client.get('/check-access')
        self.assertEquals(response.content.decode(), 'False')
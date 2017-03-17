from django.test import TestCase
from app.models import EndUser
from app.models import Room
from app.models import Company
from app.models import Event
from app.models import Permission

from datetime import datetime

class ModelsTest(TestCase):


    def test_saving_and_retrieving_models(self):
        company = Company()
        company.name = 'PSL'
        company.email = 'contact@psl.com.co'
        company.telephone = 7777777
        company.save()

        first_room = Room()
        first_room.name = 'Peter Santamaria'
        first_room.company = company
        first_room.security_level = 2
        first_room.description = 'Conference room'
        first_room.id = 'r00m1'
        first_room.save()

        second_room = Room()
        second_room.name = '201'
        second_room.company = company
        second_room.security_level = 1
        second_room.description = 'Class room'
        second_room.id = 'r00m2'
        second_room.save()

        third_room = Room()
        third_room.name = 'rest'
        third_room.company = company
        third_room.security_level = 1
        third_room.description = 'Rest room'
        third_room.id = 'r00m3'
        third_room.save()

        event = Event()
        event.name = 'My event'
        event.company = company
        event.start_date = datetime(2017, 3, 16)
        event.end_date = datetime(2017, 3, 21)
        event.event_id = '3v3nt'
        event.rooms.add(first_room)
        event.rooms.add(second_room)
        event.rooms.add(third_room)
        event.save()

        enduser = EndUser()
        enduser.id = 'u53r'
        enduser.name = 'Sebastian'
        enduser.last_name = 'Villegas'
        enduser.email = 'svillegas@qraccess.com'
        enduser.save()

        first_permission = Permission()
        first_permission.user_id = enduser
        first_permission.event = event
        first_permission.id = '93rm151'
        first_permission.save()

        second_permission = Permission()
        second_permission.user_id = enduser
        second_permission.event = event
        second_permission.id = '93rm152'
        second_permission.save()

        saved_company = Company.objects.first()
        self.assertEqual(saved_company, company)

        saved_rooms = Room.objects.all()
        self.assertEqual(saved_rooms.count(), 3)
        self.assertEqual(saved_rooms[0], first_room)
        self.assertEqual(saved_rooms[1], second_room)
        self.assertEqual(saved_rooms[2], third_room)

        saved_event = Event.objects.first()
        self.assertEqual(saved_event, event)

        saved_enduser = EndUser.objects.first()
        self.assertEqual(saved_enduser, enduser)

        saved_permissions = Permission.objects.all()
        self.assertEqual(saved_permissions.count(), 2)
        self.assertEqual(saved_permissions[0], first_permission)
        self.assertEqual(saved_permissions[1], second_permission)

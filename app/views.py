"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from datetime import date
from app.forms import EventCreation
from app.forms import AttendeeRegistration
from django.http import HttpResponse, HttpResponseRedirect
from app.utils import generate_token
from app.models import Permission
from app.models import EndUser
from app.models import Event
from app.models import Company
from django.views.decorators.csrf import csrf_exempt  # for testing only
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Contact',
            'message': 'Your contact page.',
            'year': datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )


def error_happened(request, message):
    return render(
        request,
        'app/error.html',
        {
            'title': 'Oops',
            'message': message,
        }
    )


def success_happened(request, message):
    return render(
        request,
        'app/success.html',
        {
            'title': 'Done!',
            'message': message,
        }
    )


@csrf_exempt
@require_POST
def user_registration(request):

    form = AttendeeRegistration(request.POST)

    if form.is_valid():
        data = form.cleaned_data
        user_id = data['user_id']
        name = data['name']
        last_name = data['last_name']
        email = data['email']
        event_id = data['event_id']

        if not Event.objects.filter(event_id=event_id).exists():
            return HttpResponse('Evento inválido')
        else:
            event = Event.objects.get(event_id=event_id)

        # TODO what if id is already registered but with a different email or name?

        if not EndUser.objects.filter(id=user_id).exists():
            user = EndUser.objects.create(id=user_id, name=name, last_name=last_name, email=email)
            user.save()
        else:
            user = EndUser.objects.get(id=user_id)

        if not Permission.objects.filter(user_id=user, event=event).exists():
            token_id = generate_token()
            permission = Permission.objects.create(user_id=user, event=event, id=token_id)
        else:
            return HttpResponse(False)

        # TODO send email with link
        return HttpResponse(token_id)
    else:
        return HttpResponse(False)


def generate_qr(request, id):
    try:
        permission = Permission.objects.get(id=id)
        event = permission.event
        description = event.description
        allowed_rooms = event.rooms
        company = event.company
        start_date = event.start_date
        end_date = event.end_date
        name = permission.user_id.name

    except Permission.DoesNotExist:
        return error_happened(request, 'Invalid code for QR generation')
    else:
        return render(
            request,
            'end_user/generate_qr.html',
            {
                'generating_qr': True,
                'qr_id': id,
                'allowed_rooms': allowed_rooms,
                'event': event,
                'company': company,
                'start_date': start_date,
                'end_date': end_date,
                'year': datetime.now().year,
                'title': 'QR Generated',
                'name': name,
                'description': description,
            }
        )


@csrf_exempt
def check_room_access(request):
    if request.method == 'POST':

        permission_id = request.POST.get('permission_id')
        room_id = request.POST.get('room_id')

        try:
            permission = Permission.objects.get(id=permission_id)
        except Permission.DoesNotExist:
            return HttpResponse(False)

        start_date = permission.event.start_date
        end_date = permission.event.end_date

        if not (start_date <= date.today() <= end_date):
            return HttpResponse(False)

        if permission.event.rooms.all().filter(id=room_id).exists():
            return HttpResponse(True)

        return HttpResponse(False)

    else:
        return HttpResponse(False)


@login_required
def create_event(request):
    if request.method == 'POST':

        logged_user = request.user.username
        form = EventCreation(request.POST, logged_user=logged_user)
        if form.is_valid():
            data = form.cleaned_data
            company = Company.objects.get(name=logged_user)

            event = Event.objects.create(
                        name=data['name'],
                        company=company,
                        start_date=data['start_date'],
                        end_date=data['end_date'],
                        event_id=generate_token(),
                        description=data['description']
                    )
            for room in data['allowed_rooms']:
                event.rooms.add(room)

            return success_happened(request, 'Succesfully created the event %s' % data['name'])

    else:
        form = EventCreation(logged_user=request.user.username)

    return render(
        request,
        'event/create.html',
        {
           'creating_event': True,
           'form': form,
           'year': datetime.now().year,
           'title': 'Create an event'
        }
    )


@login_required
def list_events(request):
    logged_user = request.user.username
    # TODO implement paginator, it comes in handy here
    events = Company.objects.get(name=logged_user).event_set.all().order_by('-start_date')
    if events.exists():
        return render(
            request,
            'event/list.html',
            {
               'events': events,
               'year': datetime.now().year,
               'title': 'Your events'
            }
        )
    return error_happened(request, 'You have no events to list')


@login_required
def delete_event(request, event_id):

    logged_user = request.user.username

    try:
        company = Company.objects.get(name=logged_user)
        event = Event.objects.get(event_id=event_id, company=company)
    except Event.DoesNotExist:
        return error_happened(request, 'Invalid event')

    event.delete()

    return success_happened(request, 'Succesfully deleted the event %s' % event.name)


def scan_qr(request):
    return render(
        request,
        'end_user/scan.html',
        {
            'year': datetime.now().year,
            'title': 'Scanning QR',
            'message': 'Place your QR code in front of the webcam',
            'reading_qr': True
        }
    )


def permission_details(request, permission_id):

    try:        
        permission = Permission.objects.get(pk=permission_id)
    except Permission.DoesNotExist:
        return error_happened(request, 'Invalid code')

    qr_user = permission.user_id
    event = permission.event

    return render(
        request,
        'end_user/details.html',
        {
           'year': datetime.now().year,
           'title': 'Details',
           'qr_user': qr_user,
           'event': event    
        }
    )


@login_required
def event_details(request, event_id):

    logged_user = request.user.username
    company = Company.objects.get(name=logged_user)

    try:        
        event = Event.objects.get(pk=event_id, company=company)
    except Event.DoesNotExist:
        return error_happened(request, 'Invalid event')

    permissions = Permission.objects.filter(event=event)

    attendees = []
    for permission in permissions:
        attendee = permission.user_id
        attendees.append(attendee)

    return render(
        request,
        'event/details.html',
        {
           'year': datetime.now().year,
           'title': 'Details',
           'event': event,
           'attendees': attendees
        }
    )


@login_required
def add_attendee(request, event_id):
    if request.POST:
        logged_user = request.user.username
        form = AttendeeRegistration(request.POST)
        if form.is_valid():

            data = form.cleaned_data
            user_id = data['user_id']
            name = data['name']
            last_name = data['last_name']
            email = data['email']
            event_id = data['event_id']

            company = Company.objects.get(name=logged_user)
            # TODO check if ID exists
            event = Event.objects.get(event_id=event_id)
            if event.company != company:
                return error_happened(request, 'Invalid event')
            if event.end_date < date.today():
                return error_happened(request, 'Event has already finished')
            
            # TODO what if id is already registered but with a different email or name?

            if not EndUser.objects.filter(id=user_id).exists():
                user = EndUser.objects.create(id=user_id, name=name, last_name=last_name, email=email)
                user.save()
            else:
                user = EndUser.objects.get(id=user_id)

            if not Permission.objects.filter(user_id=user, event=event).exists():
                token_id = generate_token()
                permission = Permission.objects.create(user_id=user, event=event, id=token_id)
            else:
                return error_happened(request, '%s %s is already registered in event' % (name, last_name))

            return success_happened(request, 'Succesfully added %s %s to %s' % (name, last_name, event.name))

    else:
        form = AttendeeRegistration(initial={'event_id': event_id})
        event = Event.objects.get(event_id=event_id)

    return render(
        request,
        'event/add_attendee.html',
        {
           'form': form,
           'year': datetime.now().year,
           'title': 'Adding Attendee to %s' % event.name
        }
    )


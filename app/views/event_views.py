from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from datetime import datetime
from datetime import date

from app.views.main_views import error_happened
from app.views.main_views import success_happened
from app.forms import EventCreation
from app.forms import AttendeeRegistration
from app.models import Event
from app.models import Company
from app.models import EndUser
from app.models import Permission
from app.utils import generate_token

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


@login_required
def edit_event(request, event_id):
    
    event = Event.objects.get(event_id=event_id)

    if request.method == 'POST':

        logged_user = request.user.username
        form = EventCreation(request.POST, logged_user=logged_user)
        if form.is_valid():
            data = form.cleaned_data
            company = Company.objects.get(name=logged_user)
            event.name = data['name']
            event.company=company
            event.start_date=data['start_date']
            event.end_date=data['end_date']
            event.description=data['description']
            event.save()
            event.rooms.clear()
            for room in data['allowed_rooms']:
                event.rooms.add(room)

            return success_happened(request, 'Succesfully updated the event %s' % data['name'])

    else:
        form = EventCreation(
                logged_user=request.user.username,
                initial={'name': event.name,
                         'start_date': event.start_date,
                         'end_date': event.end_date,
                         'description': event.description,
                         'allowed_rooms': event.rooms.all
                         }
               )

    return render(
        request,
        'event/create.html',
        {
           'creating_event': True,
           'editing_event': True,
           'form': form,
           'year': datetime.now().year,
           'title': 'Edit an event'
        }
    )

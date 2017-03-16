"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from datetime import date
from app.forms import User_self_registration
from app.forms import EventCreation
from django.http import HttpResponse, HttpResponseRedirect
from app.utils import generate_token
from app.models import Permission
from app.models import EndUser
from app.models import Event
from app.models import Room
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


@csrf_exempt
@require_POST
def user_registration(request):

    form = User_self_registration(request.POST)

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

        token_id = generate_token()

        permission = Permission.objects.create(user_id=user, event=event, id=token_id)

        # TODO send email with link

        return HttpResponseRedirect('../generate/%s' % permission.id)

    else:
        return HttpResponse('Datos inválidos')


def generate_qr(request, id):
    try:
        permission = Permission.objects.get(id=id)
        event = permission.event
        allowed_rooms = event.rooms
        company = event.company
        start_date = event.start_date
        end_date = event.end_date
        name = permission.user_id.name

    except Permission.DoesNotExist:
        return HttpResponse('código inválido')
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

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return HttpResponse(False)
        
        # TODO replace by exists()
        if permission.event.rooms.all().filter(id=room_id).exists():
            return HttpResponse(True)

        return HttpResponse(False)

    else:
        return HttpResponse(False)


@login_required
def create_event(request):
    if request.method == 'POST':    
        form = EventCreation(request.POST, logged_user=request.user.username)
        if form.is_valid():
            data = form.cleaned_data
            for room in data['allowed_rooms']:
                pass

            return HttpResponse(data['allowed_rooms'])
            # check company, insert into db
        else:
            return HttpResponse('error validando')
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

"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from app.forms import User_self_registration
from app.forms import Login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from app.models import Permission
from app.models import EndUser
from app.models import Event

# for testing only
from django.views.decorators.csrf import csrf_exempt


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
def user_registration(request):
    if request.method == 'POST':
        form = User_self_registration(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_id = data['user_id']
            name = data['name']
            last_name = data['last_name']
            email = data['email']
            event_id = data['event_id']
            rooms = data['rooms'].split(",")

            if not Event.objects.filter(event_id=event_id).exists():
                return HttpResponse('Evento inválido')
            else:
                event = Event.objects.get(event_id=event_id)

            # TODO get rooms, create rooms objects, validate company rooms, insert into db

            # TODO what if id is already registered but with a different email or name?
            
            if not EndUser.objects.filter(id=user_id).exists():
                user = EndUser.objects.create(id=user_id, name=name, last_name=last_name, email=email)
                user.save()
            else: 
                user = EndUser.objects.get(id=user_id)

            permission = Permission.objects.create(user_id=user, event=event, id="RANDOM")
            
            return HttpResponse('%s/generate/%s' % ("dominio", "permiso"))

        else:
            return HttpResponse('Datos inválidos')
    return HttpResponse('Algo sucedió')


def login(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = Login()
    return render(
        request,
        'app/login.html',
        {
           'form': form,
           'year': datetime.now().year,
           'title': 'Login'
        }
    )


def logout_user(request):
    logout(request)
    return render(request, 'logged out')


def generate_qr(request, id):
    try:
        permission = Permission.objects.get(id=id)
        allowed_rooms = permission.room
        event = permission.event
        company = permission.event.company
        start_date = permission.event.start_date
        end_date = permission.event.end_date

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
            }
        )

from django.views.decorators.csrf import csrf_exempt  # for testing only
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.shortcuts import render

from datetime import datetime
from datetime import date

from app.forms import AttendeeRegistration
from app.models import Event
from app.models import EndUser
from app.models import Permission
from app.utils import generate_token
from app.views.main_views import error_happened
from app.views.main_views import success_happened

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
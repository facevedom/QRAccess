"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from app.forms import User_self_registration
from django.http import HttpResponse
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
            cd = form.cleaned_data
            name = cd['name']
            return render(request, 'end_user/user_registration_success.html', {'name': name})
    return HttpResponse("Error")

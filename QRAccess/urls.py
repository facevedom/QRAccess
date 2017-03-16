"""
Definition of urls for QRAccess.
"""

from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from datetime import datetime

import app.forms
import app.views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about$', app.views.about, name='about'),
    url(r'^user/registration$', app.views.user_registration, name='registration'),
    url(r'^create/event$', app.views.create_event, name='create_event'),
    url(r'^generate/([A-Za-z0-9-_]+)$', app.views.generate_qr, name='generate'),
    url(r'^check-access$', app.views.check_room_access),
    url(r'^login/$', auth_views.login, {'extra_context':{'title':'Login', 'year':datetime.now().year}}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^create/event$', app.views.create_event, name='create_event'),
    url(r'^delete/event/(?P<event_id>[A-Za-z0-9-_]+)$', app.views.delete_event, name='delete_event'),
    url(r'^list/events$', app.views.list_events, name='list_events'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
]

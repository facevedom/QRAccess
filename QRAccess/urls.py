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
    url(
        r'^login/$',
        auth_views.login,
        {'extra_context': {'title': 'Login', 'year': datetime.now().year}},
        name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^create/event$', app.views.create_event, name='create_event'),
    url(r'^edit/event/(?P<event_id>[A-Za-z0-9-_]+)$', app.views.edit_event, name='edit_event'),
    url(r'^delete/event/(?P<event_id>[A-Za-z0-9-_]+)$', app.views.delete_event, name='delete_event'),
    url(r'^list/events$', app.views.list_events, name='list_events'),
    url(r'^scan$', app.views.scan_qr, name='scan'),
    url(r'^details/permission/(?P<permission_id>[A-Za-z0-9-_]+)$', app.views.permission_details, name='permission_details'),
    url(r'^details/event/(?P<event_id>[A-Za-z0-9-_]+)$', app.views.event_details, name='event_details'),
    url(r'^add-attendee/event/(?P<event_id>[A-Za-z0-9-_]+)$', app.views.add_attendee, name='add_attendee'),
    url(r'^company/registration/$', app.views.company_registration, name='company_registration'),
    url(r'^company/password/', include('password_reset.urls'),),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
]

"""
Definition of urls for QRAccess.
"""

from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

import app.forms
import app.views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^user/registration$', app.views.user_registration, name='registration'),
    url(r'^login$', app.views.login_staff_user, name='login'),
    url(r'^logout_user', app.views.logout),
    url(r'^generate/([A-Za-z0-9]+)$', app.views.generate_qr, name='generate'),
    url(r'^check-access$', app.views.check_room_access),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
]

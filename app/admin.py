from django.contrib import admin
from .models import Company, Event, Room, Permission

admin.site.register(Company)
admin.site.register(Event)
admin.site.register(Room)
admin.site.register(Permission)

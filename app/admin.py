from django.contrib import admin
from .models import Company, Event, Room, Permission, EndUser, AccessLog

admin.site.register(Company)
admin.site.register(Event)
admin.site.register(Room)
admin.site.register(Permission)
admin.site.register(EndUser)
admin.site.register(AccessLog)

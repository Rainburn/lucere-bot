from django.contrib import admin
from .models import *

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'site', 'when', 'dateissued')
    search_fields = ('id', 'name', 'site', 'when', 'dateissued')

class UserAdmin(admin.ModelAdmin):
    list_display = ('userid', 'nickname')
    search_fields = ('userid', 'nickname')

class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ('event', 'user')
    search_fields = ('event', 'user')

admin.site.register(Event, EventAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(EventParticipant, EventParticipantAdmin)
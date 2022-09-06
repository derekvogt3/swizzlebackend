from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Event, Invitation


class EventAdmin(admin.ModelAdmin):
    pass


admin.site.register(Event, EventAdmin)


class InvitationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Invitation, InvitationAdmin)

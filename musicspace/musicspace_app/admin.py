from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    MusicspaceUser, Genre, Instrument,
    Provider, Address, TakeOneUser, TakeOneProfileVideoContainer
)

# Register your models here.

class MusicspaceUserAdmin(UserAdmin):
    pass

admin.site.register(MusicspaceUser, MusicspaceUserAdmin)


admin.site.register(Genre)
admin.site.register(Instrument)
admin.site.register(Provider)
admin.site.register(Address)
admin.site.register(TakeOneUser)
admin.site.register(TakeOneProfileVideoContainer)

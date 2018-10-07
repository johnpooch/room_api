from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Room


admin.site.register(Room, SimpleHistoryAdmin)

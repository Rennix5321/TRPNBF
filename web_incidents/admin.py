from django.contrib import admin
from .models import Incident, IncidentUser, Executor

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'priority', 'user', 'executor')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'description', 'user__name')
    list_select_related = ('user', 'executor')

admin.site.register(IncidentUser)
admin.site.register(Executor)

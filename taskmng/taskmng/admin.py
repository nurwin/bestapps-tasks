from django.contrib import admin
from django import forms
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse

from taskmng.models import *

class TaskScheduleAdmin(admin.ModelAdmin):
    list_display = ('task_schedule_name',)

admin.site.register(TaskSchedule, TaskScheduleAdmin)
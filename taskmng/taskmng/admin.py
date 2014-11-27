from django.contrib import admin
from django import forms
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse

from taskmng.models import *

class TaskScheduleAdmin(admin.ModelAdmin):
    list_display = ('task_schedule_name',)
    
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name',)
    
class UserTaskAdmin(admin.ModelAdmin):
    list_display = ('user','task')

admin.site.register(TaskSchedule, TaskScheduleAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(UserTask, UserTaskAdmin)
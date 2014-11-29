from django.contrib import admin
from django import forms
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse

from taskmng.models import *

class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ('task_category_name',)
    
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name',)
    
class UserTaskAdmin(admin.ModelAdmin):
    list_display = ('user','task')

admin.site.register(TaskCategory, TaskCategoryAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(UserTask, UserTaskAdmin)
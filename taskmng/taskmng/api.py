from django.contrib.auth.models import User, Group

from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization

from taskmng.models import *

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		authorization = DjangoAuthorization()
		authentication = BasicAuthentication()
		fields = ['id', 'username', 'first_name', 'last_name', 'last_login', 'email', 'is_staff', 'is_superuser']

class TaskScheduleResource(ModelResource):
	class Meta:
		queryset = TaskSchedule.objects.all()
		resource_name = 'task_schedule'
		authorization = Authorization()

class TaskResource(ModelResource):
	task_schedule = fields.ForeignKey(TaskScheduleResource, 'task_schedule', full=True, null=True)

	def dehydrate_task_category(self, bundle):
		return bundle.obj.get_task_category_display()

	class Meta:
		queryset = Task.objects.all()
		resource_name = 'task'
		authorization = Authorization()
		filtering = {
			'task_schedule':ALL
		}

class AttachmentResource(ModelResource):
	task = fields.ForeignKey(TaskResource, 'task', full=True)

	def dehydrate_attachment_type(self, bundle):
		return bundle.obj.get_attachment_type_display()

	class Meta:
		queryset = Attachment.objects.all()
		authorization = Authorization()
		resource_name = 'attachment'

class UserTaskResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user', full=True)
	task = fields.ForeignKey(TaskResource, 'task', full=True)

	def dehydrate_task_status(self, bundle):
		return bundle.obj.get_task_status_display()

	class Meta:
		queryset = UserTask.objects.all()
		authorization = Authorization()
		resource_name = 'user_task'
		filtering = {
			'user':ALL,
			'task':ALL,
		}
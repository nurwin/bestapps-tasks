from string import upper

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.conf.urls import url
from django.http import HttpResponse

from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization

from taskmng.models import *

class CORSResource(object):
    """
    Adds CORS headers to resources that subclass this.
    """
    def create_response(self, *args, **kwargs):
        response = super(CORSResource, self).create_response(*args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Content-Type'

        return response

    def method_check(self, request, allowed=None):
        if allowed is None:
            allowed = []

        request_method = request.method.lower()
        allows = ','.join(map(str.upper, allowed))

        if request_method == 'options':
            response = HttpResponse(allows)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        if not request_method in allowed:
            response = http.HttpMethodNotAllowed(allows)
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        return request_method

class UserResource(CORSResource, ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		authorization = DjangoAuthorization()
		authentication = BasicAuthentication()
		list_allowed_methods = ['get', 'post']
		detail_allowed_methods = ['get', 'patch', 'put', 'post', 'delete']
		fields = ['id', 'username', 'first_name', 'last_name', 'last_login', 'email', 'is_staff', 'is_superuser']
		filtering={
			'username':ALL_WITH_RELATIONS,
			'first_name':ALL_WITH_RELATIONS,
			'last_name':ALL_WITH_RELATIONS,
			'email':ALL_WITH_RELATIONS

		}

	def prepend_urls(self):
		return [
			url(r"^(?P<resource_name>%s)/login%s$" %
				(self._meta.resource_name, trailing_slash()),
				self.wrap_view('login'), name="api_login"),
			url(r'^(?P<resource_name>%s)/logout%s$' %
				(self._meta.resource_name, trailing_slash()),
				self.wrap_view('logout'), name='api_logout'),
		]

	def obj_create(self, bundle, **kwargs):
		REQUIRED_FIELDS = ('username', 'email', 'password')
		for field in REQUIRED_FIELDS:
			if field not in bundle.data:
				raise CustomBadRequest(
					code='missing_key',
					message=('Must provide {missing_key} when creating a'
								' user.').format(missing_key=field))

		email = bundle.data['email']
		try:
			if User.objects.filter(email=email):
				raise CustomBadRequest(
					code='duplicate_exception',
					message='That email is already associated with some user.')
		except User.DoesNotExist:
			pass

		username, password, email = bundle.data['username'], bundle.data['password'], bundle.data['email']
		
		try:
			bundle.obj = User.objects.create_user(username, email, password)
		except IntegrityError:
			raise BadRequest('That username already exists')
		return bundle

	def login(self, request, **kwargs):
		self.method_check(request, allowed=['post'])

		data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

		username = data.get('username', '')
		password = data.get('password', '')

		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				response = request.auth.HTTPBasicAuth(username, password)
				return self.create_response(request, {
						'success': True,
						'key': response
				})
			else:
				return self.create_response(request, {
					'success': False,
					'reason': 'disabled',
				}, HttpForbidden )
		else:
			return self.create_response(request, {
				'success': False,
				'reason': 'incorrect',
				}, HttpUnauthorized )

	def logout(self, request, **kwargs):
		self.method_check(request, allowed=['get'])
		if request.user and request.user.is_authenticated():
			logout(request)
			return self.create_response(request, { 'success': True })
		else:
			return self.create_response(request, { 'success': False }, HttpUnauthorized)

class TaskScheduleResource(CORSResource, ModelResource):
	class Meta:
		queryset = TaskSchedule.objects.all()
		resource_name = 'task_schedule'
		authorization = DjangoAuthorization()
		authentication = BasicAuthentication()

class TaskResource(ModelResource):
	task_schedule = fields.ForeignKey(TaskScheduleResource, 'task_schedule', full=True, null=True)

	def dehydrate_task_category(self, bundle):
		return bundle.obj.get_task_category_display()

	class Meta:
		queryset = Task.objects.all()
		resource_name = 'task'
		authorization = DjangoAuthorization()
		authentication = BasicAuthentication()
		filtering = {
			'task_schedule':ALL,
			'task_name' :ALL,
			'task_category' :ALL,

		}

class AttachmentResource(ModelResource):
	task = fields.ForeignKey(TaskResource, 'task', full=True)

	def dehydrate_attachment_type(self, bundle):
		return bundle.obj.get_attachment_type_display()

	class Meta:
		queryset = Attachment.objects.all()
		authorization = DjangoAuthorization()
		authentication = BasicAuthentication()
		resource_name = 'attachment'

class UserTaskResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user', full=True)
	task = fields.ForeignKey(TaskResource, 'task', full=True)

	def dehydrate_task_status(self, bundle):
		return bundle.obj.get_task_status_display()

	class Meta:
		queryset = UserTask.objects.all()
		authorization = DjangoAuthorization()
		authentication = BasicAuthentication()
		resource_name = 'user_task'
		filtering = {
			'user':ALL,
			'task':ALL,
			'task_status':ALL
		}
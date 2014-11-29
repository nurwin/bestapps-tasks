from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from taskmng.api import *

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(TaskCategoryResource())
v1_api.register(AttachmentResource())
v1_api.register(TaskResource())
v1_api.register(UserTaskResource())


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'taskmng.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls)),
)

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from account.views import *
from request.views import *
schema_view = get_swagger_view(title='ShareX')
router = DefaultRouter()

router.register(r'login', UserLoginViewSet)
router.register(r'register',UserRegisterViewSet)
router.register(r'logout',UserLogoutViewSet)
router.register(r'test',test_Token)

router.register(r'get_request',get_request)
# router.register(r'gentoken',gen_token)
# router.register(r'logout',UserLogoutViewSet)

urlpatterns = [
    url(r'^api/$', schema_view),
    #url(r'^test/$', test_Token),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    # url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/successfully_logged_out/'})
]

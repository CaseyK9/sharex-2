from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from account.views import *
from request.views import *
from car.views import *
from travel.views import *
from matching.views import *
#from upload.views import *

schema_view = get_swagger_view(title='ShareX')
router = DefaultRouter()

router.register(r'login', UserLoginViewSet)
router.register(r'register',UserRegisterViewSet)
router.register(r'logout',UserLogoutViewSet)

router.register(r'test',test_Token)

router.register(r'get-request',GetRequestViewSet)
router.register(r'get-travel',GetTravelViewSet)
router.register(r'get-matching-detail',GetMatching_Detail)
router.register(r'get-multiple-matching',Get_Multiple_Matching)
router.register(r'update-station',Update_Matching_Station)
router.register(r'store-route-url',Store_Route_Url)

#router.register(r'get-list-match',GetList_Match_ViewSet)
router.register(r'get-request-detail',Get_Request_Detail)
router.register(r'get-account-detail',Get_Account_Detail)
router.register(r'get-request-history',Get_Request_History)
router.register(r'edit-profile',Edit_Profile)
router.register(r'cancel-request',Cancel_Request)

router.register(r'get-list-travel',GetTravel_List)
router.register(r'matching',GetMatchViewSet)
router.register(r'add-car',add_car)

router.register(r'make-it-done',Make_It_Done)
#router.register(r'upload-img',FileView)

# router.register(r'gentoken',gen_token)
# router.register(r'logout',UserLogoutViewSet)

urlpatterns = [
    url(r'^api/$', schema_view),
    #url(r'^test/$', test_Token),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    # url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/successfully_logged_out/'})
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

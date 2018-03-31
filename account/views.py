from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication,BasicAuthentication, SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied, NotAuthenticated
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from .models import Account
from matching.models import Matching
#from .authenticate import CsrfExemptSessionAuthentication
from .serializers import *
from .permissions import IsAuthenticated


class UserLoginViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = Account.objects.all()
    allow_redirects = True
    authentication_classes = (BasicAuthentication,TokenAuthentication)
    serializer_class = UserLogInSerializer

    def create(self, request, *args, **kwargs):
        import re
        if request.user.is_authenticated():
            raise PermissionDenied('Please logout.')

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email', None)
            password = serializer.data.get('password')

            email_regex = re.compile(r'[^@]+@[^@]+\.[^@]+')
            if email_regex.match(email):
                msg = 'This email or password is not valid.'
            else:
                msg = 'This email is wrong format'

            user = authenticate(email=email, password=password)
            if not user:
                raise AuthenticationFailed(msg)

            login(request, user)
            #request.session['email'] = email;
            #request.session.set_expiry(3153600000)

            # response = UserAccountSerializer(user).data
            obj = Token.objects.get(user=user)
            detail = []
            if user.status == "busy":
                for i in Matching.objects.all():
                    if i.travel_data.account == request.user:
                        detail.append({'matching_id':i.pk})
                
            
            return Response({'Token':obj.key,'is_driver':str(user.is_driver),'acoount_status':str(user.status),'acount_id':str(user.pk),'detail':detail}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            account = Account.objects.create_user(
                email=serializer.data['email'],
                first_name=serializer.data['first_name'],
                last_name=serializer.data['last_name'],
                tel=serializer.data['tel'],
                address=serializer.data['address'],
                is_driver=serializer.data['is_driver'],
                personal_id=serializer.data['personal_id'],
                license=serializer.data['license'],
                #status = serializer.data['status']
            )
            account.set_password(serializer.data['password'])
            account.save()
            return JsonResponse({'error':'false','content':'success'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = UserLogoutSerializer
    permission_classes = (IsAuthenticated, )

    def create(self,request):
        if request.user.is_authenticated():
            logout(request)
            return Response("loged out", status=status.HTTP_200_OK)
        else :
            return Response("Unauthenticated")


class test_Token(mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = testSerializer
    def create(self,request):
        if request.user.is_authenticated():
            return Response(request.user.email)
        else :
            return Response("Unauthenticated")


# class gen_token(mixins.CreateModelMixin,viewsets.GenericViewSet):
#     queryset = Account.objects.all()
#     serializer_class = genSerializer
#     for user in Account.objects.all():
#         Token.objects.get_or_create(user=user)
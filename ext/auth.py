from rest_framework.authentication import BaseAuthentication
from reservation.models import User 

class QueryParamsAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('openid')
        if not token:
            return
        user_object = User.objects.filter(username=token).first()
        if user_object:
            return user_object,token
    def authenticate_header(self, request):
        return 'token'

class HeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return
        user_object = User.objects.filter(username=token).first()
        if user_object:
            return user_object,token
    def authenticate_header(self, request):
        return 'token'
    
    
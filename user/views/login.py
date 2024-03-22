import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import MyTokenObtainPairSerializer
from rest_framework import permissions


class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class WXLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        res = {
            'code': 200,
            'msg': 'success',
            'date': {}
        }
        code = request.GET.get('code')  # 从前端获取code
        # 向微信API发送请求，获取用户信息等操作
        wx_api_url = 'https://api.weixin.qq.com/sns/jscode2session'
        params = {
            'appid': 'wxbb790dfebfba6b18',
            'secret': '92ad213ff31f718a3ab140beb3db90f8',
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        response = requests.get(wx_api_url, params=params)
        data = response.json()
        print(data)
        # 处理获取到的用户信息
        res['data'] = data
        # 对用户进行认证和管理操作
        # 返回相应的信息给前端
        return Response(res)
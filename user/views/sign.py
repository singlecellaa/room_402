from rest_framework.views import APIView
from room_app.models import User
from rest_framework.response import Response


class SignView(APIView):
    permission_classes = []

    def post(self, request):
        res = {
            'code': 500,
            'msg': '注册成功',
            'data': []
        }

        username = request.data.get('username')
        password = request.data.get('password')
        re_password = request.data.get('re_password')
        if password != re_password:
            res['msg'] = '两次密码输入不一致'
            return Response(res)

        user = User.objects.filter(username=username)
        if user:
            res['msg'] = '该用户名已存在'
            return Response(res)

        User.objects.create_user(username=username, password=password)

        res['code'] = 200
        return Response(res)

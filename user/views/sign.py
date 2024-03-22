from rest_framework.views import APIView
from reservation.models import User
from rest_framework.response import Response


class SignView(APIView):
    permission_classes = []

    def post(self, request):
        res = {
            'code': 500,
            'msg': '填写成功',
            'data': []
        }

        name = request.data.get('name')
        user_id = request.data.get('user_id')
        student_id = request.data.get('student_id')
        depart_id = request.data.get('depart_id')
        club_id = request.data.get('club_id')

        user_query = User.objects.filter(id=user_id)

        user_query.update(name=name, student_id=student_id, depart_id=depart_id, club_id=club_id)
        res['code'] = 200
        return Response(res)

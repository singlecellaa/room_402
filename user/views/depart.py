from rest_framework.views import APIView
from rest_framework.response import Response
from reservation.models import Depart
from rest_framework import permissions


class DepartView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self,request):
        res = {
            'code': 500,
            'msg': 'success',
            'data': []
        }

        depart_list = Depart.objects.all()
        for depart in depart_list:
            res['data'].append({
                'id': depart.id,
                'name': depart.name
            })

        return Response(res)
from rest_framework.views import APIView
from rest_framework.response import Response
from reservation.models import Club
from rest_framework import permissions


class ClubView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self):
        res = {
            'code': 500,
            'msg': 'success',
            'data': []
        }

        club = Club.objects.all()
        for cl in club:
            res['data'].append({
                'id': cl.id,
                'name': cl.name
            })

        return Response(res)
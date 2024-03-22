from rest_framework.views import APIView
from rest_framework.response import Response
from reservation.models import Club
from rest_framework import permissions


class ClubView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        res = {
            'code': 500,
            'msg': 'success',
            'data': []
        }
        depart_id = request.GET.get('depart_id')
        club = Club.objects.filter(depart_id=depart_id)
        for cl in club:
            res['data'].append({
                'id': cl.id,
                'name': cl.name
            })

        return Response(res)
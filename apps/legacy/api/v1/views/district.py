from django.db.models import F
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.legacy.models import YearToDistMapping


class DistrictRankingApiView(APIView):

    def get(self, request):
        d = YearToDistMapping.objects.values(
            'district',
            district_fips=F('dist_fips')
        )
        data = {
            'data': d
        }
        return Response(data=data)

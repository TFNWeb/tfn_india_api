from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from apps.legacy.models import PDistrictRanking


class DistrictRankingApiView(APIView):

    def get(self, request):
        year = request.query_params.get('year')
        # need to format error message
        if not year:
            raise ValidationError({
                "detail": {
                    'query_params': {
                        'year': "Year is required"
                    }
                }
            })
        rows = PDistrictRanking.objects.filter(year=year).values('year',
                                                                 'state_abbr',
                                                                 'district_fips',
                                                                 'ranking',
                                                                 'percentage').order_by('state_abbr', 'ranking')

        if not rows:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                'detail': "Data Not Available"
            })
        # Group rows by state abbreviation
        grouped_rows = {}
        for row in rows:
            state_abbr = row['state_abbr']
            if state_abbr not in grouped_rows:
                grouped_rows[state_abbr] = []
            grouped_rows[state_abbr].append({
                'district_fips': row['district_fips'],
                'ranking': row['ranking'],
                'percentage': row['percentage']
            })
        data = grouped_rows
        return Response(data=data)

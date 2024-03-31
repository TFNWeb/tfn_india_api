from django.urls import path

from apps.legacy.api.v1.views import DistrictRankingApiView

urlpatterns = [
    path('district-rankings/', DistrictRankingApiView.as_view())
]

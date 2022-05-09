from django.urls import path
from rest_framework.routers import DefaultRouter

from fun_fact.views import DatesCreateListDestroy

router = DefaultRouter()
router.register(r'dates', DatesCreateListDestroy, basename='date')

app_name = 'fun_fact'

urlpatterns = [
    # path(r'rate/', CarRatingCreateAPIView.as_view(), name='rate'),
    # path(r'popular/', PopularCarListAPIView.as_view(), name='popular'),
    # path(r'cars_by_make/', AllCarsByMakeAPIView.as_view(), name="cars_by_make")
]

urlpatterns += router.urls
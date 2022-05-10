from django.urls import path
from rest_framework.routers import DefaultRouter

from fun_fact.views import DatesCreateListDestroy, PopularDateListAPIView

router = DefaultRouter()
router.register(r'dates', DatesCreateListDestroy, basename='date')

app_name = 'fun_fact'

urlpatterns = [
    path(r'popular', PopularDateListAPIView.as_view(), name='popular'),
]

urlpatterns += router.urls
from django.urls import path
from rest_framework.routers import DefaultRouter

from fun_fact.views import FactDateCreateListDestroy, PopularDateListAPIView

router = DefaultRouter()
router.register(r'fact_dates', FactDateCreateListDestroy, basename='fact_dates')

app_name = 'fun_fact'

urlpatterns = [
    path(r'popular', PopularDateListAPIView.as_view(), name='popular'),
]

urlpatterns += router.urls
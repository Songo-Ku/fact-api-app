from django.urls import path
from rest_framework.routers import DefaultRouter

from fun_fact.views import FactDateCreateListDestroy, PopularDateListViewSet
# PopularDateListAPIView

router = DefaultRouter()
router.register(r'dates', FactDateCreateListDestroy, basename='dates')
router.register(r'popular', PopularDateListViewSet, basename='popular')

app_name = 'fun_fact'

urlpatterns = [
]

urlpatterns += router.urls
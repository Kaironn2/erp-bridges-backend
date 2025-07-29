from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BuyOrderViewSet, CustomerViewSet

app_name = 'mgt_v1'

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'buyorders', BuyOrderViewSet, basename='buyorder')

urlpatterns = [
    path('', include(router.urls))
]

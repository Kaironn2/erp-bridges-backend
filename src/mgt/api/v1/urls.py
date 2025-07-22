from django.urls import include
from rest_framework.routers import DefaultRouter

from .views import CustomerViewSet

app_name = 'v1'

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    '', include(router.urls)
]

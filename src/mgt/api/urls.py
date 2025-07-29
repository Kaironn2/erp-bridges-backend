from django.urls import include, path

urlpatterns = [
    path('v1/mgt/', include('mgt.api.v1.urls'))
]

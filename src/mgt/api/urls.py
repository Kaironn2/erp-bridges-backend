from django.urls import include, path

urlpatterns = [
    path('mgt/', include('mgt.api.v1.urls'))
]

from django.urls import include, path

urlpatterns = [
    path('v1/', include('reports.api.v1.urls', namespace='v1')),
]

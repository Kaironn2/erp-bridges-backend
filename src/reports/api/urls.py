from django.urls import include, path

urlpatterns = [
    path('v1/reports/', include('reports.api.v1.urls')),
]

from django.urls import include, path

urlpatterns = [
    path('reports/', include('reports.api.v1.urls')),
]

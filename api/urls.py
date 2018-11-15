from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .engine.views import index_view, FilterListAPIView

router = routers.DefaultRouter()
router.register('filters', FilterListAPIView, base_name='filters')

urlpatterns = [

    # http://localhost:8000/
    path('', index_view, name='index'),

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include(router.urls)),

    # http://localhost:8000/api/admin/
    path('api/admin/', admin.site.urls),
]

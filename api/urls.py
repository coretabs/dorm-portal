from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .engine import views as engine_views

router = routers.DefaultRouter()
router.register('locale', engine_views.LocaleListViewSet, base_name='locale')
router.register('filters', engine_views.FiltersListViewSet, base_name='filters')
router.register('dorms', engine_views.DormViewSet, base_name='dorms')

urlpatterns = [

    # http://localhost:8000/
    path('', engine_views.index_view, name='index'),

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include(router.urls)),

    # http://localhost:8000/api/admin/
    path('api/admin/', admin.site.urls),
]

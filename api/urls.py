from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from rest_framework_nested import routers

from .engine import views as engine_views

router = routers.DefaultRouter()
router.register('locale', engine_views.LocaleListViewSet, base_name='locale')
router.register('filters', engine_views.FiltersListViewSet, base_name='filters')
router.register('dorms', engine_views.DormViewSet, base_name='dorms')
router.register('manager-dorms', engine_views.DormManagementViewSet, base_name='manager-dorms')

# for url in router.urls:
#    print(url.__dict__)


dorms_router = routers.NestedSimpleRouter(router, 'manager-dorms', lookup='dorm')
dorms_router.register('bank_accounts', engine_views.BankAccountManagementViewSet,
                      base_name='bank-accounts')
dorms_router.register('photos', engine_views.PhotoDormManagementViewSet,
                      base_name='photos')

urlpatterns = [

    # http://localhost:8000/
    path('', engine_views.index_view, name='index'),

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include((router.urls, 'engine'), namespace='engine')),
    #path('api/manager', include((manager_router.urls, 'engine'), namespace='engine')),
    path('api/dorms', include((dorms_router.urls, 'engine'), namespace='engine.dorms')),

    # http://localhost:8000/api/admin/
    path('api/admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

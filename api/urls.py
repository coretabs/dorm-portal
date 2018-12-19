from django.contrib import admin
from django.contrib.auth.views import PasswordResetConfirmView

from django.conf.urls.static import static
from django.conf import settings

from django.urls import path, include

from rest_framework_nested import routers

from .engine import views as engine_views

router = routers.DefaultRouter()
router.register('locale', engine_views.LocaleListViewSet, base_name='locale')
router.register('filters', engine_views.FiltersListViewSet, base_name='filters')
router.register('reservations', engine_views.ReservationViewSet, base_name='reservations')
router.register('dorms', engine_views.DormViewSet, base_name='dorms')
router.register('manager-dorms', engine_views.DormManagementViewSet, base_name='manager-dorms')

# for url in router.urls:
#    print(url.__dict__)

reservations_router = routers.NestedSimpleRouter(router, 'reservations', lookup='reservation')
reservations_router.register('receipts', engine_views.ReceiptViewSet,
                             base_name='receipts')

dorms_router = routers.NestedSimpleRouter(router, 'manager-dorms', lookup='dorm')
dorms_router.register('bank_accounts', engine_views.BankAccountManagementViewSet,
                      base_name='bank-accounts')
dorms_router.register('photos', engine_views.PhotoDormManagementViewSet,
                      base_name='photos')
dorms_router.register('reservations', engine_views.ReservationManagementViewSet,
                      base_name='reservations')

urlpatterns = [

    # http://localhost:8000/
    path('', engine_views.index_view, name='index'),

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include((router.urls, 'engine'), namespace='engine')),
    #path('api/manager', include((manager_router.urls, 'engine'), namespace='engine')),
    path('api/dorms', include((dorms_router.urls, 'engine'), namespace='engine.dorms')),
    path('api/', include((reservations_router.urls, 'engine'), namespace='engine.reservations')),

    path('api/auth/', include('rest_auth.urls')),
    #path(r'^', include('django.contrib.auth.urls')),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView, name='password_reset_confirm'),
    path('api/auth/registration/', include('rest_auth.registration.urls')),
    path('api/auth/resend-confirmation/',
         engine_views.ResendConfirmView.as_view(), name='resend_confirm_view'),

    # http://localhost:8000/api/admin/
    path('api/admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

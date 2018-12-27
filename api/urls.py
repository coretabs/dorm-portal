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

manager_dorms_router = routers.NestedSimpleRouter(router, 'manager-dorms', lookup='dorm')
manager_dorms_router.register('bank-accounts', engine_views.BankAccountManagementViewSet,
                              base_name='bank-accounts')
manager_dorms_router.register('photos', engine_views.PhotoDormManagementViewSet,
                              base_name='photos')
manager_dorms_router.register('reservations', engine_views.ReservationManagementViewSet,
                              base_name='reservations')
manager_dorms_router.register('rooms', engine_views.RoomManagementViewSet,
                              base_name='rooms')

manager_rooms_router = routers.NestedSimpleRouter(
    manager_dorms_router, 'rooms', lookup='room')
manager_rooms_router.register('photos', engine_views.PhotoRoomManagementViewSet,
                              base_name='photos')

urlpatterns = [

    # http://localhost:8000/
    path('', engine_views.index_view, name='index'),

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include((router.urls, 'engine'), namespace='engine')),
    #path('api/manager', include((manager_router.urls, 'engine'), namespace='engine')),
    path('api/', include((reservations_router.urls, 'engine'), namespace='engine.reservations')),
    path('api/', include((manager_dorms_router.urls, 'engine'), namespace='engine.manager-dorms')),
    path('api/', include((manager_rooms_router.urls, 'engine'), namespace='engine.manager-dorms.rooms')),

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

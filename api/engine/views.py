from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.utils import translation
from django.conf import settings

from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response

from .exceptions import (NoEnoughQuotaException, NonFinishedUserReservationsException,
                         NonUpdatableReservationException, NonReviewableReservation)
from . import serializers
from . import models


# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


def activate_language(language):
    if language not in settings.LANGUAGES_DICT:
        language = 'en'
    translation.activate(language)


class ResendConfirmView(generics.GenericAPIView):

    serializer_class = serializers.ResendConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response({'detail': "Email confirmation sent"})


class LocaleListViewSet(viewsets.ViewSet):
    serializer_class = serializers.LocaleSerailizer

    def list(self, request):
        return Response(self.serializer_class([]).data)


class FiltersListViewSet(viewsets.ViewSet):
    serializer_class = serializers.ClientReturnedFiltersSerializer

    def list(self, request):
        activate_language(request.query_params.get('language', 'en'))

        return Response(self.serializer_class([]).data)


class DormViewSet(viewsets.ViewSet):

    def create(self, request):
        """
        It's not actually creating anything, it's just filtering
        But drf doesn't allow changing the action of list ViewSet
        """

        activate_language(request.data.get('language', 'en'))

        deserialized_filters = serializers.ClientAcceptedFiltersSerializer(data=request.data)
        deserialized_filters.is_valid()

        filtered_dorms = models.Dormitory.objects\
            .superfilter(
                category_id=deserialized_filters.data.get('category_selected_option_id', None),
                duration_option_id=deserialized_filters.data.get('duration_option_id', None),
                dorm_features_ids=deserialized_filters.data.get('dorm_features', None),
                radio_integeral_choices=deserialized_filters.data.get('additional_filters', None),
                room_features_ids=deserialized_filters.data.get('room_features', None),
                to_currency=request.data.get('currency', 'USD'))\
            .with_reviews_statistics()\

        # print(filtered_dorms)

        return Response(serializers.DormSerializer(filtered_dorms, many=True).data)

    def retrieve(self, request, pk=None):
        activate_language(request.query_params.get('language', 'en'))

        dorm = models.Dormitory.objects.filter(id=pk)\
            .superfilter(to_currency=request.data.get('currency', 'USD'))\
            .with_last_3_reviews()\
            .with_reviews_statistics()\
            .first()

        return Response(serializers.DormDetailsSerializer(dorm).data)

    def reviews(self, request, pk):
        reviews = models.Dormitory.objects.get(pk=pk).reviews
        return Response(serializers.ReviewSerializer(reviews, many=True).data)


class HisOwnDormitoryObject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_owner(request.user)


class HisOwnDormitoryChildObjects(BasePermission):
    def has_permission(self, request, view):
        return models.Dormitory.objects.get(pk=view.kwargs['dorm_pk']).manager == request.user


class RoomManagementViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, HisOwnDormitoryChildObjects)

    def get_queryset(self):
        return models.RoomCharacteristics.objects.filter(dormitory__id=self.kwargs['dorm_pk'])

    def list(self, request, dorm_pk):
        rooms = self.get_queryset().with_reserved_rooms_number()

        return Response(serializers.DormManagementRoomStatisticsSerializer(rooms, many=True).data)

    def retrieve(self, request, dorm_pk, pk):
        room = models.RoomCharacteristics.objects.with_all_filters_and_choices(pk)

        return Response(serializers.DormManagementRoomDetailsSerializer(room).data)

    def create(self, request, dorm_pk):
        serializer = serializers.DormManagementNewRoomSerializer(
            data=request.data, context={'dorm_pk': dorm_pk})

        serializer.is_valid()
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, dorm_pk, pk):
        room = self.get_queryset().get(pk=pk)

        serializer = serializers.DormManagementEditRoomSerializer(
            room, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, dorm_pk, pk):
        """reservation = self.get_queryset().get(pk=pk)

        serializer = serializers.ClientReservationManagementSerializer(
            reservation, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)"""


class ReservationManagementViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, HisOwnDormitoryChildObjects)
    serializer_class = serializers.ClientReservationManagementSerializer

    def get_queryset(self):
        return models.Reservation.objects.filter(
            room_characteristics__dormitory__id=self.kwargs['dorm_pk'])

    def list(self, request, dorm_pk):
        reservations = self.get_queryset()

        result = reservations.status_statistics()
        result['reservations'] = reservations

        return Response(serializers.ReservationManagementSerializer(result).data)

    def update(self, request, dorm_pk, pk):
        reservation = self.get_queryset().get(pk=pk)

        serializer = serializers.ClientReservationManagementSerializer(
            reservation, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='ask-review')
    def ask_review(self, request, dorm_pk, pk):
        serializer = serializers.AskForReviewSerializer(
            data={'reservation_id': pk}, context={'request': request})

        serializer.is_valid()
        serializer.save()

        return Response()


class BankAccountManagementViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, HisOwnDormitoryChildObjects)
    serializer_class = serializers.ClientBankAccountSerializer

    def get_queryset(self):
        return models.BankAccount.objects.filter(dormitory=self.kwargs['dorm_pk'])


class PhotoDormManagementViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, HisOwnDormitoryChildObjects)
    serializer_class = serializers.ClientPhotoDormSerializer

    def get_queryset(self):
        return models.DormitoryPhoto.objects.filter(dormitory=self.kwargs['dorm_pk'])


class DormManagementViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = (IsAuthenticated, )
        else:
            self.permission_classes = (IsAuthenticated, HisOwnDormitoryObject, )

        return super().get_permissions()

    def list(self, request):
        dorms = request.user.dormitories
        return Response(serializers.DormManagementSerializer(dorms, many=True).data)

    def retrieve(self, request, pk=None):
        dorm = models.Dormitory.objects.get(pk=pk)
        self.check_object_permissions(request, dorm)

        return Response(serializers.DormManagementDetailsSerializer(dorm).data)

    def update(self, request, pk=None):
        dorm = models.Dormitory.objects.get(pk=pk)
        self.check_object_permissions(request, dorm)

        serializer = serializers.ClientDormManagementSerializer(
            dorm, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()

        return Response()

    @action(detail=True, methods=['put'], url_path='update-cover')
    def update_cover(self, request, pk=None):
        return self.update(request, pk)

    @action(detail=False, methods=['get'], url_path='filters')
    def filters(self, request):
        return Response(serializers.DormManagementRoomFiltersSerializer([]).data)


class HisOwnReservation(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_owner(request.user)


class ReceiptViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, HisOwnReservation)
    serializer_class = serializers.ReceiptSerializer

    def get_queryset(self):
        return models.ReceiptPhoto.objects.filter(reservation=self.kwargs['reservation_pk'])

    def create(self, request, reservation_pk=None):
        reservation = models.Reservation.objects.get(pk=self.kwargs['reservation_pk'])
        self.check_object_permissions(request, reservation)

        serializer = serializers.ReceiptSerializer(
            data=request.data, context={'reservation_pk': reservation_pk})
        serializer.is_valid()

        try:
            result = serializer.save()
            response = Response(status=status.HTTP_201_CREATED)

        except (NonUpdatableReservationException) as exception:
            response = Response(str(exception), status=status.HTTP_400_BAD_REQUEST)

        return response


class ReservationViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, HisOwnReservation)

    def create(self, request):
        serializer = serializers.ClientAcceptedReservationSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid()

        try:
            result = serializer.save()
            reservation = models.Reservation.objects.get(pk=result.id)
            response = Response(serializers.ReservationDetailsSerializer(reservation).data,
                                status=status.HTTP_201_CREATED)

        except (NoEnoughQuotaException, NonFinishedUserReservationsException) as exception:
            response = Response(str(exception), status=status.HTTP_400_BAD_REQUEST)

        return response

    def retrieve(self, request, pk=None):
        reservation = models.Reservation.objects.get(pk=pk).check_if_expired()
        self.check_object_permissions(request, reservation)

        return Response(serializers.ReservationDetailsSerializer(reservation).data)

    @action(detail=True, methods=['post'], url_path='add-review')
    def add_review(self, request, pk):
        reservation = models.Reservation.objects.get(pk=pk)
        self.check_object_permissions(request, reservation)

        try:
            serializer = serializers.ReviewSerializer(
                data=request.data, context={'reservation_id': pk})
            serializer.is_valid()
            serializer.save()
            response = Response(status=status.HTTP_201_CREATED)

        except NonReviewableReservation as exception:
            response = Response(str(exception), status=status.HTTP_400_BAD_REQUEST)

        return response

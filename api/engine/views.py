from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.utils import translation

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response

from api import settings

from . import serializers
from . import models


# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


class LocaleListViewSet(viewsets.ViewSet):
    serializer_class = serializers.LocaleSerailizer

    def list(self, request):
        return Response(self.serializer_class([]).data)


class FiltersListViewSet(viewsets.ViewSet):
    serializer_class = serializers.ClientReturnedFiltersSerializer

    def list(self, request):
        language = request.query_params.get('language', 'en')
        if language not in settings.LANGUAGES_DICT:
            language = 'en'

        translation.activate(language)

        return Response(self.serializer_class([]).data)


class DormViewSet(viewsets.ViewSet):
    serializer_class = serializers.DormSerializer

    def activate_language(self, request):
        language = request.data.get('language', 'en')
        if language not in settings.LANGUAGES_DICT:
            language = 'en'

        translation.activate(language)

    def list(self, request):
        self.activate_language(request)

        deserialized_filters = serializers.ClientAcceptedFiltersSerializer(data=request.data)
        deserialized_filters.is_valid()

        filtered_dorms = models.Dormitory.objects\
            .superfilter(
                category_id=deserialized_filters.data.get(
                    'category_selected_option_id', None),
                duration_option_id=deserialized_filters.data.get(
                    'duration_option_id', None),
                dorm_features_ids=deserialized_filters.data.get(
                    'dorm_features', None),
                radio_integeral_choices=deserialized_filters.data.get(
                    'additional_filters', None),
                room_features_ids=deserialized_filters.data.get(
                    'room_features', None))

        # print(filtered_dorms)

        return Response(self.serializer_class(filtered_dorms, many=True).data)

    def retrieve(self, request, pk=None):
        self.activate_language(request)

        dorm = models.Dormitory.objects.filter(id=pk).superfilter().first()

        return Response(serializers.DormDetailsSerializer(dorm).data)

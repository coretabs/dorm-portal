from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response


from . import serializers
from . import models


# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


class FilterListAPIView(viewsets.ViewSet):
    serializer_class = serializers.FiltersSerializer

    def list(self, request):
        return Response(self.serializer_class([]).data)

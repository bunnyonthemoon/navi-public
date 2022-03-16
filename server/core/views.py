import json

from django.views.generic.base import TemplateView, View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.catalog import models as catalogModels
from apps.catalog import serializers as catalogSerializers
from apps.catalog.scripts import get_filter_values
from apps.content import models as content_models
from apps.content import serializers as content_serializers


class IndexPageView(TemplateView):

    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)


        settings = content_models.Settings.value()
        context['site_meta'] = {
            'description': settings.meta_description,
            'primary_color': settings.primary_color,
            'secondary_color': settings.secondary_color
        }
        context['settings'] = json.dumps(
            content_serializers.SettingsSerializer(
                settings).data)
        context['complexes'] = json.dumps(
            catalogSerializers.ComplexSerializer(
                catalogModels.Complex.objects.order_by('order')[:3], many=True).data)
        context['private'] = json.dumps(
            catalogSerializers.ComplexPrivateSerializer(
                catalogModels.ComplexPrivate.objects.order_by('order'), many=True).data)
        context['selections'] = json.dumps(
            catalogSerializers.SelectionSerializer(
                catalogModels.Tag.objects.filter(type__isnull=False), many=True).data)
        context['filter'] = json.dumps(get_filter_values())

        return self.render_to_response(context)

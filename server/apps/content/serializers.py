import json
from lib2to3.pytree import convert

from django.db.models import FloatField, Max, Min
from rest_framework import serializers

from . import models


class SettingsSerializer(serializers.Serializer):
    primary_color = serializers.ReadOnlyField()
    secondary_color = serializers.ReadOnlyField()

    instagram = serializers.ReadOnlyField()
    telegram = serializers.ReadOnlyField()
    phone = serializers.ReadOnlyField()
    address = serializers.ReadOnlyField()

    catalog = serializers.FileField()
    agreement = serializers.FileField()

    meta_description = serializers.ReadOnlyField()

    private_order = serializers.ReadOnlyField()
    budget_order = serializers.ReadOnlyField()
    type_order = serializers.ReadOnlyField()
    catalog_order = serializers.ReadOnlyField()

    main_title = serializers.ReadOnlyField()
    main_subtitle = serializers.ReadOnlyField()
    main_catalog_title = serializers.ReadOnlyField()
    main_catalog_text = serializers.ReadOnlyField()

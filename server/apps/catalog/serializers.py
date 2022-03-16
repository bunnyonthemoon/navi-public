import json
from lib2to3.pytree import convert

from django.db.models import FloatField, Max, Min
from rest_framework import serializers

from . import models


class DeveloperSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.Developer
        fields = [
            'id', 'name'
        ]


class TagSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    color = serializers.ReadOnlyField()


class LotSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    price = serializers.ReadOnlyField()
    rate = serializers.ReadOnlyField()
    floor = serializers.ReadOnlyField()

    trim = serializers.CharField()

    complex = serializers.SerializerMethodField()

    def get_complex(self, obj):
        return { 'id': obj.complex.id, 'name': obj.complex.name }


class PlanSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    area = serializers.ReadOnlyField()
    min_price = serializers.ReadOnlyField()
    max_price = serializers.ReadOnlyField()
    min_rate = serializers.ReadOnlyField()
    max_rate = serializers.ReadOnlyField()
    rooms = serializers.ReadOnlyField()
    property_type = serializers.ReadOnlyField()
    key = serializers.ReadOnlyField()

    image = serializers.ImageField()

    complex = serializers.SerializerMethodField()

    def get_complex(self, obj):
        return { 'id': obj.complex.id, 'name': obj.complex.name }


class ComplexSubwaySerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    duration = serializers.ReadOnlyField()

    def get_name(self, obj):
        return obj.subway.name
    def get_color(self, obj):
        return obj.subway.color

class ComplexRoomsStatsSerializer(serializers.Serializer):
    rooms = serializers.ReadOnlyField()
    min_price = serializers.FloatField()
    max_price = serializers.FloatField()
    min_rate = serializers.FloatField()
    max_rate = serializers.FloatField()
    min_area = serializers.FloatField()
    max_area = serializers.FloatField()


class ComplexMapSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    key = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    image = serializers.ImageField()
    coordinates = serializers.JSONField()
    min_price = serializers.FloatField()


class ComplexSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    deadline = serializers.ReadOnlyField()
    done = serializers.ReadOnlyField()
    address = serializers.ReadOnlyField()
    location = serializers.ReadOnlyField()
    key = serializers.ReadOnlyField()

    image = serializers.ImageField()

    property_type = serializers.JSONField()
    property_class = serializers.CharField()

    min_price = serializers.FloatField()
    max_price = serializers.FloatField()
    min_rate = serializers.FloatField()
    max_rate = serializers.FloatField()
    min_area = serializers.FloatField()
    max_area = serializers.FloatField()

    rooms_info = serializers.SerializerMethodField()
    lots_count = serializers.SerializerMethodField()

    subway = serializers.SerializerMethodField()

    def get_rooms_info(self, obj):
        return ComplexRoomsStatsSerializer(obj.complexroomsstats_set.all().order_by('rooms'), many=True).data
    def get_lots_count(self, obj):
        return obj.complexroomsstats_set.all().count()
    def get_subway(self, obj):
        return ComplexSubwaySerializer(obj.complexsubway_set.order_by('duration')[0]).data


class ComplexCatalogSerializer(ComplexSerializer):
    coordinates = serializers.JSONField()


class ComplexDetailSerializer(ComplexSerializer):
    presentation = serializers.FileField()

    coordinates = serializers.JSONField()
    floors = serializers.ReadOnlyField()
    ceilings = serializers.ReadOnlyField()
    lots_count_total = serializers.ReadOnlyField()
    description = serializers.ReadOnlyField()

    trim = serializers.CharField(source='get_trim_display')
    property_class = serializers.JSONField()
    territory = serializers.CharField(source='get_territory_display')

    developer = DeveloperSerializer('developer')

    lots = serializers.SerializerMethodField()
    plans = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    recommendations = ComplexCatalogSerializer(many=True)
    subways = serializers.SerializerMethodField()

    def get_lots(self, obj):
        return LotSerializer(obj.lot_set.all(), many=True).data

    def get_plans(self, obj):
        return PlanSerializer(obj.plan_set.all(), many=True).data

    def get_images(self, obj):
        return [image.image.url for image in obj.compleximage_set.all()]

    def get_subways(self, obj):
        return ComplexSubwaySerializer(
            obj.complexsubway_set.all().order_by('duration'), many=True).data


class ComplexPrivateSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField()
    description = serializers.CharField()
    image = serializers.ImageField()
    done = serializers.ReadOnlyField()
    deadline = serializers.ReadOnlyField()
    subway = serializers.SerializerMethodField()

    def get_subway(self, obj):
        complexes = obj.complexsubway_set.order_by('duration')
        return {'name': complexes[0].subway.name, 'color': complexes[0].subway.color} if complexes.count() > 0 else None


class SelectionSerializer(TagSerializer):
    description = serializers.ReadOnlyField()
    image = serializers.ImageField()

    type = serializers.ReadOnlyField()

    count = serializers.SerializerMethodField()
    complexes = serializers.SerializerMethodField()

    key = serializers.ReadOnlyField()
    order = serializers.ReadOnlyField()

    def get_count(self, obj):
        return obj.complex_set.count()

    def get_complexes(self, obj):
        return ComplexSerializer(obj.complex_set.order_by('order')[:3], many=True).data

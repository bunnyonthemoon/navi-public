from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'id', 'name', 'photo', 'status', 'about', 'vk', 'instagram',
            'telegram', 'facebook', 'twitter', 'email', 'qr'
        ]


class UserPrivateSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(source='date_joined')
    admin = serializers.SerializerMethodField()
    cards = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = UserSerializer.Meta.fields
        fields += [
            'created', 'admin', 'phone', 'cards', 'passport',
            'waiting_passport'
        ]

    def get_admin(self, obj):
        return obj.is_staff


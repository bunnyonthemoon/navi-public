import re
import uuid
from datetime import timedelta

from django.contrib.auth import authenticate, hashers, login, logout
from django.middleware.csrf import get_token
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.catalog import models as catalog_models
from core.scripts import json_response, send_email
from env import EMAIL, SERVER_URL

from . import models, scripts, serializers
from .permissions import forbidden_response


@api_view(['POST'])
def offer(request):
    name = request.data.get('name')
    email = request.data.get('email')
    offer_type = request.data.get('type')
    object_id = request.data.get('id')

    message = f'Имя: {name}\nEmail: {email}\n'

    if offer_type == 'complex':
        title = 'Заявка на комплекс'
        complex = catalog_models.Complex.objects.get(key=object_id)
        message += f'Название комплекса: {complex.name}\n'
        message += f'Ссылка на комплекс: {SERVER_URL}/complex/{complex.key}'
    elif offer_type == 'private':
        title = 'Запрос на закрытые продажи'
        complex = catalog_models.ComplexPrivate.objects.get(pk=object_id)
        message += f'Название комплекса: {complex.name}\n'
        message += f'Ссылка на комплекс в админке: {SERVER_URL}/admin/catalog/complexprivate/{complex.id}/change/'
    else:
        return Response({'status': False})

    send_email(EMAIL, title, message)

    return Response({'status': True})

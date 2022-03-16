import logging
import os
from pathlib import Path

from env import *

from .default_settings import *

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'webpack_loader',
    'rest_framework',
    'ckeditor',
    'image_optimizer',
    'apps.authentication',
    'apps.catalog',
    'apps.content',
]

OPTIMIZED_IMAGE_METHOD = 'pillow'

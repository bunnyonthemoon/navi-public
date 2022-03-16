from datetime import datetime

import requests
from django import forms
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import m2m_changed, pre_delete, pre_save
from image_optimizer.fields import OptimizedImageField

from core.scripts import get_address_info

PROPERTY_CLASSES = (
    ('Бизнес', 'Бизнес'),
    ('Премиум', 'Премиум'),
    ('Делюкс', 'Делюкс'),
)
TRIMS = (
    ('Без отделки', 'Без отделки'),
    ('Whitebox', 'Whitebox'),
    ('С отделкой', 'С отделкой'),
)
HOUSING_TYPES = (
    ('Жилая', 'Жилая'),
    ('Коммерческая', 'Коммерческая'),
)
TERRITORIES = (
    ('Открытая', 'Открытая'),
    ('Закрытая', 'Закрытая'),
)

PROPERTY_TYPES = (
    ('Квартира', 'Квартира'),
    ('Апартаменты', 'Апартаменты'),
    ('Пентхаус', 'Пентхаус'),
    ('Таунхаус', 'Таунхаус'),
    ('Особняк', 'Особняк'),
    ('Вилла', 'Вилла'),
    ('Офис', 'Офис'),
    ('Ритейл', 'Ритейл'),
)


def get_deadlines():
    deadlines = []
    year = datetime.now().year

    index = 0
    while index < 7:
        for qv in ['I', 'II', 'III', 'IV']:
            value = f'{qv} кв. {year + index}'
            deadlines.append((value, value))
        index = index + 1

    return deadlines


class ChoiceArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)


class Developer(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')

    class Meta:
        verbose_name = 'Застройщик'
        verbose_name_plural = 'Застройщики'

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    SELECTION_TYPES = (
        ('list', 'Список'),
        ('price', 'По бюджету'),
        ('type', 'По типу')
    )

    name = models.CharField(max_length=30, verbose_name='Название')
    color = models.CharField(max_length=20, verbose_name='Цвет', null=True, blank=True)
    image = models.FileField(upload_to='selections/', verbose_name='Изображение', null=True, blank=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    type = models.CharField(max_length=20, choices=SELECTION_TYPES, verbose_name='Тип подборки', null=True, blank=True)
    budget_rate = models.IntegerField(verbose_name='Минимальный р/м2 в подборке по бюджету', null=True, blank=True)

    key = models.CharField(max_length=30, verbose_name='Ключ в url', null=True, blank=True, unique=True)
    order = models.IntegerField(
        default=1,
        verbose_name='Порядок вывода',
        help_text='Чем выше порядок, тем ниже будет выводиться подборка. Номер 0 зафиксирован за фильтром и приветсивем, 10 - за закрытыми продажами, 100 - за блоком для скачивания каталога. Соответсвенно порядок выставляйте с учётом этих значений'
    )

    class Meta:
        verbose_name = 'Тег / подборка'
        verbose_name_plural = 'Теги / подборки'

    def __str__(self):
        return f'{self.name}'


class Subway(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название станции')
    color = models.CharField(max_length=25, verbose_name='Цвет ветки', null=True, blank=True)
    class Meta:
        verbose_name = 'Станция метро'
        verbose_name_plural = 'Станции метро'

    def __str__(self):
        return f'{self.name}'


class Complex(models.Model):

    name = models.CharField(max_length=30, verbose_name='Название')
    description = models.TextField(verbose_name='Описание комплекса')

    address = models.CharField(max_length=100, verbose_name='Адрес')
    coordinates = models.JSONField(verbose_name='Координаты', help_text='Два значения с плавающей точкой. Пример: 59.94003449148195, 30.314545145537842', null=True, blank=True)
    location = models.CharField(max_length=50, verbose_name='Рядом', help_text='Ориентир местности. Например станция метро', null=True, blank=True)

    image = OptimizedImageField(optimized_image_output_size=(400, 240),
                                optimized_image_resize_method='cover',
                                upload_to='complexes/',
                                verbose_name='Изображение')

    presentation = models.FileField(upload_to='complexes/presentation/', verbose_name='Презентация', null=True, blank=True)

    property_class = models.CharField(max_length=30, choices=PROPERTY_CLASSES, verbose_name='Тип недвижимости')
    property_type = ChoiceArrayField(models.CharField(max_length=20, choices=PROPERTY_TYPES), default=list, verbose_name='Тип недвижимости')

    deadline = models.CharField(max_length=20, verbose_name='Срок сдачи', null=True, blank=True, help_text='Можно не заполнять если сдан', choices=get_deadlines())
    done = models.BooleanField(default=False, verbose_name='Сдан')

    developer = models.ForeignKey(Developer, on_delete=models.SET_NULL, null=True, verbose_name='Застройщик')

    floors = models.CharField(max_length=20, verbose_name='Этажность')
    ceilings = models.CharField(max_length=20, verbose_name='Потолки')
    lots_count_total = models.IntegerField(verbose_name='Кол-во лотов (в общем)')
    lots_count = models.IntegerField(verbose_name='Кол-во лотов (в продаже)')

    trim = models.CharField(max_length=30, choices=TRIMS, verbose_name='Отделка')
    territory = models.CharField(max_length=30, choices=TERRITORIES, verbose_name='Территория')

    recommendations = models.ManyToManyField('catalog.Complex', verbose_name='Рекомендации', blank=True)
    tags = models.ManyToManyField(Tag, verbose_name='Теги', blank=True)

    order = models.IntegerField(default=0, verbose_name='Приоритет отображения', help_text='При более высоком приоритете, комплекс выводится первее в списках, чем его соседи. Пример: Комплексы с приоритетом 3 > приоритет 1 > приоритет 0')
    key = models.CharField(unique=True, max_length=30, verbose_name='Ключ в ссылке', help_text='Разрешены только латинские буквы, цифры, нижнее подчеркивание и тире. Пробелы использовать нельзя')

    created = models.DateTimeField(default=datetime.now)

    min_rate = models.IntegerField(default=0, verbose_name='Минимальное р/м2')
    max_rate = models.IntegerField(default=0, verbose_name='Максимальное р/м2')
    min_price = models.IntegerField(default=0, verbose_name='Минимальная цена лота (р)')
    max_price = models.IntegerField(default=0, verbose_name='Максимальная цена лота (р)')
    min_area = models.DecimalField(default=0, max_digits=6, decimal_places=2, verbose_name='Минимальная площадь (м2)')
    max_area = models.DecimalField(default=0, max_digits=6, decimal_places=2, verbose_name='Максимальная площадь (м2)')

    class Meta:
        verbose_name = 'Комплекс'
        verbose_name_plural = 'Комплексы'

    def update_stats(self):

        def get_value(lots, key, dir):
            query = models.Max(key) if dir == 'max' else models.Min(key)
            result = lots.aggregate(query)
            value = result[f'{key}__{dir}']
            return value

        plans = self.plan_set.all()

        self.min_price = get_value(plans, 'min_price', 'min')
        self.max_price = get_value(plans, 'max_price', 'max')
        self.min_rate = get_value(plans, 'min_rate', 'min')
        self.max_rate = get_value(plans, 'max_rate', 'max')
        self.min_area = get_value(plans, 'area', 'min')
        self.max_area = get_value(plans, 'area', 'max')


        for number in plans.values_list('rooms', flat=True):
            plans_with_rooms = plans.filter(rooms=number)
            stats = self.complexroomsstats_set.get_or_create(rooms=number)[0]

            stats.min_price = get_value(plans_with_rooms, 'min_price', 'min')
            stats.max_price = get_value(plans_with_rooms, 'max_price', 'max')
            stats.min_rate = get_value(plans_with_rooms, 'min_rate', 'min')
            stats.max_rate = get_value(plans_with_rooms, 'max_rate', 'max')
            stats.min_area = get_value(plans_with_rooms, 'area', 'min')
            stats.max_area = get_value(plans_with_rooms, 'area', 'max')

            stats.save()

        stats_rooms = self.complexroomsstats_set.all().values_list('rooms',
                                                                   flat=True)
        plans_rooms = plans.values_list('rooms', flat=True)
        empty_rooms = stats_rooms.difference(plans_rooms)

        self.complexroomsstats_set.filter(rooms__in=empty_rooms).delete()

        if self.tags.filter(type='price').count() > 0:
            self.tags.remove(*self.tags.filter(type='price'))
        try:
            budget_selection = Tag.objects.filter(type='price', budget_rate__lte=self.min_rate).order_by('-budget_rate')[0]
            self.tags.add(budget_selection)
        except:
            pass

        self.save()

        return
        def get_value(lots, key, dir):
            query = models.Max(key) if dir == 'max' else models.Min(key)
            result = lots.aggregate(query)
            value = result[f'{key}__{dir}']
            return value

        lots = self.lot_set.all()

        self.min_price = get_value(lots, 'price', 'min')
        self.max_price = get_value(lots, 'price', 'max')
        self.min_rate = get_value(lots, 'rate', 'min')
        self.max_rate = get_value(lots, 'rate', 'max')
        self.min_area = get_value(lots, 'area', 'min')
        self.max_area = get_value(lots, 'area', 'max')

        for number in lots.values_list('rooms', flat=True):
            lots_with_rooms = lots.filter(rooms=number)
            stats = self.complexroomsstats_set.get_or_create(rooms=number)[0]

            stats.min_price = get_value(lots_with_rooms, 'price', 'min')
            stats.max_price = get_value(lots_with_rooms, 'price', 'max')
            stats.min_rate = get_value(lots_with_rooms, 'rate', 'min')
            stats.max_rate = get_value(lots_with_rooms, 'rate', 'max')
            stats.min_area = get_value(lots_with_rooms, 'area', 'min')
            stats.max_area = get_value(lots_with_rooms, 'area', 'max')

            stats.save()

        stats_rooms = self.complexroomsstats_set.all().values_list(
            'rooms', flat=True)
        lots_rooms = lots.values_list('rooms', flat=True)
        empty_rooms = stats_rooms.difference(lots_rooms)

        self.complexroomsstats_set.filter(rooms__in=empty_rooms).delete()

        self.save()

    def updateAddress(self):
        info = get_address_info(self.address)
        if info == False:
            return
        self.location = info['location']
        self.coordinates = info['coordinates']

        self.complexsubway_set.all().delete()

        for subway in info['subways']:
            try:
                station = Subway.objects.get(name=subway['name'])
            except:
                station = Subway.objects.create(name=subway['name'])

            self.complexsubway_set.create(subway=station, duration=subway['duration'] / 60)

        self.save()

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        old = None

        try:
            old = Complex.objects.get(pk=self.pk)
        except Exception:
            pass

        super().save(*args, **kwargs)

        if not old or old.address != self.address:
            self.updateAddress()


class ComplexPrivate(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    image = OptimizedImageField(optimized_image_output_size=(400, 240),
                                optimized_image_resize_method='cover',
                                upload_to='complexes/',
                                verbose_name='Изображение')

    address = models.CharField(max_length=100, verbose_name='Адрес')
    coordinates = models.JSONField(null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    subway = models.CharField(max_length=50, null=True, blank=True)

    deadline = models.CharField(max_length=20, verbose_name='Срок сдачи', null=True, blank=True, help_text='Можно не заполнять если сдан', choices=get_deadlines())
    done = models.BooleanField(default=False, verbose_name='Сдан')

    order = models.IntegerField(default=0, verbose_name='Приоритет отображения', help_text='При более высоком приоритете, комплекс выводится первее в списках, чем его соседи. Пример: Комплексы с приоритетом 3 > приоритет 1 > приоритет 0')
    created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Комплекс в закрытой продаже'
        verbose_name_plural = 'Комплексы в закрытой продаже'

    def save(self, *args, **kwargs):
        old = None

        try:
            old = ComplexPrivate.objects.get(pk=self.pk)
        except Exception:
            pass

        super().save(*args, **kwargs)

        if not old or old.address != self.address:
            self.updateAddress()

    def updateAddress(self):
        info = get_address_info(self.address)
        if info == False:
            return
        self.location = info['location']
        self.coordinates = info['coordinates']

        self.complexsubway_set.all().delete()

        for subway in info['subways']:
            try:
                station = Subway.objects.get(name=subway['name'])
            except:
                station = Subway.objects.create(name=subway['name'])

            self.complexsubway_set.create(subway=station, duration=subway['duration'] / 60)

        self.save()


class ComplexSubway(models.Model):
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE, null=True)
    complex_private = models.ForeignKey(ComplexPrivate, on_delete=models.CASCADE, null=True)
    subway = models.ForeignKey(Subway, on_delete=models.CASCADE)
    duration = models.IntegerField()


class ComplexRoomsStats(models.Model):
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE)
    rooms = models.IntegerField()
    min_price = models.IntegerField(default=0)
    max_price = models.IntegerField(default=0)
    min_rate = models.IntegerField(default=0)
    max_rate = models.IntegerField(default=0)
    min_area = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    max_area = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.complex} {self.rooms} {self.min_price}-{self.max_price} р, {self.min_area}-{self.max_area} м2'


class ComplexImage(models.Model):
    image = OptimizedImageField(optimized_image_output_size=(800, 450),
                                optimized_image_resize_method='cover',
                                upload_to='complexes/',
                                verbose_name='Изображение')
    order = models.IntegerField(
        default=0,
        verbose_name='Приоритет',
        help_text=
        'При более высоком приоритете, комплекс выводится первее в списках, чем его соседи. Пример: Комплексы с приоритетом 3 > приоритет 1 > приоритет 0'
    )
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Изображение комплекса'
        verbose_name_plural = 'Изображения комплекса'


class Plan(models.Model):
    key = models.CharField(max_length=20, verbose_name='Идентификатор')
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE, verbose_name='Комплекс')

    area = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Площадь (м2)')
    min_price = models.IntegerField(verbose_name='Минимальная стоимость (р)')
    max_price = models.IntegerField(verbose_name='Максимальня стоимость (р)')
    min_rate = models.IntegerField(verbose_name='Минимальная стоимость (р)', blank=True)
    max_rate = models.IntegerField(verbose_name='Максимальня стоимость (р)', blank=True)
    image = models.FileField(upload_to='plans/', verbose_name='Изображение')
    rooms = models.IntegerField(verbose_name='Кол-во спален', help_text='0 - если студия')

    property_type = ChoiceArrayField(models.CharField(max_length=20, choices=PROPERTY_TYPES), default=list, verbose_name='Тип недвижимости')
    class Meta:
        verbose_name = 'Планировка'
        verbose_name_plural = 'Планировки'

    def __str__(self):
        return f'ID: {self.key}; {self.complex}; {self.rooms} спальни; {self.area} м2'

    def save(self, *args, **kwargs):
        old = None

        try:
            old = Plan.objects.get(pk=self.pk)
        except Exception:
            pass

        if not old or old.min_price != self.min_price or old.max_price != self.max_price or old.area != self.area:
            self.min_rate = self.min_price / self.area
            self.max_rate = self.max_price / self.area

        super().save(*args, **kwargs)
        if old and old.complex != self.complex:
            old.complex.update_stats()
        self.complex.update_stats()

    def delete(self, *args, **kwargs):
        complex = Lot.objects.get(pk=self.pk).complex
        super().delete(*args, **kwargs)
        complex.update_stats()


class Lot(models.Model):
    key = models.CharField(max_length=20, verbose_name='Идентификатор')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name='Планировка')

    price = models.IntegerField(verbose_name='Стоимость')
    rate = models.IntegerField(verbose_name='Цена за метр', blank=True)
    floor = models.IntegerField(verbose_name='Этаж')

    trim = models.CharField(max_length=30, choices=TRIMS, verbose_name='Отделка')

    complex = models.ForeignKey(Complex, on_delete=models.CASCADE, verbose_name='Комплекс')

    class Meta:
        verbose_name = 'Лот'
        verbose_name_plural = 'Лоты'

    def __str__(self):
        return f'{self.key}, {self.floor} этаж, {self.price} ₽. Планировка: {self.plan}'

    def save(self, *args, **kwargs):
        old = None

        try:
            old = Lot.objects.get(pk=self.pk)
        except Exception:
            pass

        if not old or old.price != self.price or old.plan != self.plan:
            self.rate = self.price / self.plan.area

        super().save(*args, **kwargs)
        if old and old.complex != self.complex:
            old.complex.update_stats()
        self.complex.update_stats()

    def delete(self, *args, **kwargs):
        complex = Lot.objects.get(pk=self.pk).complex
        super().delete(*args, **kwargs)
        complex.update_stats()

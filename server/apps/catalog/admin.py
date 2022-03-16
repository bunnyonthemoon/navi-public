from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.urls import resolve
from django.utils.safestring import mark_safe

from . import models


class ComplexImageInline(admin.TabularInline):
    model = models.ComplexImage
    extra = 0
    fields = ('getImage', 'image', 'order')
    readonly_fields = ('getImage',)

    @mark_safe
    def getImage(self, obj):
        return f'<a href="{obj.image.url}" target="_blank"><img src="{obj.image.url}" width="60" width="100"></a>'
    getImage.short_description = u'Изображение'


class LotInline(admin.StackedInline):
    model = models.Lot
    extra = 0
    fields = ('key', 'plan', 'floor', 'price', 'trim')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        resolved = resolve(request.path_info)
        if resolved.kwargs.get('object_id'):
            kwargs["queryset"] = models.Plan.objects.filter(complex__pk=resolved.kwargs['object_id'])
        else:
            kwargs['queryset'] = models.Plan.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PlanInline(admin.StackedInline):
    model = models.Plan
    extra = 0
    fields = ('key', 'rooms', 'area', 'min_price', 'max_price', 'property_type', 'image')


class ComplexForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(),
                              label='Описание', required=False)
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label='Загрузить сразу много картинок', required=False)


@admin.register(models.Complex)
class ComplexAdmin(admin.ModelAdmin):
    list_display = ['getImage', '__str__', 'done', 'order', 'get_lots']
    list_display_links = ['__str__']
    list_editable = ['order']
    ordering = ['-order']
    list_filter = ['developer', 'property_type', 'property_class', 'trim', 'done']
    search_fields = ['name', 'address', 'key']
    form = ComplexForm
    save_as = True

    inlines = [ComplexImageInline, LotInline, PlanInline]

    fieldsets = (
        ('Основное', {
            'fields': ('name', 'address', 'tags', 'developer', 'done', 'deadline',
                       'image', 'getImage', 'images', 'presentation')
        }),
        ('Описание', {
            'fields':
            ('property_class', 'property_type', 'trim', 'territory', 'floors', 'lots_count', 'lots_count_total', 'ceilings', 'description')
        }),
        ('SEO', {
            'fields': ('order', 'key')
        }),
        ('Рекомендации', {
            'fields': ('recommendations', )
        }),
    )
    readonly_fields = ('getImage',)

    @mark_safe
    def getImage(self, obj):
        if obj.image:
            return f'<a href="{obj.image.url}" target="_blank"><img src="{obj.image.url}" width="60" width="100"></a>'
        else:
            return '-'
    getImage.short_description = u'Изображение'


    @mark_safe
    def get_lots(self, obj):
        return f'<a href="/admin/catalog/lot/?complex__id__exact={obj.id}">{obj.lot_set.count()} лотов</a>'
    get_lots.short_description = u'Лоты'

    def save_model(self, request, obj, form, change):
        images = request.FILES.getlist('images')
        for image in images:
            obj.compleximage_set.create(image=image)

        super().save_model(request, obj, form, change)


@admin.register(models.Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_complexes']

    @mark_safe
    def get_complexes(self, obj):
        return f'<a href="/admin/catalog/complex/?developer__id__exact={obj.id}">{obj.complex_set.count()} комплексов</a>'
    get_complexes.short_description = u'Комплексы'


@admin.register(models.Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ['get_image', 'key', 'complex', 'get_plan', 'floor', 'price', 'trim']
    list_display_links = ['key']
    list_filter = ['complex', 'trim']
    fields = ('key', 'complex', 'floor', 'price', 'trim')
    readonly_fields = ('get_image', 'get_plan')

    @admin.display(description='Изображение', ordering='plan')
    @mark_safe
    def get_image(self, obj):
        if obj.plan and obj.plan.image:
            return f'<a href="{obj.plan.image.url}" target="_blank"><img src="{obj.plan.image.url}" width="60" width="100"></a>'
        else:
            return '-'

    @admin.display(description='Планировка', ordering='plan')
    @mark_safe
    def get_plan(self, obj):
        return f'<a href="/admin/catalog/plan/{obj.plan.id}/change/" target="_blank">{obj.plan.__str__()}</a>'


class ComplexInline(admin.TabularInline):
    model = models.Complex.tags.through
    extra = 0
    verbose_name = 'Комлекс'
    verbose_name_plural = 'Комлексы'

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'get_complexes', 'order']
    inlines = [ComplexInline]
    list_editable = ['order']
    ordering = ['type', 'order']

    fieldsets = (
        ('Основное', {
            'fields': ('name', 'order')
        }),
        ('Подборка', {
            'fields': ('type', 'budget_rate', 'description', 'color', 'image', 'key')
        }),
    )

    @admin.display(description='Комплексы', ordering='plan')
    @mark_safe
    def get_complexes(self, obj):
        return f'{obj.complex_set.count()} комплексов'


@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['get_image', 'key', 'complex', 'rooms', 'area', 'min_price', 'property_type']
    list_display_links = ['key',]
    list_filter = ['complex', 'property_type']
    fields = ('key', 'complex', 'rooms', 'area', 'min_price', 'max_price', 'property_type', 'image', 'get_image')
    readonly_fields = ('get_image',)

    @admin.display(description='Изображение', ordering='plan')
    @mark_safe
    def get_image(self, obj):
        if obj.image:
            return f'<a href="{obj.image.url}" target="_blank"><img src="{obj.image.url}" width="60" width="100"></a>'
        else:
            return '-'


@admin.register(models.Subway)
class SubwayAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'get_color']
    list_editable = ['color']

    @admin.display(description='Цвет', ordering='color')
    @mark_safe
    def get_color(self, obj):
        return f'<div style="width: 50px; height: 30px; background-color: {obj.color};"></div>'


@admin.register(models.ComplexPrivate)
class ComplexPrivateAdmin(admin.ModelAdmin):
    list_display = ['getImage', 'name', 'order']
    list_display_links = ['name']
    list_editable = ['order']
    fields = ('name', 'description', 'address', 'done', 'deadline', 'image', 'getImage',
              'order')
    readonly_fields = ('getImage', )

    @mark_safe
    def getImage(self, obj):
        if obj.image:
            return f'<a href="{obj.image.url}" target="_blank"><img src="{obj.image.url}" width="60" width="100"></a>'
        else:
            return '-'

    getImage.short_description = u'Изображение'

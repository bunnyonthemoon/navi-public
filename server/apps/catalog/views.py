from django.db.models import Count, FloatField, Max, Min, Q
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from . import models, serializers


@api_view(['GET'])
def complex(request, complex_key):

    complex = models.Complex.objects.get(key=complex_key)

    complex_serialized = serializers.ComplexDetailSerializer(complex).data

    around = models.Complex.objects.exclude(pk=complex.pk)
    around_serialized = serializers.ComplexMapSerializer(around, many=True).data

    return Response({'complex': complex_serialized, 'around': around_serialized})


@api_view(['GET'])
def lot(request, lot_id):

    plan = models.Plan.objects.get(pk=lot_id)

    lot_serialized = serializers.PlanSerializer(plan).data

    return Response({'lot': lot_serialized})


@api_view(['GET'])
def selection(request, selection_key):

    selection = models.Selection.objects.get(key=selection_key)

    selection_serialized = serializers.SelectionDetailSerializer(selection).data

    return Response({'selection': selection_serialized})


@api_view(['POST'])
def options(request):
    complexes = models.Complex.objects.all()

    def get_value(key, dir):
        query = Max(key) if dir == 'max' else Min(key)
        result = complexes.aggregate(query)
        value = result[f'{key}__{dir}']
        return float(value) if value else value

    response = {
        'price': {
            'min': get_value('min_price', 'min'),
            'max': get_value('max_price', 'max')
        },
        'area': {
            'min': get_value('min_area', 'min'),
            'max': get_value('max_area', 'max')
        },
    }

    return Response(response)


@api_view(['POST'])
def filter(request):

    bedrooms = request.data.get('bedrooms')
    area = request.data.get('area')
    price = request.data.get('price')
    sort_key = request.data.get('sort_key')
    sort_dir = request.data.get('sort_dir')
    property_class = request.data.get('class')
    deadline = request.data.get('deadline')
    search = request.data.get('search')
    selection = request.data.get('selection')

    plans = models.Plan.objects.all()

    if bedrooms:
        if '4+' in bedrooms:
            bedrooms_temp = bedrooms
            bedrooms_temp.remove('4+')
            plans = plans.filter(Q(rooms__in=bedrooms_temp) | Q(rooms__gte=4))
        else:
            plans = plans.filter(rooms__in=bedrooms)

    # complexes = models.Complex.objects.annotate(plan_count=Count('plan')).filter(Q(pk__in=plans.values_list('complex', flat=True)) | Q(plan_count=0))
    complexes = models.Complex.objects.filter(pk__in=plans.values_list('complex', flat=True))

    if selection:
        selection_obj = models.Tag.objects.get(key=selection)
        
        complexes = complexes.filter(pk__in=selection_obj.complex_set.all().values_list('id', flat=True))

    if deadline:
        if 'done' in deadline:
            complexes = complexes.filter(Q(deadline__in=deadline) | Q(done=True))
        else:
            complexes = complexes.filter(deadline__in=deadline)
    if property_class:
        complexes = complexes.filter(property_class__in=property_class)

    if area:
        complexes = complexes.filter(
            Q(max_area__gte=area[0]) & Q(min_area__lte=area[1]))
    if price:
        complexes = complexes.filter(
            Q(max_price__gte=price[0]) & Q(min_price__lte=price[1]))

    if search:
        subways = models.ComplexSubway.objects.filter(name__icontains=search)
        complexes = complexes.filter(
            Q(name__icontains=search) | Q(address__icontains=search)
            | Q(developer__name__icontains=search) | Q(trim__icontains=search)
            | Q(property_type__icontains=search)
            | Q(location__icontains=search)
            | Q(id__in=subways.values_list('complex', flat=True)))

    if sort_key == 'price':
        dir = '' if sort_dir == 1 else '-'
        complexes = complexes.order_by(dir + 'min_price')
    if sort_key == 'rate':
        dir = '' if sort_dir == 1 else '-'
        complexes = complexes.order_by(dir + 'min_rate')
    if sort_key == 'created':
        dir = '' if sort_dir == 1 else '-'
        complexes = complexes.order_by(dir + 'created')

    result = serializers.ComplexCatalogSerializer(complexes, many=True).data
    return Response({'complexes': result, 'found': complexes.count()})


@api_view(['POST'])
def favorites(request):
    ids = request.data.get('ids')

    complexes = models.Complex.objects.filter(pk__in=ids)

    complexes_serialized = serializers.ComplexSerializer(complexes, many=True).data

    return Response({'complexes': complexes_serialized})

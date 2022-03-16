from django.db.models import FloatField, Max, Min, Q

from . import models


def get_filter_values():
    complexes = models.Complex.objects.filter()

    def get_value(key, dir):
        query = Max(key) if dir == 'max' else Min(key)
        result = complexes.aggregate(query)
        value = result[f'{key}__{dir}']
        return float(value) if value is not None else value

    print(set(complexes.values_list('property_class', flat=True)))
    result = {
        'price': {
            'min': get_value('min_price', 'min'),
            'max': get_value('max_price', 'max')
        },
        'area': {
            'min': get_value('min_area', 'min'),
            'max': get_value('max_area', 'max')
        },
        'property_classes': list(set(complexes.values_list('property_class', flat=True))),
        'deadlines': list(set(complexes.values_list('deadline', flat=True))),
        'total': complexes.count(),
    }
    print(result)

    return result

import googlemaps
from django.core.mail import send_mail
from rest_framework.response import Response

import env


def json_response(view):
    def wrapper(request, *args, **kwargs):
        return Response(view(request, *args, **kwargs))

    return wrapper


def send_email(email, title, message):
    try:
        send_mail(subject=title, message=message, recipient_list=[email], from_email=None)
        return True
    except Exception as error:
        print(error)
        return False


def get_address_info(address):
    try:
        gmaps = googlemaps.Client(key=env.GOOGLEMAPS_KEY)
        result = gmaps.geocode(address, language='ru')
        result = result[0]
        coordinates = result['geometry']['location']
        location = None
        
        for component in result['address_components']:
            if 'administrative_area_level_3' in component['types']:
                location = component['short_name']

        places = gmaps.places_nearby(location=coordinates,
                                     radius=1000,
                                     type='subway_station',
                                     language='ru')
        print(places)

        subways = list()
        for place in places['results']:
            duration = gmaps.distance_matrix(
                    origins=[coordinates],
                    destinations=[place['geometry']['location']],
                    mode='walking',
                    language='ru')['rows'][0]['elements'][0]
            subway = {
                'name': place['name'],
                'duration': duration['duration']['value'],
            }
            subways.append(subway)


        return { 'location': location, 'coordinates': coordinates, 'subways': subways }

    except Exception as error:
        print(error)
        return False

import json

from django.core.management.base import BaseCommand

from ...services import list_pets
from ...serializers import PetSerializer


def _str_to_optional_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ('true', '1'):
        return True
    if value.lower() in ('false', '0'):
        return False
    return None


def get_only_url_photos(photos: list) -> list:
    return list(map(lambda photo: photo['url'], photos))


class Command(BaseCommand):
    help = 'Lists pets'

    def add_arguments(self, parser):
        parser.add_argument('--has_photos', type=_str_to_optional_bool, default=None)

    def handle(self, *args, **options):
        pets = list_pets(has_photos=options.get('has_photos'))
        serializer = PetSerializer(pets, many=True)
        for pet in serializer.data:
            pet['photos'] = get_only_url_photos(pet['photos'])
        output_dict = {
            'pets': serializer.data
        }
        pretty = json.dumps(output_dict, indent=4)
        self.stdout.write(pretty)

import os
from collections.abc import Iterable
from uuid import UUID

import boto3
from django.db.models import Count, QuerySet
from django.conf import settings

from .models import Pet


def is_valid_uuid(test_uuid: str) -> bool:
    try:
        UUID(test_uuid)
    except ValueError:
        return False
    return True


def list_pets(has_photos: bool = None) -> QuerySet[Pet]:
    pets_with_photos_number = Pet.objects.annotate(photos_number=Count('photos'))
    if has_photos is None:
        return pets_with_photos_number
    if has_photos:
        return pets_with_photos_number.exclude(photos_number=0)
    return pets_with_photos_number.filter(photos_number=0)


def delete_existing_pets(ids: Iterable[UUID]) -> tuple[int, set[UUID]]:
    uniq_ids = set(ids)
    pets_to_delete = Pet.objects.filter(id__in=uniq_ids)
    pet_ids_to_delete = set(map(lambda pet_value: pet_value[0],
                                pets_to_delete.values_list('id')))

    deleted_objects = pets_to_delete.delete()[1]
    not_exists_ids = uniq_ids - pet_ids_to_delete

    return deleted_objects.get('api.Pet') or 0, not_exists_ids


def delete_image_from_s3_storage(filename: str) -> None:
    client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          endpoint_url=settings.AWS_S3_ENDPOINT_URL)
    client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                         Key=f'{settings.MEDIA_FILES_FOLDER_NAME}/{filename}')


def delete_image_from_local_storage(filename: str) -> None:
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, filename))
    except FileNotFoundError:
        pass

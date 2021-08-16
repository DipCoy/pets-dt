from uuid import UUID

from django.db.models import signals
from django.conf import settings
from django.dispatch.dispatcher import receiver
from django.core.exceptions import ValidationError

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services import \
    is_valid_uuid, \
    list_pets, \
    delete_existing_pets, \
    delete_image_from_local_storage, \
    delete_image_from_s3_storage
from .serializers import PetSerializer, PetPhotoSerializer
from .models import Pet, PetPhoto
from .paginators import CustomLimitOffsetPagination


class PetListCreateDestroyView(generics.CreateAPIView):
    serializer_class = PetSerializer
    queryset = Pet.objects.all()
    pagination_class = CustomLimitOffsetPagination

    def get(self, request, *args, **kwargs):
        has_photos = request.GET.get('has_photos')
        if has_photos == u'true':
            has_photos = True
        elif has_photos == u'false':
            has_photos = False
        else:
            has_photos = None

        filtered_pets = list_pets(has_photos=has_photos)
        page = self.paginate_queryset(filtered_pets)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)

    def delete(self, request, *args, **kwargs):
        request_to_delete_pet_ids = request.data.get('ids')
        if type(request_to_delete_pet_ids) is not list:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        to_delete_pet_uuids = []
        not_uuids = []
        for str_uuid in request_to_delete_pet_ids:
            if is_valid_uuid(str_uuid):
                to_delete_pet_uuids.append(UUID(str_uuid, version=4))
            else:
                not_uuids.append(str_uuid)

        deleted_number, not_found_ids = delete_existing_pets(to_delete_pet_uuids)

        not_found_id_errors = [{
            'id': id,
            'error': 'Pet with the matching ID was not found.'
        } for id in not_found_ids]
        not_valid_id_errors = [{
            'id': id,
            'error': 'The matching ID is not a valid UUID.'
        } for id in not_uuids]

        return Response({
            'deleted': deleted_number,
            'errors': not_found_id_errors + not_valid_id_errors
        })


@api_view(http_method_names=['POST'])
def post_pet_photo(request, id=None):
    try:
        pet_object = Pet.objects.get(id__exact=id)
    except ValidationError:
        return Response({'error': f'{id=} is not a valid UUID'})
    except Pet.DoesNotExist:
        return Response({'error': f'Pet with {id=} was not found'})

    photo = request.FILES.get('file')
    if photo is None:
        return Response({'error': 'Has no file key in form-data'})

    pet_photo = PetPhoto.objects.create(pet=pet_object, image=photo)
    serializer = PetPhotoSerializer(pet_photo)
    return Response(serializer.data)


@receiver(signals.post_delete, sender=PetPhoto)
def delete_image_from_storage_receiver(sender, instance, *args, **kwargs):
    if instance.image:
        if settings.USE_S3_STORAGE:
            delete_image_from_s3_storage(instance.image.name)
        else:
            delete_image_from_local_storage(instance.image.name)

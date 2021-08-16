from rest_framework import serializers

from .models import Pet, PetPhoto


class PetPhotoSerializer(serializers.ModelSerializer):
    url = serializers.ImageField(source='image', use_url=True)

    class Meta:
        model = PetPhoto
        fields = ('id', 'url')


class PetSerializer(serializers.ModelSerializer):
    photos = PetPhotoSerializer(
        many=True,
        read_only=True
    )
    created_at = serializers.DateTimeField('%Y-%m-%d:%H:%M:%S', required=False, read_only=True)

    class Meta:
        model = Pet
        fields = ('id', 'name', 'age', 'type', 'photos', 'created_at')

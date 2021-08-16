import uuid

from django.db import models


class Pet(models.Model):
    PET_TYPE = (
        ('dog', 'dog'),
        ('cat', 'cat')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40)
    age = models.PositiveIntegerField(null=True)
    type = models.CharField(max_length=5, choices=PET_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pet: type={self.type}, name={self.name}, age={self.age}'


class PetPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField()
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='photos')

    def __str__(self):
        return f'PetPhoto: pet={self.pet}, id={self.id}'

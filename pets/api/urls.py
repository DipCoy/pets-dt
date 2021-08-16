from django.urls import path
from . import views


urlpatterns = [
    path('pets', views.PetListCreateDestroyView.as_view()),
    path('pets/<str:id>/photo', views.post_pet_photo),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CaracteristicasAPIView,
    CaracteristicasDoCuidadorView,
    CustomAuthToken,
    UserRegisterView,
    CuidadorViewSet,
    TutorViewSet
)

router = DefaultRouter()
router.register(r'cuidadores', CuidadorViewSet, basename='cuidador')
router.register(r'tutores', TutorViewSet)

urlpatterns = router.urls


urlpatterns = [
    path('', include(router.urls)),
    path('caracteristicas/', CaracteristicasAPIView.as_view(), name='caracteristicas-list'),
    path('cuidadores/<int:cuidador_id>/caracteristicas/', CaracteristicasDoCuidadorView.as_view(), name='caracteristicas-cuidador'),
    path('api/login/', CustomAuthToken.as_view(), name='api_login'),
    path('register/', UserRegisterView.as_view(), name='register'),
]
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from django.shortcuts import redirect
from .views import (
    CaracteristicasAPIView,
    CaracteristicasDoCuidadorView,
    CustomAuthToken,
    UserRegisterView,
    CuidadorViewSet,
    TutorViewSet,
    PedidoViewSet,
    HospedagemViewSet,
    PetViewSet,
    AvaliacaoCuidadorViewSet
)

router = DefaultRouter()
router.register(r'cuidadores', CuidadorViewSet, basename='cuidador')
router.register(r'tutores', TutorViewSet)
router.register(r'pedidos', PedidoViewSet, basename='pedido')
router.register(r'hospedagens', HospedagemViewSet, basename='hospedagem')
router.register(r'pets', PetViewSet, basename='pet')
router.register(r'avaliacoes', AvaliacaoCuidadorViewSet, basename='avaliacoes')

urlpatterns = router.urls

urlpatterns += [
    path('caracteristicas/', CaracteristicasAPIView.as_view(), name='caracteristicas-list'),
    path('cuidadores/<int:cuidador_id>/caracteristicas/', CaracteristicasDoCuidadorView.as_view(), name='caracteristicas-cuidador'),
    path('api/login/', CustomAuthToken.as_view(), name='api_login'),
    path('register/', UserRegisterView.as_view(), name='register'),

    # Solução para erro 404 ao acessar /accounts/login/
    path('accounts/', include('django.contrib.auth.urls')),
]

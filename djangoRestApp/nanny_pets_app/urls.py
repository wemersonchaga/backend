from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.shortcuts import redirect
from .views import (
    LoginView,
    CaracteristicasAPIView,
    CaracteristicasDoCuidadorView,
    CustomAuthToken,
    UserRegisterView,
    CuidadorViewSet,
    TutorViewSet,
    PedidoViewSet,
    PorteListView,
    HospedagemViewSet,
    UploadImagensAmbienteView,
    usuario_logado,
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

urlpatterns = [
    *router.urls,
    
    path('caracteristicas/', CaracteristicasAPIView.as_view(), name='listar_caracteristicas_gerais'),
    path('cuidadores/<int:cuidador_id>/caracteristicas/', CaracteristicasDoCuidadorView.as_view(), name='caracteristicas_do_cuidador'),
    path('portes/', PorteListView.as_view(), name='listar-portes'),
    path('cuidadores/imagens/upload/', UploadImagensAmbienteView.as_view(), name='upload_imagens_ambiente'),
    path('api/login/', CustomAuthToken.as_view(), name='api_login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='api-login'),
    path('usuarios/me/', usuario_logado, name='usuario-logado'),
    path('accounts/', include('django.contrib.auth.urls')),
]

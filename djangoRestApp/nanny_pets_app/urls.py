from django.urls import path


from .views import CaracteristicasAPIView,CaracteristicasDoCuidadorView, CuidadorAPIView, TutorAPIView,CuidadorFiltradoView,CustomAuthToken,UserRegisterView




urlpatterns = [
    path('cuidadores/', CuidadorAPIView.as_view(), name='cuidadores'),
    path('caracteristicas/', CaracteristicasAPIView.as_view(), name='caracteristicas'),
    path('tutores/',TutorAPIView.as_view(), name='tutores'),
    path('cuidadores/<int:cuidador_id>/caracteristicas/',CaracteristicasDoCuidadorView.as_view(), name='caracteristicascuidador'),
    path('cuidadores-filtrados/', CuidadorFiltradoView.as_view(), name='cuidadores-filtrados'),
    path('api/login/', CustomAuthToken.as_view(), name='api_login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    
]
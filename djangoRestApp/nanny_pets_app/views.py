from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend

from .models import Cuidador, Tutor, Pedido, Hospedagem, Pet, AvaliacaoCuidador
from .serializers import TutorCreateSerializer, TutorReadSerializer, CuidadorCreateSerializer, CuidadorReadSerializer, CaracteristicasCuidadorSerializer, UserSerializer, PedidoSerializer, HospedagemSerializer, PetSerializer, AvaliacaoCuidadorSerializer
from .filters import CuidadorFilter
from rest_framework.decorators import action
from .permissions import IsTutorUser
from rest_framework.exceptions import ValidationError, PermissionDenied

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CuidadorViewSet(viewsets.ModelViewSet):
    queryset = Cuidador.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CuidadorCreateSerializer
        return CuidadorReadSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CuidadorFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Evita erro no Swagger
        if getattr(self, 'swagger_fake_view', False):
            return Cuidador.objects.none()
        return Cuidador.objects.all()

    @action(detail=False, methods=['get'], url_path='filtrar')
    def filtrar_por_caracteristicas(self, request):
        caracteristicas = request.query_params.getlist('caracteristicas')
        queryset = self.get_queryset()
        if caracteristicas:
            queryset = queryset.filter(caracteristicas__id__in=caracteristicas).distinct()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'cuidador'):
            raise ValidationError("Este usuário já possui um perfil de cuidador.")
        serializer.save(user=user)

class CaracteristicasAPIView(APIView):
    def get(self, request):
        from .models import CaracteristicasCuidador  # adicione este import
        caracteristicas = CaracteristicasCuidador.objects.all()
        serializer = CaracteristicasCuidadorSerializer(caracteristicas, many=True)
        return Response(serializer.data)

class CaracteristicasDoCuidadorView(APIView):
    def get(self, request, cuidador_id):
        cuidador = get_object_or_404(Cuidador, id=cuidador_id)
        caracteristicas = cuidador.caracteristicas.all()  # instância, não classe
        serializer = CaracteristicasCuidadorSerializer(caracteristicas, many=True)
        return Response(serializer.data)

class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TutorCreateSerializer
        return TutorReadSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Evita erro no Swagger
        if getattr(self, 'swagger_fake_view', False):
            return Tutor.objects.none()

        user = self.request.user
        return Tutor.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'tutor'):
            raise ValidationError("Este usuário já possui um perfil de tutor.")
        serializer.save(user=user)

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']  # <-- Aqui habilita filtro por status

    def get_queryset(self):
        user = self.request.user

        if getattr(self, 'swagger_fake_view', False):
            return Pedido.objects.none()

        if hasattr(user, 'tutor'):
            return Pedido.objects.filter(tutor=user.tutor)
        elif hasattr(user, 'cuidador'):
            return Pedido.objects.filter(cuidador=user.cuidador)

        return Pedido.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if hasattr(user, 'tutor'):
            tutor = user.tutor
            serializer.save(tutor=tutor)
        else:
            raise PermissionDenied("Apenas tutores podem criar pedidos.")

class HospedagemViewSet(viewsets.ModelViewSet):
    queryset = Hospedagem.objects.all()
    serializer_class = HospedagemSerializer
    permission_classes = [permissions.IsAuthenticated, IsTutorUser]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Hospedagem.objects.none()
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("Usuário não autenticado.")
        if not hasattr(user, 'tutor'):
            raise PermissionDenied("Apenas tutores podem acessar suas hospedagens.")
        return Hospedagem.objects.filter(tutor=user.tutor)

    def perform_create(self, serializer):
        try:
            tutor = self.request.user.tutor
            cuidador = serializer.validated_data['cuidador']
            data_inicio = serializer.validated_data['data_inicio']
            data_fim = serializer.validated_data['data_fim']

            # Validação: data de início deve ser antes da data de fim
            if data_inicio >= data_fim:
                raise ValidationError("A data de início deve ser anterior à data de fim.")

            # Verifica se há conflitos com outras hospedagens
            conflitos = Hospedagem.objects.filter(
                cuidador=cuidador,
                data_inicio__lt=data_fim,
                data_fim__gt=data_inicio
            )
            if conflitos.exists():
                raise ValidationError("O cuidador já possui hospedagens nesse período.")

            serializer.save(tutor=tutor)

        except AttributeError:
            raise PermissionDenied("Usuário não é um tutor válido.")

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated, IsTutorUser]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Pet.objects.none()
        user = self.request.user
        if not user.is_authenticated or not hasattr(user, 'tutor'):
            return Pet.objects.none()
        return Pet.objects.filter(tutor=user.tutor)
    
    def perform_create(self, serializer):
        tutor = self.request.user.tutor
        serializer.save(tutor=tutor)
    
    def perform_update(self, serializer):
        pet = self.get_object()
        if pet.tutor != self.request.user.tutor:
            raise PermissionDenied("Você não tem permissão para atualizar este pet.")
        serializer.save()
        def perform_destroy(self, instance):
            if instance.tutor != self.request.user.tutor:
                raise PermissionDenied("Você não tem permissão para excluir este pet.")
            instance.delete()


class AvaliacaoCuidadorViewSet(viewsets.ModelViewSet):
    queryset = AvaliacaoCuidador.objects.all()
    serializer_class = AvaliacaoCuidadorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'tutor'):
            return AvaliacaoCuidador.objects.filter(tutor=user.tutor)
        return AvaliacaoCuidador.objects.none()

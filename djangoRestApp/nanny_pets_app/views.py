# Django
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Terceiros
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Locais
from .filters import CuidadorFilter
from .models import (
    AvaliacaoCuidador,
    CaracteristicasCuidador,
    Cuidador,
    Hospedagem,
    Pedido,
    Pet,
    Tutor
)
from .permissions import IsTutorUser
from .serializers import (
    AvaliacaoCuidadorSerializer, CaracteristicasCuidadorSerializer,
    CuidadorCreateSerializer, CuidadorReadSerializer,
    CuidadorSerializer, HospedagemSerializer, PedidoSerializer,
    PetSerializer, TutorCreateSerializer, TutorReadSerializer,
    TutorSerializer, UserSerializer
)

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usuario_logado(request):
    user = request.user
    try:
        if hasattr(user, 'tutor'):
            return Response(TutorSerializer(user.tutor).data)
        elif hasattr(user, 'cuidador'):
            return Response(CuidadorSerializer(user.cuidador).data)
        else:
            nome = user.get_full_name() or user.username
            return Response({'nome': nome, 'email': user.email})
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CuidadorViewSet(viewsets.ModelViewSet):
    queryset = Cuidador.objects.all()
    serializer_class = CuidadorSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend]
    filterset_class = CuidadorFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CuidadorCreateSerializer
        return CuidadorReadSerializer

    def get_queryset(self):
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

    @action(detail=False, methods=['get'], url_path='me', permission_classes=[IsAuthenticated])
    def me(self, request):
        cuidador = Cuidador.objects.filter(user=request.user).first()
        if cuidador:
            serializer = CuidadorReadSerializer(cuidador)
            return Response(serializer.data)
        return Response({}, status=200)

    def perform_create(self, serializer):
        user = self.request.user
        # Impede múltiplos perfis de cuidador para o mesmo usuário
        if hasattr(user, 'cuidador'):
            raise ValidationError("Este usuário já possui um perfil de cuidador.")
        serializer.save(user=user)  # <-- Aqui vincula o tutor ao User corretamente


class CaracteristicasAPIView(APIView):
    def get(self, request):
        caracteristicas = CaracteristicasCuidador.objects.all()
        serializer = CaracteristicasCuidadorSerializer(caracteristicas, many=True)
        return Response(serializer.data)

class CaracteristicasDoCuidadorView(APIView):
    def get(self, request, cuidador_id):
        cuidador = get_object_or_404(Cuidador, id=cuidador_id)
        caracteristicas = cuidador.caracteristicas.all()
        serializer = CaracteristicasCuidadorSerializer(caracteristicas, many=True)
        return Response(serializer.data)

class UploadImagensAmbienteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ImagemAmbienteUploadSerializer(data=request.data)
        if serializer.is_valid():
            imagens = serializer.save()
            return Response({"mensagem": f"{len(imagens)} imagens enviadas com sucesso."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TutorViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    queryset = Tutor.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TutorCreateSerializer
        return TutorReadSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Tutor.objects.none()
        return Tutor.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='me', permission_classes=[IsAuthenticated])
    def me(self, request):
        tutor = Tutor.objects.filter(user=request.user).first()
        if tutor:
            serializer = TutorReadSerializer(tutor)
            return Response(serializer.data)
        return Response({}, status=200)

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'tutor'):
            raise ValidationError("Este usuário já possui um perfil de tutor.")
        serializer.save(user=user)  # <-- Aqui vincula o tutor ao User corretamente

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

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
        if not hasattr(user, 'tutor'):
            raise PermissionDenied("Apenas tutores podem acessar suas hospedagens.")
        return Hospedagem.objects.filter(tutor=user.tutor)

    def perform_create(self, serializer):
        tutor = self.request.user.tutor
        cuidador = serializer.validated_data['cuidador']
        data_inicio = serializer.validated_data['data_inicio']
        data_fim = serializer.validated_data['data_fim']

        if data_inicio >= data_fim:
            raise ValidationError("A data de início deve ser anterior à data de fim.")

        conflitos = Hospedagem.objects.filter(
            cuidador=cuidador,
            data_inicio__lt=data_fim,
            data_fim__gt=data_inicio
        )
        if conflitos.exists():
            raise ValidationError("O cuidador já possui hospedagens nesse período.")

        serializer.save(tutor=tutor)

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated, IsTutorUser]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Pet.objects.none()
        user = self.request.user
        if not hasattr(user, 'tutor'):
            return Pet.objects.none()
        return Pet.objects.filter(tutor=user.tutor)

    def perform_create(self, serializer):
        serializer.save()  # Remova o tutor=tutor daqui

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

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        login_value = request.data.get('username', '').lower()
        password = request.data.get('password')

        # Tenta buscar username case-insensitive
        try:
            user_obj = User.objects.get(username__iexact=login_value)
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        # Se falhar, tenta email case-insensitive
        if not user:
            try:
                user_obj = User.objects.get(email__iexact=login_value)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })

        return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

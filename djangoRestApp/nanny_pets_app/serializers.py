from django.db.models import Avg
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cuidador, CaracteristicasCuidador, Tutor, Pedido, Hospedagem, Pet, AvaliacaoCuidador
from datetime import date
from django.conf import settings
from urllib.parse import urljoin
from rest_framework.validators import UniqueValidator
import django_filters

# ------------------- USER -------------------
class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Este e-mail já está em uso.")]
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# ------------------- CUIDADOR -------------------
class CuidadorFilter(django_filters.FilterSet):
    caracteristicas = django_filters.ModelMultipleChoiceFilter(
        field_name='caracteristicas',
        queryset=CaracteristicasCuidador.objects.all(),
        conjoined=False
    )

    class Meta:
        model = Cuidador
        fields = ['caracteristicas']


class CaracteristicasCuidadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaracteristicasCuidador
        fields = '__all__'


class CuidadorCreateSerializer(serializers.ModelSerializer):
    caracteristicas_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CaracteristicasCuidador.objects.all(),
        write_only=True,
        source='caracteristicas'
    )
    foto_perfil = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Cuidador
        fields = [
            'id', 'nome', 'sobrenome', 'data_nascimento', 'cpf', 'email',
            'telefone', 'cep', 'estado', 'cidade', 'rua', 'numero',
            'instagram', 'foto_perfil', 'caracteristicas_ids'
        ]
        extra_kwargs = {
            'cpf': {'write_only': True},
            'email': {'write_only': True},
            'telefone': {'write_only': True},
            'cep': {'write_only': True},
            'estado': {'write_only': True},
            'cidade': {'write_only': True},
            'rua': {'write_only': True},
            'numero': {'write_only': True},
            'instagram': {'required': False, 'allow_blank': True},
        }

    def create(self, validated_data):
        caracteristicas = validated_data.pop('caracteristicas', [])
        user = self.context['request'].user
        cuidador = Cuidador.objects.create(user=user, **validated_data)
        cuidador.caracteristicas.set(caracteristicas)
        return cuidador
        
    def perform_create(self, serializer):
    user = self.request.user
    if hasattr(user, 'tutor'):
        raise ValidationError("Este usuário já possui um perfil de tutor.")
    try:
        tutor = serializer.save(user=user)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erro ao criar tutor: {e}", exc_info=True)
        raise ValidationError(f"Erro ao criar tutor: {str(e)}")



class CuidadorReadSerializer(serializers.ModelSerializer):
    caracteristicas = CaracteristicasCuidadorSerializer(many=True, read_only=True)
    media_avaliacoes = serializers.SerializerMethodField()
    total_avaliacoes = serializers.SerializerMethodField()
    avaliacoes_recentes = serializers.SerializerMethodField()

    class Meta:
        model = Cuidador
        fields = [
            'id', 'nome', 'sobrenome', 'data_nascimento',
            'instagram', 'foto_perfil', 'caracteristicas',
            'media_avaliacoes', 'total_avaliacoes', 'avaliacoes_recentes'
        ]

    def get_media_avaliacoes(self, obj):
        media = obj.avaliacoes.aggregate(media=Avg('nota'))['media']
        return round(media, 1) if media else None

    def get_total_avaliacoes(self, obj):
        return obj.avaliacoes.count()

    def get_avaliacoes_recentes(self, obj):
        avaliacoes = obj.avaliacoes.select_related('tutor').order_by('-data_hora')[:3]
        return [
            {
                'nota': a.nota,
                'comentario': a.comentario,
                'data': a.data_hora.strftime('%d/%m/%Y'),
                'tutor': {
                    'nome': f"{a.tutor.nome} {a.tutor.sobrenome}",
                    'foto_perfil': (
                        a.tutor.foto_perfil.url if a.tutor.foto_perfil
                        else urljoin(settings.MEDIA_URL, 'default/avatar_tutor.png')
                    )
                }
            } for a in avaliacoes
        ]


class CuidadorSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='user.first_name')
    email = serializers.EmailField(source='user.email')
    foto_perfil = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Cuidador
        fields = ['id', 'nome', 'email', 'descricao', 'telefone', 'foto_perfil']
        fields = '__all__'

# ------------------- TUTOR -------------------
class TutorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ('id', 'nome', 'sobrenome', 'data_nascimento', 'cpf', 'email', 'foto_perfil')

    def create(self, validated_data):
        user = self.context['request'].user
        return Tutor.objects.create(user=user, **validated_data)


class TutorReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ('id', 'nome', 'sobrenome', 'data_nascimento', 'foto_perfil')


class TutorSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['id', 'nome', 'sobrenome', 'email', 'foto_perfil']
        read_only_fields = fields


class TutorSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='user.first_name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Tutor
        fields = ['id', 'nome', 'email', 'cpf', 'data_nascimento', 'foto_perfil']

# ------------------- PEDIDO -------------------
class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
        read_only_fields = ['id', 'tutor', 'status', 'data_criacao']

    def validate(self, data):
        if data['data_inicio'] > data['data_fim']:
            raise serializers.ValidationError("A data de início não pode ser depois da data de fim.")

        cuidador = data['cuidador']
        pedidos_existentes = Pedido.objects.filter(
            cuidador=cuidador,
            data_fim__gte=data['data_inicio'],
            data_inicio__lte=data['data_fim'],
            status__in=['pendente', 'aprovado']
        )
        if pedidos_existentes.exists():
            raise serializers.ValidationError("O cuidador não está disponível nesse período.")
        return data

    def create(self, validated_data):
        tutor = self.context['request'].user.tutor
        return Pedido.objects.create(tutor=tutor, **validated_data)

# ------------------- HOSPEDAGEM -------------------
class HospedagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospedagem
        fields = '__all__'
        read_only_fields = ['id', 'tutor', 'status', 'data_criacao']

    def validate(self, data):
        if data['data_inicio'] >= data['data_fim']:
            raise serializers.ValidationError("A data de início deve ser anterior à data de fim.")

        hospedagens_existentes = Hospedagem.objects.filter(
            cuidador=data['cuidador'],
            data_fim__gte=data['data_inicio'],
            data_inicio__lte=data['data_fim'],
            status__in=['pendente', 'aprovada']
        )
        if hospedagens_existentes.exists():
            raise serializers.ValidationError("O cuidador não está disponível nesse período.")
        return data

    def create(self, validated_data):
        validated_data['tutor'] = self.context['request'].user.tutor
        return super().create(validated_data)

# ------------------- PET -------------------
class PetSerializer(serializers.ModelSerializer):
    tutor = TutorSimplesSerializer(read_only=True)

    class Meta:
        model = Pet
        fields = ['id', 'nome', 'especie', 'porte', 'tutor']
        read_only_fields = ['id', 'tutor']

    def create(self, validated_data):
        tutor = self.context['request'].user.tutor
        return Pet.objects.create(tutor=tutor, **validated_data)

# ------------------- AVALIAÇÃO -------------------
class AvaliacaoCuidadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvaliacaoCuidador
        fields = ['id', 'hospedagem', 'cuidador', 'tutor', 'nota', 'comentario', 'data_hora']
        read_only_fields = ['id', 'data_hora', 'tutor', 'cuidador']

    def validate(self, attrs):
        tutor = self.context['request'].user.tutor
        hospedagem = attrs.get('hospedagem')

        if hospedagem.tutor != tutor:
            raise serializers.ValidationError("Você não tem permissão para avaliar esta hospedagem.")

        if hospedagem.status != 'finalizada':
            raise serializers.ValidationError("A hospedagem precisa estar finalizada para ser avaliada.")

        if AvaliacaoCuidador.objects.filter(hospedagem=hospedagem).exists():
            raise serializers.ValidationError("Esta hospedagem já foi avaliada.")

        return attrs

    def create(self, validated_data):
        request = self.context['request']
        tutor = request.user.tutor
        hospedagem = validated_data['hospedagem']
        validated_data['tutor'] = tutor
        validated_data['cuidador'] = hospedagem.cuidador
        return super().create(validated_data)

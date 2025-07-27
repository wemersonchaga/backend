import django_filters
from django.db.models import Avg
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cuidador, CaracteristicasCuidador, Tutor, Pedido, Hospedagem, Pet, AvaliacaoCuidador
from datetime import date
from django.conf import settings
from urllib.parse import urljoin
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)  # ⬅️ Adicionado

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
class CuidadorFilter(django_filters.FilterSet):
    caracteristicas = django_filters.ModelMultipleChoiceFilter(
        field_name='caracteristicas',
        queryset=CaracteristicasCuidador.objects.all(),
        conjoined=False  # ou True se quiser que sejam todas (E), não qualquer (OU)
    )

    class Meta:
        model = Cuidador
        fields = ['caracteristicas']

class CaracteristicasCuidadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaracteristicasCuidador
        fields = '__all__'  # ou uma lista que contém 'estudante_de_veterinaria'

class CuidadorCreateSerializer(serializers.ModelSerializer):
    caracteristicas_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CaracteristicasCuidador.objects.all(), write_only=True, source='caracteristicas'
    )

    class Meta:
        model = Cuidador
        fields = [
            'id', 'nome', 'sobrenome', 'data_nascimento', 'cpf', 'email',
            'telefone', 'cep', 'numero', 'instagram', 'caracteristicas_ids'
        ]
        extra_kwargs = {
            'cpf': {'write_only': True},
            'email': {'write_only': True},
            'telefone': {'write_only': True},
            'cep': {'write_only': True},
            'numero': {'write_only': True},
        }
class CuidadorReadSerializer(serializers.ModelSerializer):
    caracteristicas = CaracteristicasCuidadorSerializer(many=True, read_only=True)
    media_avaliacoes = serializers.SerializerMethodField()
    total_avaliacoes = serializers.SerializerMethodField()
    avaliacoes_recentes = serializers.SerializerMethodField()

    class Meta:
        model = Cuidador
        fields = [
            'id', 'nome', 'sobrenome', 'data_nascimento',
            'instagram', 'caracteristicas',
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

    
class TutorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = (
            'id', 'nome', 'sobrenome', 'data_nascimento', 'cpf', 'email', 'foto_perfil'
        )

class TutorReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = (
            'id', 'nome', 'sobrenome', 'data_nascimento', 'foto_perfil'
        )


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

class HospedagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospedagem
        fields = '__all__'
        read_only_fields = ['id', 'tutor', 'status', 'data_criacao']

    def validate(self, data):
        data_inicio = data['data_inicio']
        data_fim = data['data_fim']
        
        if data_inicio >= data_fim:
            raise serializers.ValidationError("A data de início deve ser anterior à data de fim.")

        cuidador = data['cuidador']
        hospedagens_existentes = Hospedagem.objects.filter(
            cuidador=cuidador,
            data_fim__gte=data_inicio,
            data_inicio__lte=data_fim,
            status__in=['pendente', 'aprovada']
        )
        if hospedagens_existentes.exists():
            raise serializers.ValidationError("O cuidador não está disponível nesse período.")
        
        return data

    def create(self, validated_data):
        request = self.context['request']
        tutor = request.user.tutor
        validated_data['tutor'] = tutor
        return super().create(validated_data)


class TutorSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['id', 'nome', 'sobrenome', 'email', 'foto_perfil']
        read_only_fields = fields

class PetSerializer(serializers.ModelSerializer):
    tutor = TutorSimplesSerializer(read_only=True)

    class Meta:
        model = Pet
        fields = ['id', 'nome', 'especie', 'porte', 'tutor']
        read_only_fields = ['id', 'tutor']

    def create(self, validated_data):
        tutor = self.context['request'].user.tutor
        return Pet.objects.create(tutor=tutor, **validated_data)

class AvaliacaoCuidadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvaliacaoCuidador
        fields = ['id', 'hospedagem', 'cuidador', 'tutor', 'nota', 'comentario', 'data_hora']
        read_only_fields = ['id', 'data_hora', 'tutor', 'cuidador']

    def validate(self, attrs):
        request = self.context['request']
        tutor = request.user.tutor
        hospedagem = attrs.get('hospedagem')

        # Verifica se o tutor da hospedagem é o usuário autenticado
        if hospedagem.tutor != tutor:
            raise serializers.ValidationError("Você não tem permissão para avaliar esta hospedagem.")

        # Permite avaliação apenas se a hospedagem estiver finalizada
        if hospedagem.status != 'finalizada':
            raise serializers.ValidationError("A hospedagem precisa estar finalizada para ser avaliada.")

        # Bloqueia avaliações duplicadas
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

class TutorSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='user.first_name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Tutor
        fields = ['id', 'nome', 'email', 'cpf', 'data_nascimento', 'foto_perfil']

class CuidadorSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='user.first_name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Cuidador
        fields = ['id', 'nome', 'email', 'descricao', 'telefone', 'foto_perfil']

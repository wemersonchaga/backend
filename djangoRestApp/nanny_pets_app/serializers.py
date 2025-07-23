import django_filters
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Cuidador, CaracteristicasCuidador, Tutor

class CuidadorFilter(django_filters.FilterSet):
    caracteristicas = django_filters.ModelMultipleChoiceFilter(
        field_name='caracteristicas',
        queryset=CaracteristicasCuidador.objects.all(),
        conjoined=False  # ou True se quiser que sejam todas (E), não qualquer (OU)
    )

    class Meta:
        model = Cuidador
        fields = ['caracteristicas']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class CaracteristicasCuidadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaracteristicasCuidador
        fields = '__all__'  # ou uma lista que contém 'estudante_de_veterinaria'

class CuidadorSerializer(serializers.ModelSerializer):
    caracteristicas = CaracteristicasCuidadorSerializer(many=True, read_only=True)
    caracteristicas_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CaracteristicasCuidador.objects.all(), write_only=True, source='caracteristicas'
    )

    class Meta:
        model = Cuidador
        fields = [
            'id',
            'nome',
            'sobrenome',
            'data_nascimento',
            'cpf',
            'email',
            'telefone',
            'cep',
            'numero',
            'instagram',
            'caracteristicas',      # leitura (detalhado)
            'caracteristicas_ids'   # escrita (apenas IDs)
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = (
            'id',
            'nome',
            'sobrenome',
            'data_nascimento',
            'cpf',
            'email',
            'foto_perfil',
        )

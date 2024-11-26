from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Cuidador, Caracteristicas, Tutor

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Criação do usuário com criptografia da senha
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class CaracteristicasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caracteristicas
        fields = ['id', 'nome']

class CuidadorSerializer(serializers.ModelSerializer):
    # Usamos PrimaryKeyRelatedField para aceitar IDs das características no ManyToManyField
    caracteristicas = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Caracteristicas.objects.all()
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
            'logradouro',
            'cep',
            'uf',
            'localidade',
            'numero',
            'instagram',
            'caracteristicas'
        ]
    def create(self, validated_data):
        caracteristicas_data = validated_data.pop('caracteristicas')
        cuidador = Cuidador.objects.create(**validated_data)
        cuidador.caracteristicas.set(caracteristicas_data)
        return cuidador

    def update(self, instance, validated_data):
        caracteristicas_data = validated_data.pop('caracteristicas')
        instance = super().update(instance, validated_data)
        instance.caracteristicas.set(caracteristicas_data)
        return instance

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = (
            'id',
            'nome',
            'sobrenome',
            'data_nascimento',
            'cpf',
            'email'
        )


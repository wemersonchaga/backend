from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Pessoa(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='%(class)s')
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)
    cpf = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    foto_perfil = models.ImageField(blank=True, null=True)

    class Meta:
        abstract = True


class Tutor(Pessoa):
    plataformaIndicação = models.CharField(max_length=100,blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Tutores'

    def __str__(self):
        return self.nome

class Caracteristicas(models.Model):
    nome = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.nome if self.nome else "Sem Nome"

class Cuidador(Pessoa):
    telefone = models.IntegerField()
    cep = models.CharField(max_length = 8,null = True)
    uf = models.CharField(max_length = 100, null = True)
    localidade = models.CharField(max_length = 100, null = True)
    numero = models.IntegerField(default = 0)
    logradouro = models.CharField(max_length = 100)
    instagram = models.CharField(max_length=100)
    caracteristicas = models.ManyToManyField(Caracteristicas)

    class Meta:
        verbose_name_plural = 'Cuidadores'

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'


class AvaliacaoTutor(models.Model):
    nota = models.IntegerField()
    comentario = models.TextField()
    data_hora = models.DateTimeField()

    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='tutor')
    
    class Meta:
        verbose_name_plural = 'Avaliações do tutor'


class AvaliacaoCuidador(models.Model):
    nota=models.IntegerField()
    comentario=models.TextField()
    data_hora=models.DateTimeField()

    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE, related_name='avaliacaocuidador')

    class Meta:
        verbose_name_plural = 'Avaliações do cuidador'

class ImagensAmbiente(models.Model):
    fotos_local=models.ImageField()

    class Meta:
        verbose_name_plural = 'Imagens do ambiente'

    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE, related_name='imagensambiente')

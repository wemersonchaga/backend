from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Modelo base abstrato
class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128, default='123456')
    foto_perfil = models.ImageField(
        upload_to='uploads/',
        default='defaults/avatar_padrao.png',
        blank=True
        )
    
    class Meta:
        abstract = True

# Tutor - dono do pet
class Tutor(Pessoa):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tutor')
    plataforma_indicacao = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'

# Modelo para porte de pet
class Porte(models.Model):
    nome = models.CharField(max_length=20, choices=(
        ('pequeno', 'Pequeno'),
        ('medio', 'Médio'),
        ('grande', 'Grande'),
    ))

    def __str__(self):
        return self.get_nome_display()  # retorna 'Pequeno', 'Médio', etc.

# Cuidador - quem hospeda pets
class Cuidador(Pessoa):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cuidador')
    telefone = models.CharField(max_length=15)
    cep = models.CharField(max_length=8, null=True)
    estado = models.CharField(max_length=100, null=True)
    cidade = models.CharField(max_length=100, null=True)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10, default='S/N')
    descricao = models.TextField()
    instagram = models.CharField(max_length=100, blank=True, null=True)
    disponivel = models.BooleanField(default=True)  # Novo campo
    caracteristicas = models.ManyToManyField('CaracteristicasCuidador', blank=True, related_name='cuidadores')
    preco_diaria = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0)],
        verbose_name="Preço por diária"
    )
    portes_aceitos = models.ManyToManyField(Porte, blank=True, related_name='cuidadores')

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'

# Pet do tutor
class Pet(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='pets')
    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raca = models.CharField(max_length=50, blank=True, null=True)
    porte = models.CharField(max_length=20, choices=[
        ('pequeno', 'Pequeno'),
        ('medio', 'Médio'),
        ('grande', 'Grande')
    ])
    idade = models.PositiveIntegerField()
    castrado = models.BooleanField(default=False)
    genero = models.CharField(max_length=10, choices=[('Macho', 'Macho'), ('Fêmea', 'Fêmea')])
    foto = models.ImageField(upload_to='pets/', blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.nome} ({self.especie})'

# Pedido de hospedagem (solicitação do tutor)
class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('recusado', 'Recusado'),
        ('cancelado', 'Cancelado'),
    ]

    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='pedidos')
    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE, related_name='pedidos_recebidos')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    observacoes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido de {self.tutor.nome} para {self.pet.nome} ({self.status})'

# Pedido de hospedagem (aceito=confirmada pelo cuidador)
class Hospedagem(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='hospedagens')
    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE, related_name='hospedagens')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='hospedagens')
    pedido = models.OneToOneField(Pedido, on_delete=models.SET_NULL, null=True, blank=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('confirmada', 'Confirmada'),
        ('em_andamento', 'Em andamento'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ], default='confirmada')
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.pet.nome} hospedado com {self.cuidador.nome}"
    
# Avaliação de cuidadores
class AvaliacaoCuidador(models.Model):
    hospedagem = models.OneToOneField(Hospedagem, on_delete=models.CASCADE, related_name='avaliacao')
    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE, related_name='avaliacoes')
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.PositiveSmallIntegerField()
    comentario = models.TextField(blank=True)
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Avaliação para {self.cuidador.nome} - Nota {self.nota}'

# Características do cuidador
class CaracteristicasCuidador(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

# Imagens do ambiente do cuidador
class ImagemAmbiente(models.Model):
    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE, related_name='imagens')
    foto = models.ImageField(upload_to='ambientes/')

    def __str__(self):
        return f'Imagem do ambiente - {self.cuidador.nome}'

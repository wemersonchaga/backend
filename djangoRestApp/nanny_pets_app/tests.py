from django.test import TestCase
from .models import Tutor, Cuidador, Pet, Pedido, Hospedagem

class PedidoHospedagemSignalTest(TestCase):
    def setUp(self):
        # Criar Tutor
        self.tutor = Tutor.objects.create(
            nome='João', sobrenome='Silva', cpf='12345678901',
            email='joao@email.com', senha='senha123'
        )
        # Criar Cuidador
        self.cuidador = Cuidador.objects.create(
            nome='Maria', sobrenome='Souza', cpf='98765432100',
            email='maria@email.com', senha='senha123',
            telefone='11999999999', cep='12345678',
            estado='SP', cidade='São Paulo', rua='Rua A', numero='123'
        )
        # Criar Pet
        self.pet = Pet.objects.create(
            tutor=self.tutor,
            nome='Bob',
            especie='Cachorro',
            porte='medio',
            idade=3
        )

    def test_cria_hospedagem_apos_pedido_aprovado(self):
        pedido = Pedido.objects.create(
            tutor=self.tutor,
            cuidador=self.cuidador,
            pet=self.pet,
            data_inicio='2025-08-01',
            data_fim='2025-08-10',
            status='aprovado',
            observacoes='Cuidar bem do Bob'
        )
        # Verifica se hospedagem foi criada
        hospedagem = Hospedagem.objects.filter(pedido=pedido).first()
        self.assertIsNotNone(hospedagem, 'Hospedagem não foi criada automaticamente')
        self.assertEqual(hospedagem.status, 'confirmada')
        self.assertEqual(hospedagem.pet, self.pet)
        self.assertEqual(hospedagem.cuidador, self.cuidador)
        self.assertEqual(hospedagem.tutor, self.tutor)
        self.assertEqual(hospedagem.observacoes, 'Cuidar bem do Bob')

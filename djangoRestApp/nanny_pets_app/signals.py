from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pedido, Hospedagem

@receiver(post_save, sender=Pedido)
def criar_hospedagem_ao_aprovar_pedido(sender, instance, created, **kwargs):
    if instance.status == 'aprovado':
        # Verifica se já existe hospedagem criada para esse pedido
        if not Hospedagem.objects.filter(pedido=instance).exists():
            Hospedagem.objects.create(
                pedido=instance,
                tutor=instance.tutor,
                cuidador=instance.cuidador,
                pet=instance.pet,
                data_inicio=instance.data_inicio,
                data_fim=instance.data_fim,
                observacoes=instance.observacoes,
                status='confirmada'
            )

# filters.py
from django_filters import rest_framework as filters
from .models import Cuidador, CaracteristicasCuidador

class CuidadorFilter(filters.FilterSet):
    caracteristicas = filters.ModelMultipleChoiceFilter(
        field_name='caracteristicas__id',
        to_field_name='id',
        queryset=CaracteristicasCuidador.objects.all(),
        conjoined=False  # OR entre filtros, ou mude para True se quiser AND
    )

    cep = filters.CharFilter(field_name='cep', lookup_expr='exact')
    disponivel = filters.BooleanFilter(field_name='disponivel')

    class Meta:
        model = Cuidador
        fields = ['caracteristicas', 'cep', 'disponivel']

    # se quiser pode manter o __init__ para personalizar queryset, mas já setei direto

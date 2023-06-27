import django_filters
from .models import *
from django_filters import CharFilter


class InstrumentFilter(django_filters.FilterSet):
    note = CharFilter(field_name='instrument_name', lookup_expr='icontains')

    class Meta:
        model = MusicalInstrument
        fields = ['note', 'category', 'manufacturer', 'instrument_price']

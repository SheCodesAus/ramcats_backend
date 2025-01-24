from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from .models import Opportunity

class OpportunityFilter(FilterSet):
    organisation_name = CharFilter(field_name='owner__organisation__name', lookup_expr='icontains')
    organisation_id = CharFilter(field_name='owner__organisation__id', lookup_expr='exact')
    class Meta:
        model = Opportunity
        fields = ['eligibility','discipline','type','attendance_mode', 'location', 'organisation_name', 'organisation_id']


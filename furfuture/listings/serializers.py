from rest_framework import serializers
from django.apps import apps
from .models import Eligibility, Type, Discipline

class ListingSerializer(serializers.ModelSerializer):
    eligibility = serializers.PrimaryKeyRelatedField(queryset=Eligibility.objects.all(), many=True)
    type = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all(), many=True)
    discipline = serializers.PrimaryKeyRelatedField(queryset=Discipline.objects.all(), many=True)
    class Meta:
        model = apps.get_model('listings.Listing')
        fields = '__all__'

class EligibilitySerializer(serializers.ModelSerializer):
        class Meta:
            model = apps.get_model('listings.Eligibility')
            fields='__all__'

class DisciplineSerializer(serializers.ModelSerializer):
        class Meta:
            model = apps.get_model('listings.Discipline')
            fields='__all__'
class TypeSerializer(serializers.ModelSerializer):
        class Meta:
            model = apps.get_model('listings.Type')
            fields='__all__'
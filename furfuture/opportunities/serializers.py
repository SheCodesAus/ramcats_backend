from rest_framework import serializers
from django.apps import apps
from .models import Eligibility, Type, Discipline

class OpportunitySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    organisation = serializers.SerializerMethodField()
    eligibility = serializers.PrimaryKeyRelatedField(queryset=Eligibility.objects.all(), many=True)
    type = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all(), many=True)
    discipline = serializers.PrimaryKeyRelatedField(queryset=Discipline.objects.all(), many=True)
    class Meta:
        model = apps.get_model('opportunities.Opportunity')
        fields = '__all__'
    
    def get_organisation(self,obj):
          if obj.owner and obj.owner.organisation:
                return{
                      "id": obj.owner.organisation.id,
                      "name": obj.owner.organisation.name,
                      "website": obj.owner.organisation.website,
                      "description": obj.owner.organisation.description,
                      "logo": obj.owner.organisation.logo,

                }
          return None
class EligibilitySerializer(serializers.ModelSerializer):
        class Meta:
            model = apps.get_model('opportunities.Eligibility')
            fields='__all__'

class DisciplineSerializer(serializers.ModelSerializer):
        class Meta:
            model = apps.get_model('opportunities.Discipline')
            fields='__all__'
class TypeSerializer(serializers.ModelSerializer):
        class Meta:
            model = apps.get_model('opportunities.Type')
            fields='__all__'

class NestedOpportunitySerializer(serializers.ModelSerializer):
    eligibility = serializers.PrimaryKeyRelatedField(queryset=Eligibility.objects.all(), many=True)
    type = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all(), many=True)
    discipline = serializers.PrimaryKeyRelatedField(queryset=Discipline.objects.all(), many=True)
    class Meta:
        model = apps.get_model('opportunities.Opportunity')
        exclude = ['owner']

class OpportunityDetailSerializer(OpportunitySerializer):
    eligibilities = EligibilitySerializer(many=True, read_only=True)
    disciplines = DisciplineSerializer(many=True, read_only=True)
    types = TypeSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if instance.is_archive:
             instance.is_open = False
        instance.save()
        return instance
  
class EligibilityDetailSerializer(EligibilitySerializer):
     def update(self, instance, validated_data):
          instance.description =  validated_data.get('description', instance.description)
          instance.save()
          return instance
class DisciplineDetailSerializer(DisciplineSerializer):
     def update(self, instance, validated_data):
          instance.description =  validated_data.get('description', instance.description)
          instance.save()
          return instance
class TypeDetailSerializer(TypeSerializer):
     def update(self, instance, validated_data):
          instance.description =  validated_data.get('description', instance.description)
          instance.save()
          return instance
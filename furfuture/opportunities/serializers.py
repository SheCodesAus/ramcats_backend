from rest_framework import serializers
from django.apps import apps
from .models import Eligibility, Type, Discipline


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
class GetOpportunitySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    organisation = serializers.SerializerMethodField()
    eligibility = EligibilitySerializer(many=True, read_only=True)
    type = TypeSerializer (many=True, read_only=True)
    discipline = DisciplineSerializer (many=True, read_only=True)
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

class PostOpportunitySerializer(serializers.ModelSerializer):
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
class NestedOpportunitySerializer(serializers.ModelSerializer):
    eligibility = serializers.PrimaryKeyRelatedField(queryset=Eligibility.objects.all(), many=True)
    type = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all(), many=True)
    discipline = serializers.PrimaryKeyRelatedField(queryset=Discipline.objects.all(), many=True)
    class Meta:
        model = apps.get_model('opportunities.Opportunity')
        exclude = ['owner']

# class OpportunityDetailSerializer(GetOpportunitySerializer):
#     # eligibilities = EligibilitySerializer(many=True, read_only=True)
#     # disciplines = DisciplineSerializer(many=True, read_only=True)
#     # types = TypeSerializer(many=True, read_only=True)

class UpdateOpportunityDetailSerializer(PostOpportunitySerializer):
    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            if field == "eligibility":
                instance.eligibility.set(value)
            elif field == "type":
                instance.type.set(value)
            elif field == "discipline":
                instance.discipline.set(value)
            else:
                setattr(instance, field, value)
        if instance.is_archive:
             instance.is_open = False
        # if 'eligibility' in validated_data:
        #     eligibility_data = validated_data.pop('eligibility')
        #     instance.eligibility.set(eligibility_data)
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
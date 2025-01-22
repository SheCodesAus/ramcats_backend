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

class OpportunityDetailSerializer(OpportunitySerializer):
  eligibilities = EligibilitySerializer(many=True, read_only=True)
  disciplines = DisciplineSerializer(many=True, read_only=True)
  types = TypeSerializer(many=True, read_only=True)

  def update(self, instance, validated_data): #instance: The model instance being updated.validated_data: A dictionary of validated data from the request (after being checked by the serializer).
    instance.project_name = validated_data.get('project_name', instance.project_name) #Each field on the instance (like title, description, goal, etc.) is updated using validated_data.get().validated_data.get('field', instance.field) works by:Looking for the field in validated_data.If the field is present, it uses the new value; if not, it keeps the existing value (instance.field).
    instance.title = validated_data.get('title', instance.title)
    instance.description = validated_data.get('description', instance.description)
    instance.opportunity_url = validated_data.get('opportunity_url', instance.opportunity_url)
    instance.amount = validated_data.get('amount', instance.amount)
    instance.is_open = validated_data.get('is_open', instance.is_open)
    instance.create_date = validated_data.get('create_date', instance.create_date)
    instance.open_date = validated_data.get('end_date', instance.end_date)
    instance.close_date = validated_data.get('open_date', instance.open_date)
    instance.is_archive = validated_data.get('is_archive', instance.is_archive)
    instance.attendance_mode = validated_data.get('attendance_mode', instance.attendance_mode)
    instance.location = validated_data.get('location', instance.location)
    instance.owner = validated_data.get('owner', instance.owner)
    instance.save() #After all fields are updated, instance.save() writes the changes to the database.
    return instance #Finally, the method returns the updated instance.
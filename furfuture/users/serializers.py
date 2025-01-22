from rest_framework import serializers
from .models import CustomUser, Organisation
from opportunities.serializers import NestedOpportunitySerializer

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = "__all__"

class CustomUserSerializer(serializers.ModelSerializer):
    organisation = OrganisationSerializer()

    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        organisation_data = validated_data.pop('organisation')
        organisation, created = Organisation.objects.get_or_create(
            name=organisation_data['name'],
            defaults={'logo': organisation_data.get('logo'), 'website': organisation_data.get('website'), 'description': organisation_data.get('description')})
        
        if not created:
            organisation.logo = organisation_data.get('logo',organisation.logo)
            organisation.website = organisation_data.get('website',organisation.website)
            organisation.description = organisation_data.get('description',organisation.description)

        user = CustomUser.objects.create_user(
            organisation=organisation,
            **validated_data
        )
        return user

class CustomUserDetailSerializer(CustomUserSerializer):
    owned_opportunities = NestedOpportunitySerializer(many=True, read_only=True)

    def update(self,instance,validated_data):
        instance.username = validated_data.get('username',instance.username)
        password = validated_data.get('password',None)
        if password:
            instance.set_password(password)
        instance.email = validated_data.get('email', instance.email)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

class NestedCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','first_name','last_name','email']
    
class OrganisationDetailSerializer(OrganisationSerializer):
    users = NestedCustomUserSerializer(many=True, read_only=True)
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.website = validated_data.get('website', instance.website)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
from rest_framework import serializers
from .models import CustomUser, Organisation
from opportunities.serializers import NestedOpportunitySerializer

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = "__all__"

class CustomUserSerializer(serializers.ModelSerializer):
    organisation = OrganisationSerializer(required=False,allow_null=True)

    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, data):
        user_type = data.get("user_type")
        organisation = data.get("organisation",None)
        
        if user_type == CustomUser.APPLICANT and organisation is not None:
            raise serializers.ValidationError({"organisation": "Applicants should not have an organisation."})
        
        if user_type == CustomUser.ORGANISATION and organisation is None:
            raise serializers.ValidationError({"organisation": "Organisations must have an associated organisation."})
        return data


    def create(self, validated_data):
        organisation_data = validated_data.pop('organisation',None)
        organisation = None

        if organisation_data:
            organisation, created = Organisation.objects.get_or_create(
                name=organisation_data['name'],
                defaults={
                    'logo': organisation_data.get('logo'), 
                    'website': organisation_data.get('website'), 
                    'description': organisation_data.get('description')})
        
            if not created:
                organisation.logo = organisation_data.get('logo',organisation.logo)
                organisation.website = organisation_data.get('website',organisation.website)
                organisation.description = organisation_data.get('description',organisation.description)
                organisation.save()

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
    

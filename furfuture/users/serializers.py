from rest_framework import serializers
from .models import CustomUser, Organisation

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

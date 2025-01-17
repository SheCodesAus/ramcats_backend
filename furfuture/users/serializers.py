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
        organisation, created = Organisation.objects.get_or_create(name=organisation_data['name'])
        return CustomUser.objects.create(organisation=organisation, **validated_data)

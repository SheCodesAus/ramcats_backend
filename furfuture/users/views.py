from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, Organisation
from .serializers import CustomUserSerializer, CustomUserDetailSerializer, OrganisationDetailSerializer, OrganisationSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class CustomUserList(APIView):
   def get(self, request):
       users = CustomUser.objects.select_related('organisation').all()
       serializer = CustomUserSerializer(users, many=True)
       return Response(serializer.data)

   def post(self, request):
       serializer = CustomUserSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(
               serializer.data,
               status=status.HTTP_201_CREATED
           )
       return Response(
           serializer.errors, 
           status=status.HTTP_400_BAD_REQUEST
       )

class CustomUserDetail(APIView):
   def get_object(self, pk):
       try:
           return CustomUser.objects.get(pk=pk)
       except CustomUser.DoesNotExist:
           raise Http404

   def get(self, request, pk):
       user = self.get_object(pk)
       serializer = CustomUserDetailSerializer(user)
       return Response(serializer.data)
   
   def put(self, request, pk):
       user = self.get_object(pk)
       serializer = CustomUserDetailSerializer(
           instance = user,
           data= request.data,
           partial=True
       )

       if serializer.is_valid():
           serializer.save()
           return Response(
               serializer.data,
               status=status.HTTP_202_ACCEPTED
           )
       return Response(
           serializer.errors,
           status=status.HTTP_400_BAD_REQUEST)
   
   def delete(self,request,pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

   
class OrganisationList(APIView):
    def get(self,request):
        organisations = Organisation.objects.all()
        serializer = OrganisationSerializer(organisations, many=True)
        return Response(serializer.data)

class OrganisationDetailView(APIView):
    def get_object(self, pk):
       try:
           return Organisation.objects.get(pk=pk)
       except Organisation.DoesNotExist:
           raise Http404
    
    def get(self,request,pk):
        organisation = self.get_object(pk)
        serializer = OrganisationDetailSerializer(organisation)
        return Response(serializer.data)
    
    def put(self, request, pk):
        organisation = self.get_object(pk)
        serializer = OrganisationDetailSerializer(
            instance = organisation,
            data = request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_202_ACCEPTED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
   

class CustomAuthToken(ObtainAuthToken):
  def post(self, request, *args, **kwargs):
      serializer = self.serializer_class(
          data=request.data,
          context={'request': request}
      )
      serializer.is_valid(raise_exception=True)
      user = serializer.validated_data['user']
      token, created = Token.objects.get_or_create(user=user)

      return Response({
          'token': token.key,
          'user_id': user.id,
          'email': user.email
      })
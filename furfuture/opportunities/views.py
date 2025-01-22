from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Opportunity, Eligibility, Discipline, Type, SavedOpportunity
from django.shortcuts import get_object_or_404
from .serializers import OpportunitySerializer, EligibilitySerializer, DisciplineSerializer, TypeSerializer

class OpportunityList(APIView):
    def get(self,request):
        opportunities = Opportunity.objects.all()
        serializer = OpportunitySerializer(opportunities, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = OpportunitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response (
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class SavedOpportunityView(APIView):
    def post(self,request, opportunity_id):
        user = request.user
        if user.user_type != user.APPLICANT:
            return Response({"detail": "Only applicants can save opportunities."}, status=status.HTTP_400_BAD_REQUEST)
        opportunity = get_object_or_404(Opportunity,id=opportunity_id)
        if SavedOpportunity.objects.filter(applicant=user, opportunity=opportunity).exists():
            return Response({"detail": "You have already saved this opportunity."}, status=status.HTTP_400_BAD_REQUEST)
        SavedOpportunity.objects.create(applicant=user, opportunity=opportunity)
        return Response({"detail": "Opportunity saved successfully."}, status=status.HTTP_201_CREATED)
    
    def get(self,request):
        user=request.user
        if user.user_type != user.APPLICANT:
            return Response({"detail": "Only applicants can view saved opportunities."}, status=status.HTTP_400_BAD_REQUEST)
        saved_opportunities = user.saved_opportunities.all()
        serializer = OpportunitySerializer(saved_opportunities, many=True)
        return Response(serializer.data)
    
    def delete(self,request,opportunity_id):
        opportunity = get_object_or_404(Opportunity,id=opportunity_id)
        opportunity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EligibilityList(APIView):
    def get(self,request):
        eligibilities = Eligibility.objects.all()
        serializer = EligibilitySerializer(eligibilities, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = EligibilitySerializer(data=request.data)
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
class DisciplineList(APIView):
    def get(self,request):
        disciplines = Discipline.objects.all()
        serializer = DisciplineSerializer(disciplines, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = DisciplineSerializer(data=request.data)
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
class TypeList(APIView):
    def get(self,request):
        types = Type.objects.all()
        serializer = TypeSerializer(types, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TypeSerializer(data=request.data)
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
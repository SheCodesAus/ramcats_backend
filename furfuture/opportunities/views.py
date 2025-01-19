from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Opportunity, Eligibility, Discipline, Type
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
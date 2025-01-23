from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Opportunity, Eligibility, Discipline, Type, SavedOpportunity
from django.shortcuts import get_object_or_404
from .serializers import OpportunitySerializer, EligibilitySerializer, DisciplineSerializer, TypeSerializer, OpportunityDetailSerializer, EligibilityDetailSerializer, TypeDetailSerializer, DisciplineDetailSerializer

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
        saved_opportunities = SavedOpportunity.objects.filter(applicant=user).select_related('opportunity')
        opportunities = [saved_opportunity.opportunity for saved_opportunity in saved_opportunities]
        serializer = OpportunitySerializer(opportunities, many=True)
        return Response(serializer.data)
    
    def delete(self,request,opportunity_id):
        user=request.user
        if user.user_type != user.APPLICANT:
            return Response({"detail": "Only applicants can remove saved opportunities."}, status=status.HTTP_400_BAD_REQUEST)
        saved_opportunity = get_object_or_404(SavedOpportunity,applicant=request.user, opportunity__id=opportunity_id)
        saved_opportunity.delete()
        return Response({"detail": "Opportunity removed from saved opportunities."}, status=status.HTTP_204_NO_CONTENT)

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
    
class OpportunityDetail(APIView):

    def get_object(self, pk):
        try:
            opportunity = Opportunity.objects.get(pk=pk)
            return opportunity
        except Opportunity.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        opportunity = self.get_object(pk)
        serializer = OpportunityDetailSerializer(opportunity)
        return Response(serializer.data)
    
    
    def put(self, request, pk):
        opportunity = self.get_object(pk)
        serializer = OpportunityDetailSerializer(
        instance=opportunity,
        data=request.data,
        partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):
        opportunity = self.get_object(pk)
        opportunity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EligibilityDetailView(APIView):
    def get_object(self, pk):
       try:
           return Eligibility.objects.get(pk=pk)
       except Eligibility.DoesNotExist:
           raise Http404
    
    def get(self,request,pk):
        eligibility = self.get_object(pk)
        serializer = EligibilityDetailSerializer(eligibility)
        return Response(serializer.data)
    
    def put(self, request, pk):
        eligibility = self.get_object(pk)
        serializer = EligibilityDetailSerializer(
            instance = eligibility,
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
class EligibilityDetailView(APIView):
    def get_object(self, pk):
       try:
           return Eligibility.objects.get(pk=pk)
       except Eligibility.DoesNotExist:
           raise Http404
    
    def get(self,request,pk):
        eligibility = self.get_object(pk)
        serializer = EligibilityDetailSerializer(eligibility)
        return Response(serializer.data)
    
    def put(self, request, pk):
        eligibility = self.get_object(pk)
        serializer = EligibilityDetailSerializer(
            instance = eligibility,
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
    
    def delete(self, request, pk):
        eligibility = self.get_object(pk)
        eligibility.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TypeDetailView(APIView):
    def get_object(self, pk):
       try:
           return Type.objects.get(pk=pk)
       except Type.DoesNotExist:
           raise Http404
    
    def get(self,request,pk):
        type = self.get_object(pk)
        serializer = TypeDetailSerializer(type)
        return Response(serializer.data)
    
    def put(self, request, pk):
        type = self.get_object(pk)
        serializer = TypeDetailSerializer(
            instance = type,
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
    
    def delete(self, request, pk):
        type = self.get_object(pk)
        type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class DisciplineDetailView(APIView):
    def get_object(self, pk):
       try:
           return Discipline.objects.get(pk=pk)
       except Discipline.DoesNotExist:
           raise Http404
    
    def get(self,request,pk):
        discipline = self.get_object(pk)
        serializer = DisciplineDetailSerializer(discipline)
        return Response(serializer.data)
    
    def put(self, request, pk):
        discipline = self.get_object(pk)
        serializer = DisciplineDetailSerializer(
            instance = discipline,
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
    def delete(self, request, pk):
        discipline = self.get_object(pk)
        discipline.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
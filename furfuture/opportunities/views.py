from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Opportunity, Eligibility, Discipline, Type
from .serializers import OpportunitySerializer, EligibilitySerializer, DisciplineSerializer, TypeSerializer, OpportunityDetailSerializer

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
    
class OpportunityDetail(APIView): #This creates a class-based view named ProjectDetail that inherits from APIView. It handles operations on a single Project instance (i.e., detail view).

    def get_object(self, pk): #This method is used to retrieve a Project object based on its primary key (pk)
        try: #: It attempts to fetch the Project object from the database using Project.objects.get(pk=pk), where pk is the unique identifier for the project.
            opportunity = Opportunity.objects.get(pk=pk)
            self.check_object_permissions(self.request, opportunity)
            return opportunity.objects.get(pk=pk) #If the Project exists, it is returned.
        except Opportunity.DoesNotExist: #If the Project with the given pk does not exist, it raises an Http404 exception, which tells the client that the requested resource was not found.
            raise Http404

    def get(self, request, pk): #This method handles GET requests to retrieve the details of a specific Project.
        opportunity = self.get_object(pk) #project = self.get_object(pk): It calls the get_object method to fetch the Project object with the specified pk. If the object doesn't exist, it will raise a 404 error.
        serializer = OpportunityDetailSerializer(opportunity) #It passes the project object to the ProjectSerializer to convert it into a serialized format (e.g., JSON) suitable for an API response.
        return Response(serializer.data) #It returns the serialized data as a JSON response to the client.
    
    
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
    
    #Add a delete method (exercise)
    def delete(self, request, pk):
        opportunity = self.get_object(pk)
        opportunity.delete()  # Deletes the project from the database
        return Response(status=status.HTTP_204_NO_CONTENT)  # Responds with a 204 status code
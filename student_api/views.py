from django.shortcuts import render, HttpResponse, get_object_or_404
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, mixins, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet


from .models import Student, Path
from .serializers import StudentSerializer, PathSerializer


def home(request):
    return HttpResponse('<h1>API Page</h1>')

#? HTTP methods -------->>>
# - GET (DB den veri çağırma, read)
# - POST (DB de değişiklik, create)
# - PUT (DB de değişiklik, update)
# - DELETE (DB de değişiklik, delete)
# - PATCH (DB de değişiklik, partially update)

@api_view(["GET"])
def student_api(request):
    student = Student.objects.all()  # data type : queryset
    serializer = StudentSerializer(student, many=True) # data type : querydict
    return Response(serializer.data)   # data type : JSON

@api_view(["POST"])
def student_create(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        message = {"message": "Student successfully created.."}
        return Response(message, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def student_detail(request, pk):
    # student = Student.objects.get(id=pk)
    student = get_object_or_404(Student, id=pk)
    serializer = StudentSerializer(student)
    return Response(serializer.data)

@api_view(["PATCH"])
def student_update(request, pk):
    student = get_object_or_404(Student, id=pk)
    serializer = StudentSerializer(instance=student, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        # message = {"message": "Student successfully updated.."}
        data = serializer.data
        data["message"] = "Student successfully updated.."
        return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def student_delete(request, pk):
    student = get_object_or_404(Student, id=pk)
    student.delete()
    message = {"message": "Student successfully deleted.."}
    return Response(message, status=status.HTTP_200_OK)

###############################################################
@api_view(['GET', 'POST'])
def student_api(request):
    if request.method == 'GET':
        students = Student.objects.all()  # queryset (complex data types)
        serializer = StudentSerializer(students, many=True) # python data types (dict , querydict)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": f"Student {serializer.validated_data.get('first_name')} saved successfully!"}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def student_api_get_update_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": f"Student {student.last_name} updated successfully"
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": f"Student {student.last_name} updated successfully"
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        student.delete()
        data = {
            "message": f"Student {student.last_name} deleted successfully"
        }
        return Response(data)
    
    
#!################### CLASS VIEWS  ###########################################

#! APIView class
class StudentListCreate(APIView):
    
    def get(self, request):
        student = Student.objects.all()  # data type : queryset
        serializer = StudentSerializer(student, many=True) # data type : querydict
        return Response(serializer.data)   # data type : JSON
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = {"message": "Student successfully created.."}
            return Response(message, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StudentDetail(APIView):
    
    def get(self, request, pk):
        student = get_object_or_404(Student, id=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data),
    
    def put(self, request, pk):
        student = get_object_or_404(Student, id=pk)
        serializer = StudentSerializer(instance=student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # message = {"message": "Student successfully updated.."}
            data = serializer.data
            data["message"] = "Student successfully updated.."
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        student = get_object_or_404(Student, id=pk)
        student.delete()
        message = {"message": "Student successfully deleted.."}
        return Response(message, status=status.HTTP_200_OK)
    
#! GenericApiView class and Mixins

""" One of the key benefits of class-based views is the way they allow you to compose bits of reusable behavior. REST framework takes advantage of this by providing a number of pre-built views that provide for commonly used patterns.

GenericAPIView class extends REST framework's APIView class, adding commonly required behavior for standard list and detail views. Some Basic Attributes and Methods. """

#? Mixins

""" The mixin classes provide the actions that are used to provide the basic view behavior. Note that the mixin classes provide action methods rather than defining the handler methods, such as .get() and .post(), directly. This allows for more flexible composition of behavior. Tek başlarına bir işlem yapamazlar. GenericAPIView ile anlamlı oluyor

The mixin classes can be imported from rest_framework.mixins.

- ListModelMixin
    - list method
- CreateModelMixin
    - create method
- RetrieveModelMixin
    - retrieve method
- UpdateModelMixin
    - update method
- DestroyModelMixin
    - destroy method """
    
class StudentGAV(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    
class StudentDetailViewGAV(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

#! Concrete Views

class StudentCV(ListCreateAPIView):

    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentDetailCV(RetrieveUpdateDestroyAPIView):
    
    queryset = Student.objects.all()
    serializer_class = StudentSerializer  
    
     
    
#! Viewsets
from .pagination import MyNumberPagination,MyLimitPaginatian,MyCursorPaginatian
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

class StudentMVS(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class=MyNumberPagination 
    # pagination_class=MyLimitPaginatian 
    # pagination_class=MyCursorPaginatian
    # def get_queryset(self):
    #     queryset = Student.objects.all()
    #     path=self.request.query_params.get('cohort')
    #     if path:
    #         my_path=Path.objects.get(path_name=path)
    #         queryset=queryset.filter(path=my_path.id)
    #     return queryset
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields=['first_name','last_name'] # Filtreleme yapılacak fieldlar. tam eşleşenleri getirir.
    search_fields = ['last_name', ]             # Arama yapılacak fieldlar. SQL deki LIKE '%%' komutu gibi arama yapar.
    ordering_fields=['number',]                 # sıralama yapılmasına izin verilecek fieldlar

class PathMVS(ModelViewSet):
    queryset= Path.objects.all()
    serializer_class = PathSerializer
    filter_backends=[DjangoFilterBackend,]
    filterset_fields=['path_name',]

        
    
    
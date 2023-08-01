from django.urls import path, include
from rest_framework import routers
from .views import (
    home, 
    student_api, student_api_get_update_delete,
    student_api, 
    student_create, 
    student_detail, 
    student_update,
    student_delete,
    StudentListCreate,
    StudentDetail,
    StudentGAV,
    StudentDetailViewGAV,
    StudentCV,
    StudentDetailCV,
    StudentMVS,
    PathMVS
    )

router = routers.DefaultRouter()
router.register( "student", StudentMVS)
router.register( "path", PathMVS)

urlpatterns = [
    path('', home),
    
    #! Func endpoints
    # path('student/', student_api),
    # path('student/<int:pk>/', student_api_get_update_delete, name = "detail"),
    
    # path("student-list/", student_api, name="list"),
    # path("student-create/", student_create, name="create"),
    # path("student-detail/<int:pk>", student_detail, name="detail"),
    # path("student-update/<int:pk>", student_update, name="update"),
    # path("student-delete/<int:pk>", student_delete, name="delete"),
    
    #! Class endpoints
    # path("student/", StudentListCreate.as_view()),
    # path("student/<int:pk>", StudentDetail.as_view()),
    
    # path("student/", StudentGAV.as_view()),
    # path("student/<int:pk>", StudentDetailViewGAV.as_view()),
    
    # path("student/", StudentCV.as_view()),
    # path("student/<int:pk>", StudentDetailCV.as_view()),
    
    path("", include(router.urls))
]




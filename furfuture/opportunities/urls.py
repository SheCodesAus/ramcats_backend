from django.urls import path
from . import views

urlpatterns = [
    path('opportunities/', views.OpportunityList.as_view()),
    path('eligibilities/', views.EligibilityList.as_view()),
    path('disciplines/', views.DisciplineList.as_view()),
    path('types/', views.TypeList.as_view()),
    path('opportunities/<int:pk>/', views.OpportunityDetail.as_view())
]
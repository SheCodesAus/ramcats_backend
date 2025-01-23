from django.urls import path
from . import views

urlpatterns = [
    path('opportunities/', views.OpportunityList.as_view()),
    path('eligibilities/', views.EligibilityList.as_view()),
    path('disciplines/', views.DisciplineList.as_view()),
    path('types/', views.TypeList.as_view()),
    path('opportunities/<int:pk>/', views.OpportunityDetail.as_view()),
    path('eligibilities/<int:pk>/', views.EligibilityDetailView.as_view()),
    path('disciplines/<int:pk>/', views.DisciplineDetailView.as_view()),
    path('types/<int:pk>/', views.TypeDetailView.as_view()),
    path('saved-opportunities/', views.SavedOpportunityView.as_view()),
    path('saved-opportunities/<int:opportunity_id>/', views.SavedOpportunityView.as_view()),
]
from django.urls import path
from . import views

urlpatterns = [
  path('users/', views.CustomUserList.as_view()),
  path('users/<int:pk>/', views.CustomUserDetail.as_view()),
  path('org/', views.OrganisationList.as_view()),
  path('org/<int:pk>/', views.OrganisationDetailView.as_view()),
]
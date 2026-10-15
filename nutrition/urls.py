from django.urls import path

from nutrition.views import SignUpView,GetMeView

from nutrition.views import FoodLogListCreateView,FoodLogRetrieveUpdateDeleteView

from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns=[
    path('signup/',SignUpView.as_view()),

    path('me/',GetMeView.as_view()),

    path('token/',ObtainAuthToken.as_view()),    

    path('foodlogs/',FoodLogListCreateView.as_view()),

    path('foodlogs/<int:pk>/',FoodLogRetrieveUpdateDeleteView.as_view()),
    
]
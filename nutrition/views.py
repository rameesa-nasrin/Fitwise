from django.shortcuts import render

from django.contrib.auth.models import User

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import authentication,permissions

from rest_framework.generics import RetrieveAPIView,UpdateAPIView,DestroyAPIView

from nutrition.serializers import UserSerializer,FoodLogSerializer

from nutrition.models import Foodlog
# Create your views here.


class SignUpView(APIView):

    def post(self,request):

        form_data = request.data

        serializer_instance = UserSerializer(data=form_data)

        if serializer_instance.is_valid():

            cleaned_data = serializer_instance.validated_data

            qs = User.objects.create_user(**cleaned_data)

            serializer_instance = UserSerializer(qs)

            return Response(serializer_instance.data)

        else:

            return Response(serializer_instance.errors)

class GetMeView(APIView):

    authentication_classes = [authentication.BasicAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        auth_user = request.user

        instance = User.objects.get(username=auth_user)

        serializer_instance = UserSerializer(instance)

        return Response(data=serializer_instance.data)

class FoodLogListCreateView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        instance = Foodlog.objects.filter(owner=request.user)

        serializer_instance = FoodLogSerializer(instance,many=True)

        return Response(serializer_instance.data)


    def post(self,request):

        form_data = request.data

        serializer_instance = FoodLogSerializer(data=form_data)

        if serializer_instance.is_valid():

            serializer_instance.save(owner=request.user)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

class FoodLogRetrieveUpdateDeleteView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,pk=None):

        instance = Foodlog.objects.get(owner=request.user,id=pk)

        serializer_instance = FoodLogSerializer(instance)

        return Response(serializer_instance.data)

    

    



        
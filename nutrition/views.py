from django.shortcuts import render

from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User

from django.db.models import Sum


from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import authentication,permissions

from rest_framework.generics import RetrieveAPIView,UpdateAPIView,DestroyAPIView


from nutrition.serializers import UserSerializer,FoodLogSerializer

from nutrition.models import Foodlog

from nutrition.permissions import IsOwner

from nutrition.ai_service import get_diet_plan


from datetime import datetime
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

    permission_classes = [IsOwner]

    def get(self,request,pk=None):

        instance = get_object_or_404(Foodlog,id=pk)

        self.check_object_permissions(request,instance)

        serializer_instance = FoodLogSerializer(instance)

        return Response(data=serializer_instance.data)

    def put(self,request,pk=None):

        instance = get_object_or_404(Foodlog,id=pk)

        self.check_object_permissions(request,instance)

        form_data = request.data

        serializer_instance = FoodLogSerializer(data=form_data,instance=instance)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)


    def delete(self,request,pk=None):

        instance  = get_object_or_404(Foodlog,id=pk)

        instance.delete()

        return Response(data={"message":"deleted"})


class FoodLogSummaryView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [IsOwner]

    def get(self,request):

        response_data = {
            "todays_category_summary":0
        }

        curr_date = datetime.today().date()

        todays_foodlog = Foodlog.objects.filter(owner=request.user,
                                                created_at__date=curr_date)

        if todays_foodlog:

            todays_category_summary = todays_foodlog.values("meal_type").annotate(total=Sum("calorie"))

            response_data["todays_category_summary"] = todays_category_summary

        return Response(data=response_data)

class DietPlanView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [IsOwner]

    def get(self,request):

        response_data = {
            "monthly_total_calorie":0
        }

        curr_year = datetime.now().year

        curr_month = datetime.now().month

        

        monthly_food_log = Foodlog.objects.filter(owner=request.user,
                                                  created_at__month=curr_month,
                                                  created_at__year=curr_year
                                            )

        if monthly_food_log:

            monthly_total_calorie = monthly_food_log.values("calorie").aggregate(total=Sum("calorie")).get("total")

            response_data["monthly_total_calorie"] = monthly_total_calorie

            monthly_category_summary = monthly_food_log.values("meal_type").annotate(total=Sum("calorie"))

            response_data["monthly_category_summary"] = monthly_category_summary

            diet_plan = get_diet_plan(response_data)

            response_data["diet_plan"] = diet_plan
            
        return Response(data=response_data)


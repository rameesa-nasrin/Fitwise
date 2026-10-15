from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Foodlog(models.Model):

    MEAL_TYPE_CHOICES =[
        ("BREAKFAST","breakfast"),
        ("LUNCH","lunch"),
        ("DINNER","dinner"),
        ("SNACKS","snacks")
    ]

    owner = models.ForeignKey(User,on_delete = models.CASCADE,related_name='food_logs')

    title = models.CharField(max_length=100)

    calorie = models.PositiveIntegerField()

    meal_type = models.CharField(max_length=20,choices=MEAL_TYPE_CHOICES)

    serving_size = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.title






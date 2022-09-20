from django.db import models
from django.conf import settings
from .validators import validate_unit_of_measure
from .utils import number_str_to_float
from django.urls import reverse
import pint
from django.db.models import Q
import pathlib
import uuid

class MealStatus(models.TextChoices):
    PENDING = 'p', 'Pending'
    COMPLETED = 'c', 'Completed'
    EXPIRED = 'e', 'Expired'
    ABORTED = 'a', 'Aborted'
    
    
class MealQuerySet(models.QuerySet):
    def pending(self):
        


class MealManager(models.Manager):
    def get_queryset(self):
        return MealQuerySet(self.model, using=self._db)


class Meal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=MealStatus.choices, default=MealStatus.PENDING)

    obj = MealManager()

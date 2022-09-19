from django.db import models
from django.conf import settings
from .validators import validate_unit_of_measure
from .utils import number_str_to_float
from django.urls import reverse
import pint
from django.db.models import Q
import pathlib
import uuid


class RecipeQuerySet(models.QuerySet):
    def search(self, query=None):
        print(query)
        if query is None or query == "":
            return self.none()
        lookups = (
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(directions__icontains=query)
        )
        # title__icontains=query
        return self.filter(lookups)


class RecipeManager(models.Manager):
    def get_queryset(self):
        return RecipeQuerySet(self.model, using=self._db)


class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    obj = RecipeManager()

    @property
    def title(self):
        return self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'id': self.id})

    def get_hx_url(self):
        return reverse('recipes:hx-detail', kwargs={'id': self.id})

    def get_edit_url(self):
        return reverse('recipes:update', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('recipes:delete', kwargs={'id': self.id})

    def get_ingredients_child(self):
        return self.recipeingredients_set.all()


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    quantity = models.CharField(max_length=50)
    quantity_as_float = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=50, validators=[
                            validate_unit_of_measure])
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        self.recipe.get_abolute_url()
        # return reverse('', kwargs={'pk': self.pk})

    def get_hx_edit_url(self):
        return reverse('recipes:hx-ingredient-detail', kwargs={'parent_id': self.recipe.id, 'id': self.id})

    def get_delete_url(self):
        return reverse('recipes:ingredient-delete', kwargs={'parent_id': self.recipe.id, 'id': self.id})

    def convert_to_system(self, system='mks'):
        if self.quantity_as_float is None:
            return None
        ureg = pint.UnitRegistry(system=system)
        measurement = self.quantity_as_float * ureg(self.unit)
        print(measurement)
        return measurement.to_base_units()
    # .to('kilogram')    #

    def as_mks(self):
        measurement = self.convert_to_system(system='mks')
        print(measurement)
        return measurement.to_base_units()

    def as_imperial(self):
        measurement = self.convert_to_system(system='imperial')
        print(measurement)
        return measurement

    def save(self, *args, **kwargs):
        qty = self.quantity
        qty_as_float, qty_float_success = number_str_to_float(qty)
        if qty_float_success:
            self.quantity_as_float = qty_as_float
        else:
            self.quantity_as_float = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


def recipe_ingredient_image_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1())
    return f"recipes/ingredient/{new_fname}{fpath.suffix}"


class RecipeIngredientImage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    image = models.FileField(upload_to=recipe_ingredient_image_upload_handler)

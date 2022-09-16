from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Recipe, RecipeIngredients

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(
            'abdulwahab', password='abdulwahab')

    def test_userpw(self):
        checked = self.user_a.check_password('abdulwahab')
        self.assertTrue(checked)


class RecipeTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(
            'abdulwahab', password='abdulwahab')
        self.recipe_a = Recipe.objects.create(
            name='Chicked',
            user=self.user_a
        )
        self.recipe_b = Recipe.objects.create(
            name='Chicked Grilled',
            user=self.user_a
        )
        self.recipe_ingredients_a = RecipeIngredients.objects.create(
            recipe=self.recipe_a,
            name='Chicken',
            quantity='1/2',
            unit='pound'
        )
        self.recipe_ingredients_b = RecipeIngredients.objects.create(
            recipe=self.recipe_a,
            name='Shake',
            quantity='asd',
            unit='pound',
        )
    def test_user_count(self):
        qs = User.objects.all()
        self.assertTrue(qs.count(), 1)

    # def test_user_recipe(self):
    #     user = self.user_a
    #     qs = user.recipe_set.all()
    #     self.assertEqual(qs.count(), 0)

    def test_user_recipe_reverse_count(self):
        user = self.user_a
        qs = user.recipe_set.all()
        self.assertEqual(qs.count(), 2)

    def test_user_recipe_forward_count(self):
        user = self.user_a
        qs = Recipe.objects.filter(user=user)
        print(qs)
        self.assertEqual(qs.count(), 2)

    def test_recipe_ingredient_reverse_count(self):
        recipe = self.recipe_a
        qs = recipe.recipeingredients_set.all()
        self.assertEqual(qs.count(), 2)

    def test_user_recipe_ingredient_count(self):
        recipe = self.recipe_a
        qs = RecipeIngredients.objects.filter(recipe=recipe)
        print(qs)
        self.assertEqual(qs.count(), 2)

    def user_two_level_relation(self):
        user = self.user
        qs = RecipeIngredients.objects.filter(recipe__user=recipe)
        self.assertEqual(qs.count(), 2)

    def user_two_level_relation_reverse(self):
        user = self.user
        recipeingredient = list(user.recipe_set.all().values_list(
            'recipeingredient__id', flat=True))
        qs = RecipeIngredients.objects.filter(id__in=recipeingredient_id)
        self.assertEqual(recipeingredient.count(), 2)

    def user_two_level_relation_via_recipe(self):
        user = self.user
        ids = user.recipe_set.all().values_list('id', flat=True)
        qs = RecipeIngredients.objects.filter(recipe__id__in=ids)
        self.assertEqual(qs.count(), 2)

    def test_unit_measure_validation(self):
        unit = 'ounce'
        with self.assertRaises(ValidationError):
            ingredient = RecipeIngredients(
                name='New',
                recipe=self.recipe_a,
                quantity=1,
                unit=unit
            )
            ingredient.full_clean()
            
    def test_unit_measure_validation_error(self):
        invalid_unit = 'adf'
        ingredient = RecipeIngredients(
            name='Strawbery Shake',
            recipe=self.recipe_a,
            quantity=1,
            unit=invalid_unit
        )
        ingredient.full_clean()
    
    def test_quantity_as_float(self):
        self.assertIsNotNone(self.recipe_ingredients_a.quantity_as_float)
        self.assertIsNone(self.recipe_ingredients_b.quantity_as_float)
        

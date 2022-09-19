from django.contrib import admin

from .models import Recipe, RecipeIngredients, RecipeIngredientImage
from django.contrib.auth import get_user_model

User = get_user_model()



# admin.site.unregister(User)

admin.site.register(RecipeIngredientImage)


# class RecipeInline(admin.StackedInline):
#     '''Tabular Inline View for '''
#     model = Recipe
#     # fields = ['name', 'quantity', 'unit', 'directions']
#     extra = 0


# class UserAdmin(admin.ModelAdmin):
#     '''Tabular Inline View for User'''
#     inlines = [RecipeInline]
#     list_display = ['username']
#     # model = User


# admin.site.register(User, UserAdmin)


class RecipeIngredientsInline(admin.StackedInline):
    '''Tabular Inline View for '''
    model = RecipeIngredients
    readonly_fields = ['quantity_as_float', 'as_mks', 'as_imperial']
    # fields = ['name', 'quantity', 'unit', 'directions']
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientsInline]
    list_display = ['name', 'user']
    readonly_fields = ['timestamp', 'updated']
    raw_id_fields = ['user']


admin.site.register(Recipe, RecipeAdmin)

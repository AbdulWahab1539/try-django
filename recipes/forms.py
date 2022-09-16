from django import forms


from .models import Recipe


class RecipeForm(forms.ModelForm):
    """Form definition for 
    Recipe."""

    class Meta:
        """Meta definition for 
        Recipeform."""

        model = Recipe
        fields = ['name', 'description', 'directions']

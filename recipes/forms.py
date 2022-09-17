from django import forms


from .models import Recipe, RecipeIngredients


class RecipeForm(forms.ModelForm):
    """Form definition for 
    Recipe."""
    required_css_class = 'required-field'
    error_css_class = 'error-field'
    # name = forms.CharField(widget=forms.TextInput(
    #     attrs={"class": "form-control", "placeholder": "Recipe Name"}))
    # description = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))

    class Meta:
        """Meta definition for 
        Recipeform."""

        model = Recipe
        fields = ['name', 'description', 'directions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            data = {
                'placeholder': f'Recipe {str(field)}',
                'class': 'form-control',
                # 'hx-post': '.',
                # 'hx-trigger': 'keyup changed delay:500ms',
                # 'hx-target': '#recipe-container',
                # 'hx-swap': 'outerHTML',
            }
            self.fields[str(field)].widget.attrs.update(data)

        self.fields['description'].widget.attrs.update({'rows': '2'})
        self.fields['directions'].widget.attrs.update({'rows': '4'})


class RecipeIngredientForm(forms.ModelForm):
    """Form definition for 
    RecipeIngredients."""

    class Meta:
        """Meta definition for 
        RecipeIngredientForm."""

        model = RecipeIngredients
        fields = ['name', 'quantity', 'unit']

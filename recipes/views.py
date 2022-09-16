from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory

from .models import Recipe, RecipeIngredients
from .forms import RecipeForm, RecipeIngredientForm


@login_required
def recipe_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    context = {
        'object_list': qs
    }
    return render(request, 'recipes/list.html', context)


@login_required
def recipe_detail_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    # qs = Recipe.objects.filter(user=request.user)
    context = {
        'object': obj
    }
    return render(request, 'recipes/detail.html', context)


@login_required
def recipe_create_view(request):
    form = RecipeForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, 'recipes/create-update.html', context)


@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    form_2 = RecipeIngredientForm(request.POST or None)
    # Formset = modelformset_factory()
    RecipeIngredientFormSet = modelformset_factory(
        RecipeIngredients, form=RecipeIngredientForm, extra=0)
    qs = obj.recipeingredients_set.all()
    formset = RecipeIngredientFormSet(request.POST or None, queryset=qs)
    # ingredient_forms = []
    # for ingredient_obj in obj.recipeingredients_set.all():
    #     ingredient_forms.append(
    #         RecipeIngredientForm(request.POST or None, instance=ingredient_obj)
    #     )
    context = {
        'form': form,
        'formset': formset,
        # 'ingredient_forms': ingredient_forms,
        'object': obj,
    }

    # my_forms = all([form.is_valid() for form in ingredient_forms])
    # if my_forms and form.is_valid():
    if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.save()
        for form in formset:
            # for form_2 in ingredient_forms:
            child = form.save(commit=False)
            # if child.recipe is None:
            child.recipe = parent
            child.save()
        context['message'] = 'Data Updated Successfully'
        if request.htmx:
            return render(request, 'recipes/partials/forms.html', context)
    return render(request, 'recipes/create-update.html', context)

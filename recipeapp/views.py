from django.shortcuts import render, HttpResponsePermanentRedirect, reverse

from recipeapp.models import Recipe, Author
from recipeapp.forms import RecipeForm, AuthorForm

def index(request):
    my_recipes = Recipe.objects.all()
    my_authors = Author.objects.all()
    return render(request, 'index.html', {'recipes': my_recipes, 'authors': my_authors})

def recipe_detail(request, recipe_id):
    my_recipe = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe_detail.html", {'recipe': my_recipe})

def author_detail(request, author_id):
    current_author = Author.objects.filter(id=author_id).first()
    current_recipes = Recipe.objects.filter(author=current_author)
    return render(request, "author_detail.html", {'author': current_author, 'recipes': current_recipes})

def recipe_form_view(request):
    if request.method == "POST":
        form  = RecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get('title'),
                description=data.get('description'),
                time_required=data.get('time_required'),
                instructions=data.get('instructions'),
                author=data.get('author')
            )
            return HttpResponsePermanentRedirect(reverse('home'))
    form = RecipeForm()
    return render(request, "generic_form.html", {"form": form})


def author_form_view(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        form.save()
        return HttpResponsePermanentRedirect(reverse('home'))
    form = AuthorForm()
    return render(request, 'generic_form.html', {"form": form})
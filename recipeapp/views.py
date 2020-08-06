from django.shortcuts import render

from recipeapp.models import Recipe, Author

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
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from recipeapp.models import Recipe, Author
from recipeapp.forms import RecipeForm, AuthorForm, LoginForm, SignupForm

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

def error_view(request):
    return render(request, 'error.html')

@login_required
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
                author=request.user.author
            )
            return HttpResponseRedirect(reverse('home'))
    form = RecipeForm()
    return render(request, "generic_form.html", {"form": form})

@login_required
def author_form_view(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = AuthorForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_user = User.objects.create_user(username=data.get("username"), password=data.get("password"))
                Author.objects.create(name=data.get("username"), bio=data.get("bio"), user=new_user)
                return HttpResponseRedirect(reverse('home'))
        form = AuthorForm()
        return render(request, 'generic_form.html', {"form": form})
    else:
        return HttpResponseRedirect(reverse('error'))

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get("username"), password=data.get("password"))
            if user:
                login(request, user)
                # return HttpResponseRedirect(reverse("home"))
                return HttpResponseRedirect(request.GET.get('next', reverse("home")))

    form = LoginForm()
    return render(request, "generic_form.html", {"form": form})

def signup_view(request):
    if request.method =="POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(username=data.get("username"), password=data.get("password"))
            Author.objects.create(name=data.get("username"), bio=data.get("bio"), user=new_user)
            login(request, new_user)
            return HttpResponseRedirect(reverse("home"))

    form = SignupForm()
    return render(request, "generic_form.html", {"form": form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))

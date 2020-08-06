from django.contrib import admin

from recipeapp.models import Author, Recipe
# Register your models here.

admin.site.register(Author)
admin.site.register(Recipe)
from database.models import *
from django.db.models import F

def getCamps():
    return Camp.objects.all()

def getCampsSection(section_name):
    return Camp.objects.filter(section__name = section_name)

def getRecipes():
    return Recipe.objects.select_related('tags').order_by('name')

def getIngredients():
    return Ingredient.objects.all()

def getMenu(date, moment, camp):
    return Menu.objects.filter(date=date, moment=moment, camp=camp).values('id', 'camp_id', 'nbr_anim', 'nbr_leaders', 'nbr_vege', 'date', 'moment', 'recipe').first()

def getMenuId(date, moment, camp):
    return Menu.objects.filter(date=date, moment=moment, camp=camp).values('id').first()

def getMenuCamp(camp):
    return Menu.objects.all().filter(camp=camp).order_by('date')

def getEngredientsFromRecipe(recipe):
    return Recipe.objects.prefetch_related('ingredients').all().filter(pk=recipe)

def getIngredient(engredient):
    return Ingredient.objects.all().filter(pk=engredient).first()

def isvege(engredient):
    return Ingredient.objects.all().filter(pk=engredient)

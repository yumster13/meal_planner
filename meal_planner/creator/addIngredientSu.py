from collections import defaultdict
from django.db import transaction
from . import databse_access
from database.models import *
from django.http import HttpResponse

from collections import defaultdict
from django.db import transaction
from . import databse_access
from database.models import *
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

def generate_ingredient_su(request):
    IngredientXSU.objects.all().delete()
    camps = databse_access.getCamps()

    # Global dictionary to track ingredient quantities across all camps
    global_ingredient_dict = defaultdict(lambda: {'quantity': 0, 'measurement': '', 'categories': ''})

    for camp in camps:
        name = camp.section.name
        age = camp.section.age
        menus = databse_access.getMenuCamp(camp)
        
        for menu in menus:
            recipe = databse_access.getEngredientsFromRecipe(menu.recipe.id)
            
            for recipexingredient in recipe:
                for ingredient in recipexingredient.ingredients.all():
                    ingredient_info = databse_access.getIngredient(ingredient.id)
                    
                    if ingredient_info.vege:
                        quantity_vege = ingredient.quantity * menu.nbr_vege if ingredient.age == 'GG' else 0
                    else:
                        quantity_vege = 0

                    quantity_anim = ingredient.quantity * menu.nbr_anim if ingredient.age == age else 0
                    quantity_lead = ingredient.quantity * menu.nbr_leaders if ingredient.age == 'GG' else 0

                    total_quantity = quantity_lead + quantity_anim + quantity_vege
                    categories = ingredient_info.category.name

                    key = ingredient_info.name
                    
                    if key in global_ingredient_dict:
                        global_ingredient_dict[key]['quantity'] += total_quantity
                    else:
                        global_ingredient_dict[key] = {
                            'id': ingredient_info.id,
                            'quantity': total_quantity,
                            'measurement': ingredient_info.mesurement,
                            'categories': categories,
                        }
    from django.shortcuts import get_object_or_404

    for ingredient_name, info in global_ingredient_dict.items():
        print(ingredient_name,"   :",info)
        ingredient_obj = get_object_or_404(Ingredient, name=ingredient_name)
        
        ingredient_xsu, created = IngredientXSU.objects.get_or_create(
            ingredient=ingredient_obj
        )
        ingredient_xsu.su = False
        ingredient_xsu.quantity += info['quantity']
        ingredient_xsu.category = info['categories']
        ingredient_xsu.save()

    return HttpResponse("Ingredients updated successfully.")


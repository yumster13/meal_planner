from . import databse_access

import pandas as pd
from django.http import HttpResponse
import os
import zipfile
from io import BytesIO

def calculate_quantities(request):
    camps = databse_access.getCamps()
    temp_dir = 'temp_files'

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    excel_files = []

    for camp in camps:
        engredient_dict = []
        name = camp.section.name
        age = camp.section.age
        menus = databse_access.getMenuCamp(camp)
        for menu in menus:
            print('recipe', menu.recipe.id)
            recipe = databse_access.getEngredientsFromRecipe(menu.recipe.id)
            print(recipe)
            for recipexengredient in recipe:
                for engredient in recipexengredient.ingredients.all():
                    print(engredient.age)
                    engredient_info = databse_access.getIngredient(engredient.id)
                    print(engredient_info.vege)
                    if engredient_info.vege:
                        if engredient.age == 'GG':
                            quantity_vege = engredient.quantity * menu.nbr_vege 
                    if engredient.age == age:
                        print('engredient\n', engredient.quantity)
                        quantity_anim = engredient.quantity * menu.nbr_anim

                    if engredient.age == 'GG':
                        quantity_lead = engredient.quantity * menu.nbr_leaders
                    else:
                        quantity_lead = 0
                        quantity_vege = 0
                    print(recipe)
                    categories = ""
                    for category in engredient_info.category.all():
                        categories += str(category.name)
                    print()
                    engredient_dict.append([menu.date, recipe[0].name, engredient_info.name, (quantity_lead + quantity_anim + quantity_vege), categories])
        print('menu\n', menus)
        print(engredient_dict)

        # Write to Excel file
        df = pd.DataFrame(engredient_dict, columns=['Date', 'Recipe Name', 'Ingredient Name', 'Total Quantity', 'Categories'])
        excel_file_path = os.path.join(temp_dir, f'ingredients_{camp.name}.xlsx')
        df.to_excel(excel_file_path, index=False)
        excel_files.append(excel_file_path)

    # Create a zip file containing all the Excel files
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for file_path in excel_files:
            zip_file.write(file_path, os.path.basename(file_path))

    # Serve the zip file as a download
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="ingredients.zip"'

    # Clean up temporary files
    for file_path in excel_files:
        os.remove(file_path)
    os.rmdir(temp_dir)

    return response

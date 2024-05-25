from django.shortcuts import render, redirect
from database.models import *
from .forms import *
# Create your views here.
from django.contrib import messages
from . import databse_access
from django.conf import settings
from django.core.mail import send_mail
from .generate_password import generate_password
from django.contrib.auth.models import User,Group
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse

def staff_member_required(view_func):
    decorated_view_func = user_passes_test(
        lambda user: user.is_active and user.is_staff,
        login_url='camps',  # The URL to redirect to if the user is not a staff member
        redirect_field_name=None
    )(view_func)
    return decorated_view_func


@staff_member_required
def home(request):

    context = {'home':True, 'user_form':CreateUser}
    return render(request,"home.html",context)


def CreateCamp(request):
    if request.method == 'POST':
        camp_form = CampForm(request.POST)
        if camp_form.is_valid():
            camp_form.save()
            messages.success(request, "Camp Created")
            return redirect('camps')
        else:
            messages.error(request, "Camp error")
            return render(request, "camp.html", {'camp_form': camp_form})
    else:
        camp_form = CampForm()
        return render(request, "camp.html", {'camp_form': camp_form, 'camp': True})
    
@login_required
def Camps(request):
    if request.user.is_staff :
        camps = databse_access.getCamps()
    else:
        camps=databse_access.getCampsSection(request.user.groups.all()[0])
    camp_form = CampForm()
    context = {'camps':camps,'camp':True, 'camp_form': camp_form}
    return render(request,'camps.html',context)

def Recipes(request):
    recipes = databse_access.getRecipes()
    recipe_dict = {}
    for recipe in recipes:
        #print(recipe.tags)
        recipe_dict[recipe.name] = {'prairie':recipe.prairie,'tags': recipe.tags.name if recipe.tags else '','avg_price':recipe.calculate_total_price(Ages.PG)}
   # print(recipe_dict)
    context = {'recipes':recipe_dict,'recipe':True}
    return render(request,'recipes.html',context)

def Engredients(request):
    ingredients = databse_access.getIngredients()
    engredients_dict = {}
    for ingredient in ingredients:
        engredients_dict[ingredient.name] = {'unit':ingredient.mesurement,'cats': ingredient.category.all(),'avg_price':ingredient.avg_price,'seasons':ingredient.season.all()}
   # print(engredients_dict)
    context = {'engredients':engredients_dict,'engredient':True}
    return render(request,'engredients.html',context)

def CreateRecipe(request):
    recipeForm = RecipeForm()
    context = {'recipe_form':recipeForm,'recipe':True}
    return render(request,'recipe.html',context)

def CreateUserView(request):
    if request.method == 'POST':
        user_form = CreateUser(request.POST)
        if user_form.is_valid():
            email = user_form.data['email']
            section = user_form.data['section']
            subject = 'Bievenue à mealplanner'
            user = email[:email.rfind("@")]
            password = generate_password(15)
            user = User.objects.create_user(user,email,password)
            message = f'Bonjour, voici votre utilisateur et votre mot de passe utilisateur = {user}, mot de passe = {password} \nVoici le site internet pour vous connecter et modifier votre menu: https://menuplanner.pythonanywhere.com/ '
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            user.save()
            sectionobj = Section.objects.values('name').filter(id=section).first()
            sectionName = sectionobj['name']
            group = Group.objects.get_or_create(name=sectionName)
            group_id = Group.objects.values('id').filter(name=sectionName).first()
            user.groups.add(group_id['id'])
            send_mail( subject, message, email_from, recipient_list )
            messages.success(request, "L'utilisateur a été ajouté")
            context = {'home':True, 'user_form':CreateUser}
            return render(request,"home.html",context)
        else:
            messages.error(request, "Erreur en ajoutant l'utilisateur")
            context = {'home':True, 'user_form':CreateUser}
            return render(request,"home.html",context)
        

def displayRecipes(request):
    databse_access.getRecipes()
from datetime import datetime,timedelta
def get_date_range(start_date, end_date):
    # Convert the input strings to datetime objects if they are strings
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Generate the list of dates
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)

    return date_list

def DisplayMenuCamp(request, camp):
    camp_objects = Camp.objects.get(id=camp)
    menus = Menu.objects.filter(camp=camp_objects).order_by('date')
    dates = get_date_range(camp_objects.from_date, camp_objects.to_date)
    menu_dict = {}
    date_dict = {}

    for date in dates:
        matin_menu = databse_access.getMenu(date, Moment.MATIN, camp_objects)
        midi_menu = databse_access.getMenu(date, Moment.MIDI, camp_objects)
        gouter_menu = databse_access.getMenu(date, Moment.GOUTER, camp_objects)
        souper_menu = databse_access.getMenu(date, Moment.SOUPER, camp_objects)
        cinquieme_menu = databse_access.getMenu(date, Moment.CINQIEME, camp_objects)
        #print(matin_menu if matin_menu else None)
        menu_dict[date.day] = [
            MenuForm(initial=matin_menu if matin_menu else {'moment': Moment.MATIN, 'date': date}),
            MenuForm(initial=midi_menu if midi_menu else {'moment': Moment.MIDI, 'date': date}),
            MenuForm(initial=gouter_menu if gouter_menu else {'moment': Moment.GOUTER, 'date': date}),
            MenuForm(initial=souper_menu if souper_menu else {'moment': Moment.SOUPER, 'date': date}),
            MenuForm(initial=cinquieme_menu if cinquieme_menu else {'moment': Moment.CINQIEME, 'date': date}),
        ]
        date_dict[date.day] = date

    section = camp_objects.section
    context = {
        'menus': menus,
        'camp_objects': camp_objects,
        'menu_form': MenuForm(initial={'moment': Moment.MATIN}),
        'search': SearchDate,
        'menu_dict': menu_dict,
        'date_dict': date_dict
    }
    return render(request, "camp_menu.html", context)


def addMenuToCamp(request, camp):
    camp_instance = get_object_or_404(Camp, pk=camp)
    if request.method == 'POST':
        menu_form = MenuForm(request.POST)
        if menu_form.is_valid():
            if databse_access.getMenuId(camp=camp, date=menu_form.cleaned_data['date'], moment=menu_form.cleaned_data['moment']) is not None:
                Menu.objects.filter(camp=camp, date=menu_form.cleaned_data['date'], moment=menu_form.cleaned_data['moment']).delete()
            if camp_instance.from_date <= menu_form.cleaned_data['date'] <= camp_instance.to_date:
                menu_instance = menu_form.save(commit=False)
                menu_instance.camp = camp_instance
                menu_instance.save()
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': "Ajout du menu"})
                messages.success(request, "Ajout du menu")
                return DisplayMenuCamp(request, camp)
            else:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': "Mauvaise date"})
                messages.error(request, "Mauvaise date")
                return DisplayMenuCamp(request, camp)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': menu_form.errors})
            messages.error(request, menu_form.errors)
    else:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': "Erreur durant l'exécution"})
        messages.error(request, "Erreur durant l'exécution")
    return DisplayMenuCamp(request, camp)

def DeleteMenuCamp(request,camp,menu):
    Menu.objects.filter(pk=menu).delete()
    return DisplayMenuCamp(request,camp)


def FinishCamp(request,camp):
    Camp.objects.filter(pk=camp).update(status=Status.F)
    return DisplayMenuCamp(request, camp)   

def ResetCampStatus(request,camp):
    Camp.objects.filter(pk=camp).update(status=Status.C)
    return Camps(request)   

def RedirectView(request):
    pass
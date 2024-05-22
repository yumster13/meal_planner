from django.contrib import admin
from django.urls import path
from .views import *
from .create_csv import calculate_quantities
urlpatterns = [
    path('admin/home',home,name="home"),
    path('camp/create',CreateCamp,name="createCamp"),
    path('camps',Camps,name="camps"),
    path('camps/menus/<str:camp>',DisplayMenuCamp,name="menus"),
    path('camps/addMenu/<str:camp>',addMenuToCamp,name="addMenu"),
    path('camps/saveMenu/<str:camp>',addMenuToCamp,name="addMenu"),
    path('camps/delete/menu/<str:camp>/<str:menu>/',DeleteMenuCamp,name="deleteMenu"),
    path('camps/setFinished/<str:camp>',FinishCamp,name="setFinished"),
    path('camps/resetStatus/<str:camp>',ResetCampStatus,name="resetStatus"),
    path('recipes',Recipes,name="recipes"),
    path('engredients',Engredients,name="engredients"),
    path('recipe/create',CreateRecipe,name="createRecipe"),
    path('user/create',CreateUserView,name="createUser"),
    path('camps/calculate_quantities',calculate_quantities,name="calculate_quantities"),

]
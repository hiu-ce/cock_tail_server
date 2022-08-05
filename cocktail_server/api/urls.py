from django.urls import path
from . import views

urlpatterns = [
    path('cocktail',views.cocktails),
    path('cocktail/<str:pk>',views.cocktail),
    path('recipes',views.recipes),
    path('search',views.search),
    path('reset',views.reset),
    path('ingredients',views.ingredients),
    path('todaydrink',views.todaydrink),   
]
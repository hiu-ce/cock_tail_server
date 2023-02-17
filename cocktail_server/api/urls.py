from django.urls import path
from . import views

urlpatterns = [
    path('cocktails',views.cocktails),
    path('base',views.base),
    path('sub',views.sub),
    path('juice',views.juice),
    path('other',views.other),
    path('glasses',views.glasses),
    path('glasses/<str:pk>',views.glass),
    path('cocktail/<str:pk>',views.cocktail),
    path('recipes',views.recipes),
    # # path('search',views.search),
    # # path('reset',views.reset),
    # path('ingredients',views.ingredients),
    # # path('todaydrink',views.todaydrink),   
]
from django.urls import path
from . import views

urlpatterns = [
    path('cocktails',views.cocktails),
    path('cocktails/<str:pk>',views.cocktail),
    path('bases',views.bases),
    path('bases/<str:pk>',views.base),
    path('subs',views.subs),
    path('subs/<str:pk>',views.sub),
    path('juices',views.juice),
    path('juices/<str:pk>',views.juice),    
    path('others',views.others),
    path('others<str:pk>',views.other),
    path('glasses',views.glasses),
    path('glasses/<str:pk>',views.glass),
    path('recipes',views.recipes),
    path('search',views.search),
    # # path('reset',views.reset),
    path('ingredients',views.ingredients),
    # # path('todaydrink',views.todaydrink),   
]
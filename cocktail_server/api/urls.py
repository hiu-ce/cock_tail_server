from django.urls import path
from . import views

urlpatterns = [
    path('cocktails',views.cocktails), # 칵테일 레시피 전체 출력
    path('cocktails/<str:pk>',views.cocktail), # 레시피 일부 출력
    path('cocktail_names',views.cocktail_names), # 칵테일 이름 전체 출력
    path('ingredients',views.ingredients), # 조합 재료 전체 출력
    path('ingredients/bases',views.bases),
    path('ingredients/bases/<str:pk>',views.base),
    path('ingredients/subs',views.subs),
    path('ingredients/subs/<str:pk>',views.sub),
    path('ingredients/juices',views.juices),
    path('ingredients/juices/<str:pk>',views.juice),    
    path('ingredients/others',views.others),
    path('ingredients/others/<str:pk>',views.other),
    path('glasses',views.glasses),
    path('glasses/<str:pk>',views.glass),
    path('hashtags',views.hashtags),
    path('hashtags/<str:pk>',views.hashtag),
    path('search',views.search),
    # # path('reset',views.reset),
    path('today-drink',views.todaydrink),   
]
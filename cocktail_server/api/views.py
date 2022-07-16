from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Base,Sub,Juice,Other,Cocktail
from .serializers import CocktailSerializer, BaseSerializer, SubSerializer, CocktailNameSerializer, OtherSerializer, JuiceSerializer

# Create your views here.

@csrf_exempt
def cocktail(request):
    if request.method == 'GET':
        query_set = Cocktail.objects.all()
        serializer = CocktailSerializer(query_set,many = True)
        return JsonResponse(serializer.data, safe = False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CocktailSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 200)
        else:
            return JsonResponse(serializer.error, status = 400)

    elif request.method == 'PUT': # 여기 어떻게 해야할까
        data = JSONParser().parse(request)
        obj = Cocktail.objects.get(cocktail_name = data['cocktail_name'])
        serializer = CocktailSerializer(obj,data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 200)
        else:
            return JsonResponse(serializer.error, status = 400)

    elif request.method == 'DELETE':
        cocktails = Cocktail.objects.all()
        cocktails.delete()
        return HttpResponse(200)

def recipes(request):
    if request.method == 'GET':
        query_set = Cocktail.objects.all()
        names = CocktailNameSerializer(query_set, many = True)
        return JsonResponse(names.data, safe = False)


@csrf_exempt
def search(request): # base filtering 예외처리 필요
    if request.method == 'GET':
        base_data = list(request.GET['base'].split(',')) 
        sub_data = list(request.GET['sub'].split(',')) 
        juice_data = list(request.GET['juice'].split(',')) 
        other_data = list(request.GET['other'].split(','))

        query_set = Cocktail.objects.all()
        for name in base_data:
            if Base.objects.filter(drink_name = name).exists():
                data = Base.objects.get(drink_name = name).cocktails.all()
                query_set = query_set and data

        for name in sub_data:
            if Sub.objects.filter(drink_name = name).exists():
                data = Sub.objects.get(drink_name = name).cocktails.all()
                query_set = query_set and data
                print(query_set)

        for name in juice_data:
            if Juice.objects.filter(drink_name = name).exists():
                data = Juice.objects.get(drink_name = name).cocktails.all()
                query_set = query_set and data
                print(query_set)

        for name in other_data:
            if Other.objects.filter(name = name).exists():
                data = Other.objects.get(name = name).cocktails.all()
                query_set = query_set and data
                print(query_set)
        
        serializer = CocktailNameSerializer(query_set, many = True)
        return JsonResponse(serializer.data, safe = False)


def ingredients(request):
    if request.method == 'GET':
        type = request.GET['type']
        if type == 'base':
            query_set = Base.objects.all()
            serializer = BaseSerializer(query_set,many = True)

        if type == 'sub':
            query_set = Sub.objects.all()
            serializer = SubSerializer(query_set,many = True)

        if type == 'juice':
            query_set = Juice.objects.all()
            serializer = JuiceSerializer(query_set,many = True)

        if type == 'other':
            query_set = Other.objects.all()
            serializer = OtherSerializer(query_set,many = True)
        
        return JsonResponse(serializer.data, safe = False)
        

def reset(request):
    if request.method == 'GET' or request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':
        Cocktail.objects.all().delete()
        Base.objects.all().delete()
        Sub.objects.all().delete()
        Juice.objects.all().delete()
        Other.objects.all().delete()

        return HttpResponse(status = 200)
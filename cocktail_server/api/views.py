from urllib import response
from xml.dom.minidom import Attr
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Base,Sub,Juice,Other,Cocktail
from .serializers import CocktailSerializer, BaseSerializer, SubSerializer, CocktailNameSerializer, OtherSerializer, JuiceSerializer, IngredientsSerializer
# Create your views here.

@csrf_exempt
def cocktails(request):
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
            if AttributeError:
                error_data = {"error_code":400, "error_message":f"{data['cocktail_name']}는 이미 존재하는 칵테일입니다"}
                return JsonResponse(error_data, status = 400)
            else:
                return JsonResponse(serializer.error, status = 400)

@csrf_exempt
def cocktail(request,pk):
    #obj = Cocktail.objects.get(cocktail_name = pk) 예외처리 ???

    if request.method == 'GET':
        obj = Cocktail.objects.get(cocktail_name = pk)
        serializer = CocktailSerializer(obj)
        return JsonResponse(serializer.data, safe=False)
        
    elif request.method == 'PUT': # 여기 어떻게 해야할까
        data = JSONParser().parse(request)
        obj = Cocktail.objects.get(cocktail_name = pk)
        serializer = CocktailSerializer(obj,data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 200)
        else:
            return JsonResponse(serializer.error, status = 400)

    elif request.method == 'DELETE':
        obj = Cocktail.objects.get(cocktail_name = pk)
        obj.delete()
        return HttpResponse(status=200)
    return 

def recipes(request):
    if request.method == 'GET':
        query_set = Cocktail.objects.all()
        names = CocktailNameSerializer(query_set, many = True)
        return JsonResponse(names.data, safe = False)


@csrf_exempt
def search(request): # base filtering 예외처리 필요
    if request.method == 'GET':
        error_code = None
        query_set = Cocktail.objects.all()

        if 'base' in request.GET:
            base_data = list(request.GET['base'].split(',')) 
            for name in base_data:
                if Base.objects.filter(drink_name = name).exists(): #여기 예외처리 error_code 필요
                    data = Base.objects.get(drink_name = name).cocktails.all()
                    query_set = query_set&data
                else:
                    error_code = 400
                    error_message = (f'there is no {name} in Base')
                
        if 'sub' in request.GET:
            sub_data = list(request.GET['sub'].split(',')) 
            for name in sub_data:
                if Sub.objects.filter(drink_name = name).exists():
                    data = Sub.objects.get(drink_name = name).cocktails.all()
                    query_set = query_set&data
                else:
                    error_code = 400
                    error_message = (f'there is no {name} in Base')

        if 'juice' in request.GET:
            juice_data = list(request.GET['juice'].split(',')) 
            for name in juice_data:
                if Juice.objects.filter(drink_name = name).exists():
                    data = Juice.objects.get(drink_name = name).cocktails.all()
                    query_set = query_set&data
                else:
                    error_code = 400
                    error_message = (f'there is no {name} in Juice')

        if 'other' in request.GET:
            other_data = list(request.GET['other'].split(','))
            for name in other_data:
                if Other.objects.filter(name = name).exists():
                    data = Other.objects.get(name = name).cocktails.all()
                    query_set = query_set&data
                else:
                    error_code = 400
                    error_message = (f'there is no {name} in Other')

        if not query_set:
            error_code = 400
            error_message = "없는 조합입니다"

        if error_code == None:
            serializer = CocktailNameSerializer(query_set, many = True)
            return JsonResponse(serializer.data, safe = False)
        else:
            response_data = {"error_code" : error_code, "error_message": error_message, "data" : []}
            return JsonResponse(response_data, status = 400)


def ingredients(request):
    if request.method == 'GET':
        if not 'type' in request.GET:
            base = BaseSerializer(Base.objects.all(),many=True)
            sub = SubSerializer(Sub.objects.all(),many = True)
            juice = JuiceSerializer(Juice.objects.all(), many= True)
            other = OtherSerializer(Other.objects.all(), many= True)
            serializer = IngredientsSerializer(data={'base':base.data,'sub': sub.data,'juice' : juice.data,'other' : other.data})
            if serializer.is_valid():
                return JsonResponse(serializer.data, safe = 200)
            else:
                return JsonResponse(serializer.data,status=200)
        else:
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
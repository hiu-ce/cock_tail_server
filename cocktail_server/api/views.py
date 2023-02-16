from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import views, response, status
from .models import Cocktail, Glass, Base, Sub, Juice, Other, CocktailBase, CocktailSub,CocktailJuice,CocktailOther
from .serializers import CocktailSerializer, GlassSerializer, BaseSerializer, SubSerializer,JuiceSerializer,OtherSerializer,CocktailNameSerializer

def check_cocktail_data(model,data): #칵테일 레시피 생성시 들어온 재료가 존재하는지 확인하는 함수
    for name in data.keys():
        if not model.objects.filter(name = name).exists():
            return False
    return True

@csrf_exempt
def cocktail(request):
    if request.method == 'GET': # 칵테일 레시피 전체 요청
        cocktails = Cocktail.objects.all()
        serializer = CocktailSerializer(cocktails, many=True)
        return JsonResponse(serializer.data,safe = False)

    elif request.method == 'POST': # 칵테일 레시피 등록
        data = JSONParser().parse(request)
        
        base_data = data.pop('base') #외래키 등록 필요한 항목들
        sub_data = data.pop('sub')
        juice_data = data.pop('juice')
        other_data = data.pop('other')
        glass_data = data.pop('glass')
        
        serializer = CocktailSerializer(data = data)
        
        # 유효성 검사
        if serializer.is_valid() and Glass.objects.filter(name = glass_data).exists() and check_cocktail_data(Base,base_data) and check_cocktail_data(Sub,sub_data) and check_cocktail_data(Juice,juice_data) and check_cocktail_data(Other,other_data):
            # 데이터 유효할 때
            cocktail = serializer.save()
            
            glass = get_object_or_404(Glass, name = glass_data) #Glass 연결
            cocktail.glass = glass
            
            for name in base_data.keys(): # base 연결
                base = get_object_or_404(Base, name = name)
                amount = base_data[name]
                CocktailBase.objects.create(cocktail = cocktail, base = base, amount = amount)

            for name in sub_data.keys(): # sub 연결
                sub = get_object_or_404(Sub, name = name)
                amount = sub_data[name]
                CocktailSub.objects.create(cocktail = cocktail, sub = sub, amount = amount)

            for name in juice_data.keys(): # other 연결
                juice = get_object_or_404(Juice, name = name)
                amount = juice_data[name]
                CocktailJuice.objects.create(cocktail = cocktail, juice = juice, amount = amount)

            for name in other_data.keys(): # other 연결
                other = get_object_or_404(Other, name = name)
                amount = other_data[name]
                CocktailOther.objects.create(cocktail = cocktail, other = other, amount = amount)
            
            cocktail.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        
        error_data = {"error_code":400, "error_message":f"invalid data"}
        return JsonResponse(error_data, status = 400)

    
@csrf_exempt
def glass(request):
    if request.method == 'GET':
        glass = Glass.objects.all()
        serializer = GlassSerializer(glass, many=True)
        return JsonResponse(serializer.data,safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = GlassSerializer(data = data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        
@csrf_exempt
def base(request):
    if request.method == 'GET':
        query_set = Base.objects.all()
        serializer = BaseSerializer(query_set,many = True)
        return JsonResponse(serializer.data, safe = False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BaseSerializer(data = data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 200)
        else:
            if AttributeError:
                error_data = {"error_code":400, "error_message":f"{data['name']}는 이미 존재하는 재료입니다"}
                return JsonResponse(error_data, status = 400)
            else:
                return JsonResponse(serializer.error, status = 400)
            
@csrf_exempt
def sub(request):
    if request.method == 'GET':
        query_set = Sub.objects.all()
        serializer = SubSerializer(query_set,many = True)
        return JsonResponse(serializer.data, safe = False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SubSerializer(data = data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 200)
        else:
            if AttributeError:
                error_data = {"error_code":400, "error_message":f"{data['name']}는 이미 존재하는 재료입니다"}
                return JsonResponse(error_data, status = 400)
            else:
                return JsonResponse(serializer.error, status = 400)

@csrf_exempt
def juice(request):
    if request.method == 'GET':
        query_set = Juice.objects.all()
        serializer = JuiceSerializer(query_set,many = True)
        return JsonResponse(serializer.data, safe = False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = JuiceSerializer(data = data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 200)
        else:
            if AttributeError:
                error_data = {"error_code":400, "error_message":f"{data['name']} is already exist"}
                return JsonResponse(error_data, status = 400)
            else:
                return JsonResponse(serializer.error, status = 400)            
            
@csrf_exempt
def other(request):
    if request.method == 'GET':
        query_set = Other.objects.all()
        serializer = OtherSerializer(query_set,many = True)
        return JsonResponse(serializer.data, safe = False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = OtherSerializer(data = data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 200)
        else:
            if AttributeError:
                error_data = {"error_code":400, "error_message":f"{data['name']} is already exist"}
                return JsonResponse(error_data, status = 400)
            else:
                return JsonResponse(serializer.error, status = 400) 
            
# @csrf_exempt
# def cocktail(request,pk):
#     #obj = Cocktail.objects.get(cocktail_name = pk) 예외처리 ???

#     if request.method == 'GET':
#         obj = Cocktail.objects.get(cocktail_name = pk)
#         serializer = CocktailSerializer(obj)
#         return JsonResponse(serializer.data, safe=False)
        
#     elif request.method == 'PUT': # 여기 어떻게 해야할까
#         data = JSONParser().parse(request)
#         obj = Cocktail.objects.get(cocktail_name = pk)
#         serializer = CocktailSerializer(obj,data = data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status = 200)
#         else:
#             return JsonResponse(serializer.error, status = 400)

#     elif request.method == 'DELETE':
#         cocktail = Cocktail.objects.get(cocktail_name = pk)
#         bases = cocktail.base_cocktail.all()
#         subs = cocktail.sub_cocktail.all()
#         juices = cocktail.juice_cocktail.all()
#         others = cocktail.other_cocktail.all()

#         for obj in bases:
#             obj.cocktails.remove(cocktail)
#             if not obj.cocktails.exists():
#                 obj.delete()

#         for obj in subs:
#             obj.cocktails.remove(cocktail)
#             if not obj.cocktails.exists():
#                 obj.delete()

#         for obj in juices:
#             obj.cocktails.remove(cocktail)
#             if not obj.cocktails.exists():
#                 obj.delete()

#         for obj in others:
#             obj.cocktails.remove(cocktail)
#             if not obj.cocktails.exists():
#                 obj.delete()

#         cocktail.delete()
#         return HttpResponse(status=200)

def recipes(request):
    if request.method == 'GET':
        query_set = Cocktail.objects.all()
        # names = CocktailNameSerializer(query_set, many = True)
        # return JsonResponse(names.data, safe = False)
        
        data = {"cocktails" : []}
        for cocktail in query_set:
            data["cocktails"].append(cocktail.name)
        return JsonResponse(data)


# @csrf_exempt
# def search(request): # base filtering 예외처리 필요
#     if request.method == 'GET':
#         error_code = None
#         query_set = Cocktail.objects.all()

#         if 'base' in request.GET:
#             base_data = list(request.GET['base'].split(',')) 
#             for name in base_data:
#                 if Base.objects.filter(drink_name = name).exists(): #여기 예외처리 error_code 필요
#                     data = Base.objects.get(drink_name = name).cocktails.all()
#                     query_set = query_set&data
#                 else:
#                     error_code = 400
#                     error_message = (f'there is no {name} in Base')
                
#         if 'sub' in request.GET:
#             sub_data = list(request.GET['sub'].split(',')) 
#             for name in sub_data:
#                 if Sub.objects.filter(drink_name = name).exists():
#                     data = Sub.objects.get(drink_name = name).cocktails.all()
#                     query_set = query_set&data
#                 else:
#                     error_code = 400
#                     error_message = (f'there is no {name} in Sub')

#         if 'juice' in request.GET:
#             juice_data = list(request.GET['juice'].split(','))
#             print(f'first query {query_set}')
#             for name in juice_data:
#                 if Juice.objects.filter(drink_name = name).exists():
#                     data = Juice.objects.get(drink_name = name).cocktails.all()
#                     query_set = query_set&data
#                 else:
#                     error_code = 400
#                     error_message = (f'there is no {name} in Juice')

#         if 'other' in request.GET:
#             other_data = list(request.GET['other'].split(','))
#             for name in other_data:
#                 if Other.objects.filter(name = name).exists():
#                     data = Other.objects.get(name = name).cocktails.all()
#                     query_set = query_set&data
#                 else:
#                     error_code = 400
#                     error_message = (f'there is no {name} in Other')


#         if not query_set:
#             error_code = 400
#             error_message = "없는 조합입니다"

#         if error_code == None:
#             serializer = CocktailNameSerializer(query_set, many = True)
#             return JsonResponse(serializer.data, safe = False)
#         else:
#             response_data = {"error_code" : error_code, "error_message": error_message, "data" : []}
#             return JsonResponse(response_data, status = 400)


# def ingredients(request):
#     if request.method == 'GET':
#         if not 'type' in request.GET:
#             base = BaseSerializer(Base.objects.all(),many=True)
#             sub = SubSerializer(Sub.objects.all(),many = True)
#             juice = JuiceSerializer(Juice.objects.all(), many= True)
#             other = OtherSerializer(Other.objects.all(), many= True)
#             serializer = IngredientsSerializer(data={'base':base.data,'sub': sub.data,'juice' : juice.data,'other' : other.data})
#             if serializer.is_valid():
#                 return JsonResponse(serializer.data, safe = 200)
#             else:
#                 return JsonResponse(serializer.data,status=200)
#         else:
#             type = request.GET['type']
#             if type == 'base':
#                 query_set = Base.objects.all()
#                 serializer = BaseSerializer(query_set,many = True)

#             if type == 'sub':
#                 query_set = Sub.objects.all()
#                 serializer = SubSerializer(query_set,many = True)

#             if type == 'juice':
#                 query_set = Juice.objects.all()
#                 serializer = JuiceSerializer(query_set,many = True)

#             if type == 'other':
#                 query_set = Other.objects.all()
#                 serializer = OtherSerializer(query_set,many = True)
            
#             return JsonResponse(serializer.data, safe = False)
        

# def reset(request):
#     if request.method == 'GET' or request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':
#         Cocktail.objects.all().delete()
#         Base.objects.all().delete()
#         Sub.objects.all().delete()
#         Juice.objects.all().delete()
#         Other.objects.all().delete()

#         return HttpResponse(status = 200)

# def todaydrink(request):
#     obj = TodayDrink.objects.all()
#     if obj.exists():
#         drink = obj.first().drink_name
#     else:
#         drink = Cocktail.objects.order_by("?").first()
#         newObj = obj.create(drink_name = drink)
#         newObj.save()
    
#     serializer = CocktailNameSerializer(drink)
#     ResponseData = {"error_code":200,"error_message":"", "data" : serializer.data}
#     return JsonResponse(ResponseData, status=200)
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import views, response, status
from .models import *
from .serializers import *

def check_cocktail_data(model,query_set): 
    # 데이터 유효성 검사 함수 (model = 검사할 데이터 모델, query_set = 검사할 데이터(딕셔너리형))
    for data in query_set:
        if not model.objects.filter(name = data['name']).exists():
            return False
    return True
    
def create_mapping_table(mapping_table_model,query_set,cocktail,ingredient_model): 
    '''
    칵테일-재료 연결 및 중간 테이블 제작 함수
    mapping_table_model = 중간 테이블 Model
    query_set = 재료 데이터 (딕셔너리 형태)
    cocktail = 칵테일 objcet
    ingredient_model = 재료 Model
    '''
    for data in query_set:
        name = ingredient_model.objects.get(name = data['name'])
        mapping_table_model.objects.create(cocktail = cocktail, name = name, amount = data['amount'])

@csrf_exempt
def cocktails(request):
    if request.method == 'GET': # 칵테일 레시피 전체 요청
        cocktails = Cocktail.objects.all()
        serializer = CocktailSerializer(cocktails, many=True)
        return JsonResponse(serializer.data,safe = False)

    elif request.method == 'POST': # 칵테일 레시피 등록
        data = JSONParser().parse(request)
        
        base_data = data.pop('base') #외래키 등록 필요한 항목들 파싱
        sub_data = data.pop('sub')
        juice_data = data.pop('juice')
        other_data = data.pop('other')
        glass_data = data.pop('glass')
        hashtag_data = data.pop('hashtag')

        serializer = CocktailSerializer(data = data) 
        
        # ---유효성 검사---
        if (serializer.is_valid()
        and Glass.objects.filter(name = glass_data).exists()
        and check_cocktail_data(Base,base_data)
        and check_cocktail_data(Sub,sub_data)
        and check_cocktail_data(Juice,juice_data)
        and check_cocktail_data(Other,other_data)):
            # --- 유효성 검사 통과 ---
            cocktail = serializer.save()
            
            glass = get_object_or_404(Glass, name = glass_data) #Glass 연결
            cocktail.glass = glass
            
            for hashtag in hashtag_data: #hashtag 연결
                cocktail.hashtag.add(hashtag)
            
            # --- 중간 테이블 연결 ---
            create_mapping_table(CocktailBase,base_data,cocktail,Base) 
            create_mapping_table(CocktailSub,sub_data,cocktail,Sub)
            create_mapping_table(CocktailJuice,juice_data,cocktail,Juice)
            create_mapping_table(CocktailOther,other_data,cocktail,Other)
            
            cocktail.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        
        error_data = {"error_code":400, "error_message":f"invalid data"}
        return JsonResponse(error_data,status = 400)
    
@csrf_exempt
def glasses(request): # 서빙 글라스 출력, 추가 함수
    if request.method == 'GET':
        glass = Glass.objects.all()
        serializer = GlassSerializer(glass, many=True)
        return JsonResponse(serializer.data,safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = GlassSerializer(data = data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status = 404)
    
@csrf_exempt
def glass(request,pk):
    if request.method == 'PUT':
        obj = get_object_or_404(Glass,name = pk)
        data = JSONParser().parse(request)
        if Glass.objects.filter(name = data['name']).exists():
            return JsonResponse({"error_code" : 404 , "error_message" : f"{data['name']} is already exists"})
        
        serializer = GlassSerializer(obj,data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status = 200)
        return JsonResponse(serializer.errors, status = 404)
    
    elif request.method == 'DELETE':
        glass = get_object_or_404(Glass,name = pk)
        glass.delete()
        data = {"response_data" : f"successfully delete {pk}"}
        return JsonResponse(data,status = 200)
        
@csrf_exempt
def bases(request):
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
            return JsonResponse(serializer.error, status = 400)
            
@csrf_exempt
def base(request,pk):
    if request.method == 'PUT':
        obj = get_object_or_404(Base,name = pk)
        data = JSONParser().parse(request)
        serializer = BaseSerializer(obj,data = data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status = 200)
        return JsonResponse(serializer.errors, status = 404)
    
    elif request.method == 'DELETE':
        obj = get_object_or_404(Base,name = pk)
        obj.delete()
        data = {"response_data" : f"successfully delete {pk}"}
        return JsonResponse(data,status = 200)
            
@csrf_exempt
def subs(request):
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
            return JsonResponse(serializer.error, status = 400)
            
@csrf_exempt
def sub(request,pk):
    if request.method == 'PUT':
        obj = get_object_or_404(Sub,name = pk)
        data = JSONParser().parse(request)
        serializer = BaseSerializer(obj,data = data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status = 200)
        return JsonResponse(serializer.errors, status = 404)
    
    elif request.method == 'DELETE':
        obj = get_object_or_404(Sub,name = pk)
        obj.delete()
        data = {"response_data" : f"successfully delete {pk}"}
        return JsonResponse(data,status = 200)

@csrf_exempt
def juices(request):
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
            return JsonResponse(serializer.error, status = 400) 
            
@csrf_exempt
def juice(request,pk):
    if request.method == 'DELETE':
        obj = get_object_or_404(Juice,name = pk)
        obj.delete()
        data = {"response_data" : f"successfully delete {pk}"}
        return JsonResponse(data,status = 200)
            
@csrf_exempt
def others(request):
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
            return JsonResponse(serializer.error, status = 400) 
            
@csrf_exempt
def other(request,pk):
    if request.method == 'DELETE':
        obj = get_object_or_404(Other,name = pk)
        obj.delete()
        data = {"response_data" : f"successfully delete {pk}"}
        return JsonResponse(data,status = 200)
            
@csrf_exempt
def cocktail(request,pk): # 특정 칵테일 수정, 삭제 함수
    if request.method == 'GET':
        obj = Cocktail.objects.get(name = pk)
        serializer = CocktailSerializer(obj)
        return JsonResponse(serializer.data, safe=False)
        
    elif request.method == 'PUT': 
        data = JSONParser().parse(request)
        
        base_data = data.pop('base') #외래키 등록 필요한 항목들 파싱
        sub_data = data.pop('sub')
        juice_data = data.pop('juice')
        other_data = data.pop('other')
        glass_data = data.pop('glass')
        
        cocktail = Cocktail.objects.get(name = pk)
        serializer = CocktailSerializer(cocktail,data = data)
        if serializer.is_valid() and Glass.objects.filter(name = glass_data).exists() and check_cocktail_data(Base,base_data) and check_cocktail_data(Sub,sub_data) and check_cocktail_data(Juice,juice_data) and check_cocktail_data(Other,other_data):
            serializer.save()
            # --------- 중간 테이블 업데이트 로직 짜야함 -------------
            # 1. 다른 부분만 검색해서 업데이트
            # 2. 전체 삭제 후 전체 생성 -> 결정.(mappng table 많아봐야 몇개 안될 듯)
            for obj in CocktailBase.objects.filter(cocktail = cocktail):
                obj.delete()
            for obj in CocktailSub.objects.filter(cocktail = cocktail):
                obj.delete()
            for obj in CocktailJuice.objects.filter(cocktail = cocktail):
                obj.delete()
            for obj in CocktailOther.objects.filter(cocktail = cocktail):
                obj.delete()
            
            glass = get_object_or_404(Glass, name = glass_data) #Glass 연결
            cocktail.glass = glass
            # --- 중간 테이블 연결 ---
            create_mapping_table(CocktailBase,base_data,cocktail,Base) 
            create_mapping_table(CocktailSub,sub_data,cocktail,Sub)
            create_mapping_table(CocktailJuice,juice_data,cocktail,Juice)
            create_mapping_table(CocktailOther,other_data,cocktail,Other)
            
            cocktail.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        
        error_data = {"error_code":400, "error_message":f"invalid data"}
        return JsonResponse(error_data, status = 400)

    elif request.method == 'DELETE': # 칵테일 삭제
        cocktail = get_object_or_404(Cocktail,name = pk) # 예외처리 필요
        for obj in CocktailBase.objects.filter(cocktail = cocktail):
            obj.delete()
        for obj in CocktailSub.objects.filter(cocktail = cocktail):
            obj.delete()
        for obj in CocktailJuice.objects.filter(cocktail = cocktail):
            obj.delete()
        for obj in CocktailOther.objects.filter(cocktail = cocktail):
            obj.delete()
        cocktail.delete()

def cocktail_names(request): # 칵테일 이름만 출력하는 함수
    if request.method == 'GET':
        query_set = Cocktail.objects.all()
        data = {"cocktails" : []}
        for cocktail in query_set:
            data["cocktails"].append(cocktail.name)
        return JsonResponse(data)

def ingredients(request): # 칵테일 재료 출력하는 함수
    if request.method == 'GET':
        data = {"base":[],"sub":[],"juice":[],"other":[]}
        
        base_query = Base.objects.all()
        for base in base_query:
            data['base'].append(base.name)
            
        sub_query = Sub.objects.all()
        for sub in sub_query:
            data['sub'].append(sub.name)
            
        juice_query = Juice.objects.all()
        for juice in juice_query:
            data['juice'].append(juice.name)
            
        other_query = Other.objects.all()
        for other in other_query:
            data['other'].append(other.name)
    
        return JsonResponse(data,status = 200)

@csrf_exempt
def search(request):
    '''
    칵테일 레시피 검색 함수
    request header로 검색 내용 주어짐
    and_query_set과 or_query_set 두 가지 쿼리셋 제작
    and_query_set 내용 없을때만 or_query_set 출력
    '''
    if request.method == 'GET':
        error_code = None
        and_query_set = Cocktail.objects.all()
        or_query_set = Cocktail.objects.none()
        
        if 'base' in request.GET: # --- Base 검색 ---
            base_data = list(request.GET['base'].split(','))
            cocktail_query_set = Cocktail.objects.prefetch_related('base').all()
            for name in base_data:
                query_set = cocktail_query_set.filter(base = name)
                and_query_set = and_query_set&query_set
                or_query_set = or_query_set.union(query_set)
    
        if 'sub' in request.GET: # --- Sub 검색 ---
            sub_data = list(request.GET['sub'].split(','))
            cocktail_query_set = Cocktail.objects.prefetch_related('sub').all()
            for name in sub_data:
                query_set = cocktail_query_set.filter(sub = name)
                and_query_set = and_query_set&query_set
                or_query_set = or_query_set.union(query_set)
                
        if 'juice' in request.GET: # --- Juice 검색 ---
            juice_data = list(request.GET['juice'].split(','))
            cocktail_query_set = Cocktail.objects.prefetch_related('juice').all()
            for name in juice_data:
                query_set = cocktail_query_set.filter(juice = name)
                and_query_set = and_query_set&query_set
                or_query_set = or_query_set.union(query_set)

        if 'other' in request.GET: # --- Other 검색 ---
            other_data = list(request.GET['other'].split(','))
            cocktail_query_set = Cocktail.objects.prefetch_related('other').all()
            for name in other_data:
                query_set = cocktail_query_set.filter(other = name)
                and_query_set = and_query_set&query_set
                or_query_set = or_query_set.union(query_set)

        if not and_query_set: # --------- 없는 쿼리 조합 구현 -----------
            error_code = 200
            error_message = "없는 조합입니다"
            serializer = CocktailNameSerializer(or_query_set,many = True)
            return JsonResponse({"error_code":error_code, "error_message": error_message, "data": serializer.data},safe = False)
        else:
            serializer = CocktailNameSerializer(and_query_set, many = True)
            return JsonResponse(serializer.data, safe = False)

# def reset(request):
#     if request.method == 'GET' or request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':
#         Cocktail.objects.all().delete()
#         Base.objects.all().delete()
#         Sub.objects.all().delete()
#         Juice.objects.all().delete()
#         Other.objects.all().delete()

#         return HttpResponse(status = 200)

def todaydrink(request): #오늘의 추천 칵테일 조회 함수
    obj = TodayDrink.objects.all()
    if obj.exists():
        today_drink = obj.first().cocktail
    else: # TodayDrink Object 존재 x 시 새로 생성
        today_drink = Cocktail.objects.order_by("?").first()
        new_obj = TodayDrink.objects.create(cocktail = today_drink)
        new_obj.save()
    
    serializer = CocktailNameSerializer(today_drink)
    ResponseData = {"error_code":200,"error_message":"", "data" : serializer.data}
    return JsonResponse(ResponseData, status=200)

@csrf_exempt
def hashtags(request):
    if request.method == 'GET':
        query_set = HashTag.objects.all()
        serializer = HashTagSerializer(query_set,many = True)
        return JsonResponse(serializer.data, safe = False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = HashTagSerializer(data = data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 200)
        else:
            return JsonResponse(serializer.errors, status = 400) 
        
@csrf_exempt
def hashtag(request,pk):
    if request.method == 'DELETE':
        obj = get_object_or_404(HashTag,name = pk)
        obj.delete()
        data = {"response_data" : f"successfully delete {pk}"}
        return JsonResponse(data,status = 200)
    
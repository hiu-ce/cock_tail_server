from rest_framework import serializers
from .models import  Base, Sub, Juice, Other, Cocktail
# from django.shortcuts import get_object_or_404

class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Base
        fields = ('drink_name',)

class SubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sub
        fields = ('drink_name',)

class JuiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Juice
        fields = ('drink_name',)

class OtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Other
        fields = ('name',)


class CocktailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cocktail
        fields = ('cocktail_name','base','sub','juice','other','recipe','img_url')

    def create(self, validated_data):
        base_names = list(validated_data['base'].keys())
        sub_names = list(validated_data['sub'].keys())
        juice_names = list(validated_data['juice'].keys())
        other_names= list(validated_data['other'].keys())

        cocktail = Cocktail.objects.create(**validated_data)
        
        for name in base_names:
            if Base.objects.filter(drink_name = name).exists() == False:
                obj = Base.objects.create(drink_name = name)
            else:
                obj = Base.objects.get(drink_name = name)

            obj.cocktails.add(cocktail)
            obj.save()

        for name in sub_names:
            if Sub.objects.filter(drink_name = name).exists() == False:
                obj = Sub.objects.create(drink_name = name)
            else:
                obj = Sub.objects.get(drink_name = name)

            obj.cocktails.add(cocktail)
            obj.save()

        for name in juice_names:
            if Juice.objects.filter(drink_name = name).exists() == False:
                obj = Juice.objects.create(drink_name = name)
            else:
                obj = Juice.objects.get(drink_name = name)

            obj.cocktails.add(cocktail)
            obj.save()

        for name in other_names:
            if Other.objects.filter(name = name).exists() == False:
                obj = Other.objects.create(name = name)
            else:
                obj = Other.objects.get(name = name)

            obj.cocktails.add(cocktail)
            obj.save()

        return cocktail
    
    def update(Self,instance, validated_data):
        if instance.base != validated_data['base']: #기존 데이터와 수정 데이터가 다를 때 - base 
            bases = Base.objects.all()
            for name in instance.base.keys(): #기존 base에서 cocktail 연결 해제
                obj = bases.get(drink_name = name)
                obj.cocktails.remove(instance)
                if not obj.cocktails.exists(): # 연결 모두 해제시 삭제
                    if not name in validated_data['base'].keys():
                        obj.delete()

            for new_name in validated_data['base'].keys(): # 새 데이터에 cocktail 연결
                if bases.filter(drink_name = new_name).exists():
                    obj = bases.get(drink_name = new_name)
                else:
                    obj = bases.create(drink_name = new_name)
                obj.cocktails.add(instance)

            instance.base = validated_data['base']

        if instance.sub != validated_data['sub']: #기존 데이터와 수정 데이터가 다를 때 - base 
            subs = Sub.objects.all()
            for name in instance.sub.keys(): #기존 base에서 cocktail 연결 해제
                obj = subs.get(drink_name = name)
                obj.cocktails.remove(instance)
                if not obj.cocktails.exists(): # 연결 모두 해제시 삭제
                    if not name in validated_data['sub'].keys():
                        obj.delete()

            for new_name in validated_data['sub'].keys(): # 새 데이터에 cocktail 연결
                if subs.filter(drink_name = new_name).exists():
                    obj = subs.get(drink_name = new_name)
                else:
                    obj = subs.create(drink_name = new_name)
                obj.cocktails.add(instance)

            instance.sub = validated_data['sub']

        if instance.juice != validated_data['juice']: #기존 데이터와 수정 데이터가 다를 때 - base
            juices = Juice.objects.all() 
            for name in instance.juice.keys(): #기존 base에서 cocktail 연결 해제
                obj = juices.get(drink_name = name)
                obj.cocktails.remove(instance)
                if not obj.cocktails.exists(): # 연결 모두 해제시 삭제
                    if not name in validated_data['juice'].keys():
                        obj.delete()

            for new_name in validated_data['juice'].keys(): # 새 데이터에 cocktail 연결
                if juices.filter(drink_name = new_name).exists():
                    obj = juices.get(drink_name = new_name)
                else:
                    obj = juices.create(drink_name = new_name)
                obj.cocktails.add(instance)

            instance.juice = validated_data['juice']

        if instance.other != validated_data['other']: #기존 데이터와 수정 데이터가 다를 때 - base 
            others = Other.objects.all()
            for name in instance.other.keys(): #기존 base에서 cocktail 연결 해제
                obj = others.get(name = name)
                obj.cocktails.remove(instance)
                if not obj.cocktails.exists(): # 연결 모두 해제시 삭제
                    if not name in validated_data['other'].keys():
                        obj.delete()

            for new_name in validated_data['other'].keys(): # 새 데이터에 cocktail 연결
                if others.filter(name = new_name).exists():
                    obj = others.get(name = new_name)
                else:
                    obj = others.create(name = new_name)
                obj.cocktails.add(instance)

            instance.other = validated_data['other']

        instance.recipe = validated_data['recipe']
        instance.img_url = validated_data['img_url']
        instance.save()
        return instance


class CocktailNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cocktail
        fields = ('cocktail_name',)

class IngredientsSerializer(serializers.Serializer):
    base = BaseSerializer(many=True)
    sub = SubSerializer(many=True)
    juice = JuiceSerializer(many=True)
    other = OtherSerializer(many=True)
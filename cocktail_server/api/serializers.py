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
        fields = ('cocktail_name','base','sub','juice','other','recipe')

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
        if instance.base != validated_data['base']: #?????? ???????????? ?????? ???????????? ?????? ??? - base 
            for name in instance.base.keys(): #?????? base?????? cocktail ?????? ??????
                obj = Base.objects.get(drink_name = name)
                obj.cocktails.remove(instance)
                if not obj.cocktails.exists(): # ?????? ?????? ????????? ??????
                    if not name in validated_data['base'].keys():
                        obj.delete()

            for new_name in validated_data['base'].keys(): # ??? ???????????? cocktail ??????
                if Base.objects.filter(drink_name = new_name).exists():
                    obj = Base.objects.get(drink_name = new_name)
                else:
                    obj = Base.objects.create(drink_name = new_name)
                obj.cocktails.add(instance)

            instance.base = validated_data['base']

        if instance.sub != validated_data['sub']: #?????? ???????????? ?????? ???????????? ?????? ??? - base 
            for name in instance.sub.keys(): #?????? base?????? cocktail ?????? ??????
                obj = Sub.objects.get(drink_name = name)
                obj.cocktails.remove(instance)
                if not obj.cocktails.exists(): # ?????? ?????? ????????? ??????
                    if not name in validated_data['sub'].keys():
                        obj.delete()

            for new_name in validated_data['sub'].keys(): # ??? ???????????? cocktail ??????
                if Sub.objects.filter(drink_name = new_name).exists():
                    obj = Sub.objects.get(drink_name = new_name)
                else:
                    obj = Sub.objects.create(drink_name = new_name)
                obj.cocktails.add(instance)

            instance.sub = validated_data['sub']

        if instance.juice != validated_data['juice']: #?????? ???????????? ?????? ???????????? ?????? ??? - base 
            for name in instance.juice.keys(): #?????? base?????? cocktail ?????? ??????
                obj = Juice.objects.get(drink_name = name)
                obj.cocktails.remove(instance)
                if not obj.cocktails.exists(): # ?????? ?????? ????????? ??????
                    if not name in validated_data['juice'].keys():
                        obj.delete()

            for new_name in validated_data['juice'].keys(): # ??? ???????????? cocktail ??????
                if Juice.objects.filter(drink_name = new_name).exists():
                    obj = Juice.objects.get(drink_name = new_name)
                else:
                    obj = Juice.objects.create(drink_name = new_name)
                obj.cocktails.add(instance)

            instance.juice = validated_data['juice']

        if instance.other != validated_data['other']: #?????? ???????????? ?????? ???????????? ?????? ??? - base 
            for name in instance.other.keys(): #?????? base?????? cocktail ?????? ??????
                obj = Other.objects.get(name = name)
                obj.cocktails.remove(instance)
                if not obj.cocktails.exists(): # ?????? ?????? ????????? ??????
                    if not name in validated_data['other'].keys():
                        obj.delete()

            for new_name in validated_data['other'].keys(): # ??? ???????????? cocktail ??????
                if Other.objects.filter(name = new_name).exists():
                    obj = Other.objects.get(name = new_name)
                else:
                    obj = Other.objects.create(name = new_name)
                obj.cocktails.add(instance)

            instance.other = validated_data['other']

        instance.recipe = validated_data['recipe']
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
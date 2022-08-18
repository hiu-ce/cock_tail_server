from .models import Cocktail,TodayDrink

def todaydrink():
    querySet = TodayDrink.objects.all()
    todayDrink = Cocktail.objects.order_by("?").first()

    if querySet.exists():
        obj_id = querySet.first().id
        obj = querySet.get(id=obj_id)
        obj.drink_name = todayDrink
        obj.save()
    else:
        newObj = querySet.create(drink_name = todayDrink)
        newObj.save()

    
from .models import Cocktail,TodayDrink

def todaydrink():
    obj = TodayDrink.objects.all()
    todayDrink = Cocktail.objects.order_by("?").first()

    if obj.exists():
        obj.first().drink_name = todayDrink
        # obj.get(id=2).drink_name = todayDrink
        obj.first().save()
    else:
        newObj = obj.create(drink_name = todayDrink)
        newObj.save()

    
from .models import Cocktail,TodayDrink

def todaydrink():
    obj = TodayDrink.objects.get(id=1)
    obj.drink_name = Cocktail.objects.order_by("?").first()
    obj.save()
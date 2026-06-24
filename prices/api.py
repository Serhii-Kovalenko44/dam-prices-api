from ninja import NinjaAPI
from django.db.models import Avg, Max, Min
from datetime import date
from .models import DamPrice
from .schemas import DamPriceOut, PriceStatsOut

api = NinjaAPI()

@api.get('/prices/', response=list[DamPriceOut])
def get_prices(request, start_date: date=None, end_date: date=None):
    queryset = DamPrice.objects.all()
    if start_date:
        queryset = queryset.filter(date__gte=start_date)
    if end_date:
        queryset = queryset.filter(date__lte=end_date)
    if not start_date and not end_date:
        queryset = queryset.order_by('-date', 'hour')[:72]
    else:
        queryset = queryset.order_by('date', 'hour')
    return queryset

@api.get('/prices/stats/', response=PriceStatsOut)
def get_price_stats(request, start_date: date, end_date: date):
    stats = DamPrice.objects.filter(date__range=[start_date, end_date]).aggregate(
        min_p = Min('price'),
        max_p = Max('price'),
        avg_p = Avg('price')
    )

    total_records = DamPrice.objects.filter(date__range=[start_date, end_date]).count()
    avg_stats = round(stats['avg_p'], 2) if stats['avg_p'] else None
    return {
        'start_date': start_date,
        'end_date': end_date,
        'min_price': stats['min_p'],
        'max_price': stats['max_p'],
        'avg_price': avg_stats,
        'total_records': total_records
    }

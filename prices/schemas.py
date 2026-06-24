from ninja import Schema
from datetime import date
from decimal import Decimal

class DamPriceOut(Schema):
    date: date
    hour: int
    price: Decimal
    sales_volume: Decimal
    purchase_volume: Decimal
    declared_sales_volume: Decimal
    declared_purchase_volume: Decimal

class PriceStatsOut(Schema):
    start_date: date
    end_date: date
    min_price: Decimal = None
    max_price: Decimal = None
    avg_price: Decimal = None
    total_records: int

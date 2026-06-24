from django.db import models

class DamPrice(models.Model):
    date = models.DateField()
    hour = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Price, UAH/MWh'
    )
    sales_volume = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        verbose_name='Sales volume, MW.h'
    )
    purchase_volume = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        verbose_name='Purchase volume, MW.h'
    )
    declared_sales_volume = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        verbose_name='Declared sales volume, MW.h'
    )
    declared_purchase_volume = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        verbose_name='Declared purchase volume, MW.h'
    )
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'DAM Market Data'
        verbose_name_plural = 'DAM Market Data'
        unique_together = ('date', 'hour')
        ordering = ['-date', 'hour']

    def __str__(self):
        return f'{self.date} {self.hour}:00 Price: {self.price} UAH'

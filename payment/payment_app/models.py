from django.db import models


class Item(models.Model):
    name: str = models.CharField(max_length=60)
    description: str = models.CharField(max_length=3000)
    price: int = models.IntegerField()

    def __str__(self):
        return self.name

    def get_display_price(self):
        return f'{self.price / 100:.2f}'

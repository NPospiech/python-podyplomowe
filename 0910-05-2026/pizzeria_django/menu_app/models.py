from django.db import models
from django.core.exceptions import ValidationError

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.FloatField()
    published_year = models.IntegerField(default=2024)

    def __str__(self):
        return f"{self.title} ({self.author})"



class Pizza(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.FloatField()

    def clean(self):
        """Walidacja domenowa."""
        if self.price is not None and self.price <= 0:
            raise ValidationError({'price': f'Nieprawidlowa cena: {self.price} (musi byc > 0)'})
        if not self.name:
            raise ValidationError({'name': 'Nazwa pizzy nie moze byc pusta!'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}: {self.price} zl"

    class Meta:
        ordering = ['name']


from django.db import models

class Car(models.Model):
    CAR_TYPES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Truck', 'Truck'),
        ('Van', 'Van'),
        ('Coupe', 'Coupe'),
    ]

    name = models.CharField(max_length=100)
    car_type = models.CharField(max_length=50, choices=CAR_TYPES)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)

    def __str__(self):
        return self.name

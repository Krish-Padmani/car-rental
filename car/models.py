from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    CAR_TYPES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Sport', 'Sport'),]
        

    name = models.CharField(max_length=100)
    car_type = models.CharField(max_length=50, choices=CAR_TYPES)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, default='Booked')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car.name} booked by {self.user.username} from {self.start_date} to {self.end_date}"

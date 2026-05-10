from django.db import models
from django.contrib.auth.models import User

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.IntegerField(default=1)
    budget = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    cost_estimate = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    # 10 Unsplash photos store karne ke liye
    image_list = models.JSONField(default=list) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.destination} Trip"

class Itinerary(models.Model):
    trip = models.ForeignKey(Trip, related_name='days', on_delete=models.CASCADE)
    day_number = models.IntegerField()
    activity_title = models.CharField(max_length=200)
    location_address = models.CharField(max_length=500)
    time_slot = models.CharField(max_length=100)
    # models.py mein 'Itinerary' class ke andar aise change karein
    cost_estimate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, default='Pending') # Pending or Completed
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['day_number']
from django.db import models
from django.utils import timezone


class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    max_capacity = models.IntegerField(
        default=10, help_text="Maximum number of participants allowed"
    )

    def __str__(self):
        return f"{self.name} (Max: {self.max_capacity})"


class Instructor(models.Model):
    name = models.CharField(max_length=100)
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    available_from = models.TimeField()
    available_to = models.TimeField()
    repeat_days = models.JSONField(default=list)

    def __str__(self):
        return f"{self.name} ({self.fitness_class.name})"


class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    class_booking_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.client_name} - {self.fitness_class.name} - {self.class_booking_at.strftime('%Y-%m-%d %H:%M')}"

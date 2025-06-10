from django.contrib import admin
from .models import FitnessClass, Instructor, Booking

admin.site.register(FitnessClass)
admin.site.register(Instructor)
admin.site.register(Booking)

# Register your models here.

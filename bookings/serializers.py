from rest_framework import serializers
from .models import FitnessClass, Instructor, Booking


class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = ["id", "name", "max_capacity"]


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = [
            "id",
            "name",
            "fitness_class",
            "available_from",
            "available_to",
            "repeat_days",
        ]


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = [
            "id",
            "fitness_class",
            "instructor",
            "client_name",
            "client_email",
            "class_booking_at",
        ]

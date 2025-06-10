from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from datetime import datetime, timedelta
from .models import FitnessClass, Instructor, Booking
from .serializers import BookingSerializer, FitnessClassSerializer, InstructorSerializer
from datetime import datetime, timedelta
from .models import Booking
import pytz
from datetime import datetime, time


def convert_slots_to_user_timezone(slot_times, user_tz_str):
    user_tz = pytz.timezone(user_tz_str)
    ist = pytz.timezone("Asia/Kolkata")

    converted_slots = []
    for slot in slot_times:
        ist_datetime = ist.localize(
            datetime.combine(datetime.today(), time.fromisoformat(slot))
        )
        user_time = ist_datetime.astimezone(user_tz)
        converted_slots.append(user_time.strftime("%I:%M %p"))

    return converted_slots


def generate_time_slots(start_time, end_time, day_date):
    current_time = datetime.combine(day_date, start_time)
    end_datetime = datetime.combine(day_date, end_time)
    slot_times = []

    while current_time < end_datetime:
        slot_times.append(current_time.strftime("%H:%M"))
        current_time += timedelta(hours=1)

    return slot_times


def get_slot_booking_count(instructor, fitness_class, day_date):
    bookings = Booking.objects.filter(
        instructor=instructor,
        fitness_class=fitness_class,
        class_booking_at__date=day_date,
    ).values_list("class_booking_at", flat=True)
    slot_counts = {}
    for dt in bookings:
        slot = dt.strftime("%H:%M")
        slot_counts[slot] = slot_counts.get(slot, 0) + 1
    return slot_counts


def check_availability(data, user_tz="Asia/Kolkata"):
    today = datetime.today().date()
    slot_data = {}
    instructor = data["instructor"]
    fitness_class = data["fitness_class"]
    max_capacity = fitness_class.max_capacity
    class_booked = data.get("class_booking_at")
    for i in range(7):
        day_date = today + timedelta(days=i)
        weekday = day_date.strftime("%A")

        if weekday in instructor.repeat_days:
            all_slots = generate_time_slots(
                instructor.available_from, instructor.available_to, day_date
            )
            slot_booking_counts = get_slot_booking_count(
                instructor, fitness_class, day_date
            )
            # Dictionary of slot -> left_slots
            slot_info = {
                slot: max_capacity - slot_booking_counts.get(slot, 0)
                for slot in all_slots
                if slot_booking_counts.get(slot, 0) < max_capacity
            }

            if slot_info:
                converted = convert_slots_to_user_timezone(
                    list(slot_info.keys()), user_tz
                )
                slot_data[day_date.strftime("%d-%m-%Y")] = [
                    {
                        "class_time": converted[i],
                        "left_slots": list(slot_info.values())[i],
                    }
                    for i in range(len(converted))
                ]

    if class_booked:
        booking_day = class_booked.strftime("%d-%m-%Y")
        booking_time = class_booked.strftime("%I:%M %p")

        available_slots_today = slot_data.get(booking_day, [])
        is_available = any(
            slot["class_time"] == booking_time for slot in available_slots_today
        )

        return is_available, slot_data

    return slot_data


class ClassListView(APIView):
    def get(self, request):
        data = {}
        today = datetime.today().strftime("%A")
        classes = FitnessClass.objects.all()
        user_tz = request.GET.get("tz", "Asia/Kolkata")

        for fitness_class in classes:
            instructors = Instructor.objects.filter(fitness_class=fitness_class)
            instructor_data = []

            for instructor in instructors:
                
                slots = []
                current_time = datetime.combine(
                    datetime.today(), instructor.available_from
                )
                end_time = datetime.combine(
                    datetime.today(), instructor.available_to
                )

                while current_time < end_time:
                    slots.append(current_time.strftime("%I:%M %p"))
                    current_time += timedelta(hours=1)

                instructor_data.append(
                    {
                        "Instructor": instructor.name,
                        "Available Slots Next 7 days": check_availability(
                            {
                                "instructor": instructor,
                                "fitness_class": fitness_class,
                                "class_booking_at": None,
                            },
                            user_tz,
                        ),
                    }
                )

            data[fitness_class.name] = instructor_data

        return Response(data)


class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user_tz = request.GET.get("tz", "Asia/Kolkata")
        if serializer.is_valid():
            instructor = serializer.validated_data.get("instructor")
            fitness_class = serializer.validated_data.get("fitness_class")
            if instructor.fitness_class != fitness_class:
                return Response(
                    {"error": f"Selected instructor does not conduct this fitness '{fitness_class.name}' class."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            is_available, available_slots = check_availability(
                serializer.validated_data, user_tz=user_tz
            )

            if not is_available:
                return Response(
                    {
                        "error": "Selected time slot is not available for this instructor.",
                        "available slots for next 7 days": available_slots,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            return Response("class booked successfully", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingListView(APIView):
    def get(self, request):
        email = request.query_params.get("email")
        if email:
            bookings = Booking.objects.filter(client_email=email)
        else:
            bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


class FitnessClassCreateView(generics.CreateAPIView):
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Fitness class created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class InstructorListView(APIView):
    def get(self, request):
        instructors = Instructor.objects.all()
        serializer = InstructorSerializer(instructors, many=True)
        return Response(serializer.data)

class InstructorCreateView(generics.CreateAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Instructor created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

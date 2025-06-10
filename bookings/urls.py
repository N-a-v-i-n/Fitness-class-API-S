from django.urls import path
from .views import (
    ClassListView,
    BookingCreateView,
    BookingListView,
    FitnessClassCreateView,
    InstructorCreateView,
    InstructorListView
)

urlpatterns = [
    path('classes/', ClassListView.as_view(), name='class-list'),
    path('classes/create/', FitnessClassCreateView.as_view(), name='class-create'),
    path('instructors/', InstructorListView.as_view(), name='instructor-list'),
    path('instructors/create/', InstructorCreateView.as_view(), name='instructor-create'),
    path('book/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/', BookingListView.as_view(), name='booking-list'),
]

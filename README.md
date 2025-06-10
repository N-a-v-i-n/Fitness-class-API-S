Fitness Class Booking API
-------------------------------
Build a simple Booking API for a fictional fitness studio using Python. The goal is to evaluate your coding skills, design thinking, and understanding of backend development principles.

#Features
View all available fitness classes and their instructors

Book classes with timezone-aware slots

Track your booking history

Manage class capacity dynamically

Handle instructor availability efficiently

Generate available date & time slots for the next 7 days

# Tech Stack
Python 3.x

Django 4.x

Django REST Framework

SQLite (default, can be replaced with any supported DB)

pytz (for timezone support)

# Setup Instructions
# 1. Clone the repository
git clone https://github.com/your-username/fitness-booking-api.git

# 2. Navigate into the project directory
cd fitness-booking-api

# 3. Create and activate a virtual environment
python -m venv env
env\Scripts\activate       # On Windows
source env/bin/activate    # On macOS/Linux

# 4. Install dependencies
pip install -r requirements.txt

# 5. Apply migrations
python manage.py migrate

# 6. Start the development server
python manage.py runserver



Sample cURL Requests
-----------------------------

1. Create a Fitness Class

curl --location 'http://127.0.0.1:8000/api/classes/create/' \
--header 'Cookie: csrftoken=6ots3a9jlejiicICNfUh4qNKwxqNNHBl2Dd4CRrhBrsBBDQ1TGyLlNdqO0GHPExq' \
--form 'name="zumba"' \
--form 'max_capacity="3"'

3. Create an Instructor

curl --location 'http://localhost:8000/api/instructors/create/' \
--header 'Content-Type: application/json' \
--data '{
    "name": "amit",
    "fitness_class": 1,
    "available_from": "05:00",
    "available_to": "08:00",
    "repeat_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
}'

4. List All Classes & Instructors

curl --location 'http://127.0.0.1:8000/api/classes/?tz=Asia%2FKolkata'

5. Book a Class

curl --location 'http://localhost:8000/api/book/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "fitness_class": 1,
    "instructor": 1,
    "client_name": "John1",
    "client_email": "john1@gmail.com",
    "class_booking_at": "2025-06-10T06:00:00"
}'

6. Get All Bookings (Optional Email Filter)

curl --location 'http://localhost:8000/api/bookings/?email=john%40gmail.com' \
--header 'Content-Type: application/json' \
--data ''

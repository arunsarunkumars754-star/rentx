import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vehicle_rental.settings')
django.setup()

from django.contrib.auth.models import User

from rental.models import (
    CUSTOMERS, VEHICLES, VEHICLE_CATEGORY, 
    BOOKING, RENTAL, PAYMENT, CANCELLATION, REPORT
)

print("Clearing old data...")
CANCELLATION.objects.all().delete()
PAYMENT.objects.all().delete()
RENTAL.objects.all().delete()
BOOKING.objects.all().delete()
VEHICLE_CATEGORY.objects.all().delete()
VEHICLES.objects.all().delete()
CUSTOMERS.objects.all().delete()
REPORT.objects.all().delete()

# Create superuser / admin user if not exists
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser('admin', 'admin@rentx.com', 'admin123')
    print("Created superuser 'admin' with password 'admin123'")

print("Seeding Customers & Users...")
customers_data = [
    ("Arun", "arun@gmail.com", "9811043210", "DL-01-2022-00123", "Indiranagar, Bengaluru"),
    ("Kiran", "kiran@gmail.com", "9898712345", "KA-04-2021-99887", "Koramangala, Bengaluru"),
    ("Rahul", "rahul@gmail.com", "9098776655", "KA-01-2023-45678", "Whitefield, Bengaluru"),
    ("Priya", "priya@gmail.com", "8765432109", "MH-02-2020-11223", "HSR Layout, Bengaluru"),
    ("Sneha", "sneha@gmail.com", "7654321098", "DL-03-2022-77889", "Jayanagar, Bengaluru"),
    ("Fleet Admin", "admin@rentx.com", "9000000000", "SYS-FLEET-01", "RENTX Central HQ, Bengaluru"),
]

customers_dict = {}
for name, email, phone, license_no, address in customers_data:
    cust = CUSTOMERS.objects.create(
        Name=name,
        Email=email,
        Phone=phone,
        License_No=license_no,
        Address=address
    )
    customers_dict[name] = cust
    
    # Also create matching Django User for login
    username = email.split('@')[0]
    if not User.objects.filter(username=username).exists():
        u = User.objects.create_user(username=username, email=email, password='password123', first_name=name)

fleet_owner = customers_dict["Fleet Admin"]

print("Seeding Vehicles...")
vehicles_specs = [
    # (Model, Plate, Rate, Fuel, Color, Status, Image, Seats, Trans, Year, Rating, Category, Description)
    ("Honda City", "KA-01-HC-1800", 1800.00, "Petrol", "White", "Available", "/static/images/vehicles/honda_city.jpg", 5, "Automatic", 2025, 4.8, "Cars", "The Honda City offers a perfect blend of style, comfort and performance. Ideal for both city and highway drives."),
    ("Hyundai Creta", "KA-03-CR-2200", 2200.00, "Diesel", "Phantom Black", "Rented", "/static/images/vehicles/creta.jpg", 5, "Automatic", 2024, 4.7, "SUVs", "Dynamic SUV with commanding road presence, panoramic sunroof and premium audio system."),
    ("Royal Enfield", "KA-05-RE-0900", 900.00, "Petrol", "Chrome Bronze", "Available", "/static/images/vehicles/royal_enfield.jpg", 2, "Manual", 2024, 4.9, "Bikes", "Iconic cruiser with timeless styling, throaty exhaust note and unmatched road presence."),
    ("Swift", "KA-02-SW-1500", 1500.00, "Petrol", "Pearl Red", "Available", "/static/images/vehicles/swift.jpg", 5, "Manual", 2024, 4.6, "Cars", "Zippy, efficient, and effortless to park. Perfect for navigating city traffic with great fuel economy."),
    ("Innova", "KA-04-IN-2500", 2500.00, "Diesel", "Silver Metallic", "Maintenance", "/static/images/vehicles/innova.jpg", 7, "Automatic", 2023, 4.8, "Vans", "Supreme comfort for family and executive travels with plush captain seats and expansive luggage space."),
    ("Fortuner", "KA-01-FT-3500", 3500.00, "Diesel", "Super White", "Available", "/static/images/vehicles/fortuner.jpg", 7, "Automatic", 2025, 4.9, "SUVs", "Formidable 4x4 SUV built to conquer any terrain with unmatched power and luxurious leather cabin."),
    ("Mahindra Thar", "KA-04-TH-2800", 2800.00, "Diesel", "Mystic Copper", "Available", "/static/images/vehicles/thar.jpg", 4, "Automatic", 2024, 4.8, "SUVs", "Legendary off-roader with convertible top and rugged capability for weekend adventures."),
    ("Tata Nexon EV", "KA-03-NX-2000", 2000.00, "Electric", "Teal Blue", "Available", "/static/images/vehicles/sedan.jpg", 5, "Automatic", 2025, 4.7, "Cars", "Eco-friendly, fast acceleration with 400km range and cutting-edge tech connectivity."),
    ("KTM Duke 390", "KA-02-KT-1100", 1100.00, "Petrol", "Electric Orange", "Available", "/static/images/vehicles/royal_enfield.jpg", 2, "Manual", 2024, 4.9, "Bikes", "High-performance naked streetfighter with razor sharp cornering dynamics."),
]

vehicles_dict = {}
for model, plate, rate, fuel, color, status, img, seats, trans, year, rating, cat, desc in vehicles_specs:
    v = VEHICLES.objects.create(
        Plate_no=plate,
        Model=model,
        Rental_rate=rate,
        fuel_type=fuel,
        color=color,
        status=status,
        image=img,
        seats=seats,
        transmission=trans,
        year=year,
        rating=rating,
        customer=fleet_owner
    )
    VEHICLE_CATEGORY.objects.create(
        vehicle=v,
        category_name=cat,
        description=desc
    )
    vehicles_dict[model] = v

print("Seeding Reports...")
reports_info = [
    ("Booking Report", "Monthly booking trends, frequency of rentals, and vehicle popularity.", date(2026, 9, 25)),
    ("Revenue Report", "Total revenue, gross transaction value, and payment channel distribution.", date(2026, 9, 25)),
    ("Vehicle Usage Report", "Vehicle mileage tracking, fleet maintenance schedules, and utilization percentage.", date(2026, 9, 25)),
    ("Customer Report", "Customer registration rate, loyalty metrics, and KYC verification records.", date(2026, 9, 25)),
    ("Cancellation Report", "Cancellation frequency, customer feedback on cancellations, and refund processing.", date(2026, 9, 25)),
]

created_reports = []
for r_type, desc, r_date in reports_info:
    rep = REPORT.objects.create(report_type=r_type, description=desc, report_date=r_date)
    created_reports.append(rep)

print("Seeding Bookings & Rentals & Payments...")
bookings_info = [
    ("Arun", "Honda City", date(2026, 9, 27), date(2026, 9, 28), date(2026, 9, 30), 2, 3600.00, "Confirmed", "Bengaluru", "UPI", "Paid", 4248.00),
    ("Kiran", "Hyundai Creta", date(2026, 9, 27), date(2026, 9, 29), date(2026, 10, 2), 3, 4400.00, "Pending", "Bengaluru", "Card", "Pending", 4400.00),
    ("Rahul", "Swift", date(2026, 9, 26), date(2026, 9, 30), date(2026, 10, 3), 3, 3200.00, "Completed", "Bengaluru", "UPI", "Paid", 3200.00),
    ("Priya", "Innova", date(2026, 9, 26), date(2026, 10, 1), date(2026, 10, 4), 3, 7500.00, "Confirmed", "Bengaluru", "Card", "Paid", 7500.00),
    ("Sneha", "Fortuner", date(2026, 9, 27), date(2026, 10, 2), date(2026, 10, 5), 3, 7000.00, "Pending", "Bengaluru", "Net Banking", "Pending", 7000.00),
]

for cust_name, veh_name, b_date, s_date, e_date, days, amount, status, loc, p_method, p_status, p_amt in bookings_info:
    b = BOOKING.objects.create(
        customer=customers_dict[cust_name],
        vehicle=vehicles_dict[veh_name],
        booking_date=b_date,
        start_date=s_date,
        end_date=e_date,
        no_of_days=days,
        total_amount=amount,
        status=status
    )
    rent = RENTAL.objects.create(
        booking=b,
        pickup_location=loc,
        return_location=loc,
        pickup_date=s_date,
        return_date=e_date
    )
    PAYMENT.objects.create(
        rental=rent,
        payment_date=b_date,
        payment_status=p_status,
        payment_method=p_method,
        amount=p_amt,
        report=created_reports[1]
    )

print("Seeding Cancellations...")
cancellations_info = [
    ("Arun", "Change in plans", date(2026, 9, 27), date(2026, 9, 29)),
    ("Kiran", "Personal work", date(2026, 9, 30), date(2026, 10, 2)),
    ("Rahul", "Weather issue", date(2026, 10, 1), date(2026, 10, 3)),
    ("Priya", "Medical reason", date(2026, 10, 5), date(2026, 10, 7)),
    ("Sneha", "Other", date(2026, 10, 6), date(2026, 10, 8)),
]

all_rentals = list(RENTAL.objects.all())
for idx, (c_name, reason, c_date, ref_date) in enumerate(cancellations_info):
    if idx < len(all_rentals):
        CANCELLATION.objects.create(
            rental=all_rentals[idx],
            cancel_date=c_date,
            reason=reason,
            refund_date=ref_date
        )

print("RENTX database fully migrated and seeded with persistent fields!")

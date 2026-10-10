import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vehicle_rental.settings')
django.setup()

from rental.models import VEHICLES, VEHICLE_CATEGORY, CUSTOMERS

# Create a dummy customer since VEHICLES requires a customer
owner, _ = CUSTOMERS.objects.get_or_create(
    Name='Company Fleet',
    Address='123 Main St',
    Email='fleet@vrms.com',
    Phone='555-0000',
    License_No='SYS-001'
)

# Create vehicles
vehicles_data = [
    ('Toyota RAV4', 'RAV-4041', 55.00, 'Hybrid', 'Silver', 'SUV', 'Sport Utility Vehicle'),
    ('Ford Explorer', 'EXP-2938', 75.00, 'Gasoline', 'Black', 'SUV', 'Sport Utility Vehicle'),
    ('Honda Civic', 'CIV-9921', 40.00, 'Gasoline', 'Blue', 'Sedan', 'Comfortable and fuel efficient'),
    ('Toyota Camry', 'CAM-8832', 45.00, 'Hybrid', 'White', 'Sedan', 'Comfortable and fuel efficient'),
    ('Mercedes-Benz S-Class', 'MER-1111', 150.00, 'Gasoline', 'Black', 'Luxury', 'Premium cars for special occasions'),
    ('BMW 7 Series', 'BMW-2222', 140.00, 'Gasoline', 'White', 'Luxury', 'Premium cars for special occasions'),
    ('Nissan Versa', 'VER-4455', 30.00, 'Gasoline', 'Red', 'Economy', 'Budget friendly compact cars'),
    ('Hyundai Accent', 'ACC-3344', 32.00, 'Gasoline', 'Grey', 'Economy', 'Budget friendly compact cars'),
    ('Maruti Suzuki Swift', 'MAR-1234', 25.00, 'Gasoline', 'Red', 'Economy', 'Budget friendly compact cars'),
]

for model, plate, rate, fuel, color, cat_name, cat_desc in vehicles_data:
    vehicle, created = VEHICLES.objects.update_or_create(
        Plate_no=plate,
        defaults={
            'Model': model,
            'Rental_rate': rate,
            'fuel_type': fuel,
            'color': color,
            'customer': owner
        }
    )
    # The current schema has VEHICLE_CATEGORY holding a ForeignKey to VEHICLES
    VEHICLE_CATEGORY.objects.update_or_create(
        vehicle=vehicle,
        category_name=cat_name,
        defaults={
            'description': cat_desc
        }
    )

print("Database seeded with realistic vehicles using the new schema!")

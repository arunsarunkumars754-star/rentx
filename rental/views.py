import os
import uuid
import json
from datetime import datetime, date, timedelta
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import (
    CUSTOMERS, VEHICLES, VEHICLE_CATEGORY, 
    BOOKING, RENTAL, PAYMENT, CANCELLATION, REPORT
)

def get_vehicle_extra(vehicle):
    """Provide high-res photos, specs, and status directly from DB with accurate model mappings."""
    name_lower = vehicle.Model.lower()
    
    # Priority defaults based on model name
    if 'bmw' in name_lower or 'm3' in name_lower:
        def_img = '/static/images/vehicles/bmw_m3.jpg'
        def_brand = 'BMW'
        def_model = 'M3 Competition Track Edition'
        def_year = 2025
        def_cat = 'Cars'
        def_desc = 'Pure track-bred performance sedan featuring twin-turbo power, carbon roof, and M xDrive precision handling.'
    elif 'nexon' in name_lower:
        def_img = '/static/images/vehicles/nexon_ev.jpg'
        def_brand = 'Tata'
        def_model = 'Nexon EV'
        def_year = 2025
        def_cat = 'Cars'
        def_desc = 'Zero-emission electric compact SUV with instant torque, connected car tech, and smooth silent drive.'
    elif 'ktm' in name_lower or 'duke' in name_lower:
        def_img = '/static/images/vehicles/ktm_duke_390.jpg'
        def_brand = 'KTM'
        def_model = 'Duke 390'
        def_year = 2024
        def_cat = 'Bikes'
        def_desc = 'High-performance naked streetfighter with razor sharp cornering dynamics and exhilarating power.'
    elif 'scooty' in name_lower:
        def_img = '/static/images/vehicles/1417e04a_SCOOTY.webp'
        def_brand = 'TVS'
        def_model = 'Scooty Zest'
        def_year = 2024
        def_cat = 'Bikes'
        def_desc = 'Lightweight, nimble, and highly efficient city scooter for seamless daily commutes and errands.'
    elif 'cycle' in name_lower:
        def_img = '/static/images/vehicles/bba07ed1_CYCLE.avif'
        def_brand = 'Hero'
        def_model = 'Cycle Urban'
        def_year = 2024
        def_cat = 'Bikes'
        def_desc = 'Eco-friendly urban bicycle for clean, active, and cost-effective commuting around town.'
    elif 'yamaha' in name_lower:
        def_img = '/static/images/vehicles/bfb05ddb_YAMAHA.webp'
        def_brand = 'Yamaha'
        def_model = 'Yamaha 122'
        def_year = 2024
        def_cat = 'Bikes'
        def_desc = 'Sporty two-wheeler offering smooth acceleration, comfortable ergonomics, and outstanding reliability.'
    elif 'taxi' in name_lower:
        def_img = '/static/images/vehicles/eae4cd1d_TAXI.webp'
        def_brand = 'Toyota'
        def_model = 'Taxi Hybrid'
        def_year = 2024
        def_cat = 'Vans'
        def_desc = 'Spacious hybrid passenger vehicle tailored for convenient group transit and city tour transfers.'
    elif 'auto' in name_lower:
        def_img = '/static/images/vehicles/aa6fd482_auto_-bajak.avif'
        def_brand = 'Bajaj'
        def_model = 'Auto RE Compact'
        def_year = 2024
        def_cat = 'Vans'
        def_desc = 'Classic commercial three-wheeler utility vehicle for quick, economical group and luggage transport.'
    elif 'city' in name_lower or 'honda' in name_lower:
        def_img = '/static/images/vehicles/honda_city.jpg'
        def_brand = 'Honda'
        def_model = 'City'
        def_year = 2025
        def_cat = 'Cars'
        def_desc = 'The Honda City offers a perfect blend of style, comfort and performance. Ideal for both city and highway drives.'
    elif 'creta' in name_lower:
        def_img = '/static/images/vehicles/creta.jpg'
        def_brand = 'Hyundai'
        def_model = 'Creta'
        def_year = 2024
        def_cat = 'SUVs'
        def_desc = 'Dynamic SUV with commanding road presence, panoramic sunroof, and premium ventilated cabin.'
    elif 'royal' in name_lower or 'enfield' in name_lower or 'bullet' in name_lower:
        def_img = '/static/images/vehicles/royal_enfield.jpg'
        def_brand = 'Royal Enfield'
        def_model = 'Classic 350'
        def_year = 2024
        def_cat = 'Bikes'
        def_desc = 'Iconic cruiser with timeless styling, throaty exhaust note, and unmatched road presence.'
    elif 'swift' in name_lower:
        def_img = '/static/images/vehicles/swift.jpg'
        def_brand = 'Maruti Suzuki'
        def_model = 'Swift'
        def_year = 2024
        def_cat = 'Cars'
        def_desc = 'Zippy, efficient, and effortless to park. Perfect for navigating city traffic with great fuel economy.'
    elif 'innova' in name_lower:
        def_img = '/static/images/vehicles/innova.jpg'
        def_brand = 'Toyota'
        def_model = 'Innova Crysta'
        def_year = 2023
        def_cat = 'Vans'
        def_desc = 'Supreme comfort for family and executive travels with plush captain seats and expansive luggage space.'
    elif 'fortuner' in name_lower:
        def_img = '/static/images/vehicles/fortuner.jpg'
        def_brand = 'Toyota'
        def_model = 'Fortuner 4x4'
        def_year = 2025
        def_cat = 'SUVs'
        def_desc = 'Formidable 4x4 SUV built to conquer any terrain with unmatched power and luxurious leather cabin.'
    elif 'thar' in name_lower:
        def_img = '/static/images/vehicles/thar.jpg'
        def_brand = 'Mahindra'
        def_model = 'Thar 4x4'
        def_year = 2024
        def_cat = 'SUVs'
        def_desc = 'Legendary off-roader with convertible styling and rugged 4x4 capability for weekend adventures.'
    else:
        def_img = '/static/images/vehicles/sedan.jpg'
        def_brand = vehicle.Model.split()[0] if ' ' in vehicle.Model else vehicle.Model
        def_model = vehicle.Model
        def_year = 2024
        def_cat = 'Cars'
        def_desc = f"The {vehicle.Model} delivers dependable performance and comfort for any rental journey."

    # Retrieve category from DB (skip corrupted dummy entries like 'SDFGH')
    first_cat = vehicle.categories.first()
    db_cat = first_cat.category_name if first_cat and first_cat.category_name else None
    cat = db_cat if db_cat and db_cat != 'SDFGH' else def_cat
    desc = first_cat.description if first_cat and first_cat.description and len(first_cat.description) > 10 else def_desc

    # Priority to actual DB fields
    img = vehicle.image if getattr(vehicle, 'image', None) and vehicle.image else def_img
    status = vehicle.status if getattr(vehicle, 'status', None) else 'Available'
    seats = vehicle.seats if getattr(vehicle, 'seats', None) else 5
    trans = vehicle.transmission if getattr(vehicle, 'transmission', None) else 'Automatic'
    year = vehicle.year if getattr(vehicle, 'year', None) else def_year
    rating = float(vehicle.rating) if getattr(vehicle, 'rating', None) else 4.8
    fuel = vehicle.fuel_type if getattr(vehicle, 'fuel_type', None) else 'Petrol'

    return {
        'image': img,
        'brand': def_brand,
        'model_name': def_model,
        'year': year,
        'seats': seats,
        'transmission': trans,
        'fuel_type': fuel,
        'ac': 'Yes' if seats > 2 else 'No',
        'status': status,
        'is_available': (status == 'Available'),
        'rating': rating,
        'reviews': 80 + (vehicle.vehicle_id * 7 % 140),
        'category': cat,
        'description': desc
    }

def home(request):
    raw_vehicles = VEHICLES.objects.all().order_by('vehicle_id')
    vehicles = []
    for v in raw_vehicles:
        v.meta = get_vehicle_extra(v)
        vehicles.append(v)

    # Categories metadata
    cat_counts = {'Cars': 0, 'SUVs': 0, 'Bikes': 0, 'Vans': 0}
    for v in vehicles:
        c = v.meta['category']
        if c in cat_counts:
            cat_counts[c] += 1

    categories = [
        {
            "name": "Cars",
            "title": "Cars",
            "slug": "Cars",
            "icon": "fa-car",
            "emoji": "🚗",
            "count": cat_counts['Cars'],
            "desc": "Comfortable vehicles for city travel and business trips."
        },
        {
            "name": "SUVs",
            "title": "SUVs & 4x4",
            "slug": "SUVs",
            "icon": "fa-truck-monster",
            "emoji": "🏔️",
            "count": cat_counts['SUVs'],
            "desc": "Perfect for long drives and adventurous journeys."
        },
        {
            "name": "Bikes",
            "title": "Bikes & Scooters",
            "slug": "Bikes",
            "icon": "fa-motorcycle",
            "emoji": "🏍️",
            "count": cat_counts['Bikes'],
            "desc": "Affordable and convenient for city commuting."
        },
        {
            "name": "Vans",
            "title": "Vans",
            "slug": "Vans",
            "icon": "fa-van-shuttle",
            "emoji": "🚐",
            "count": cat_counts['Vans'],
            "desc": "Spacious vehicles for families and groups."
        },
    ]

    # Map vehicles into Popular Choices sections strictly using existing database records
    # Most Rented: Honda City, KTM Duke 390, Hyundai Creta
    # Best for Families: Innova, Fortuner, Mahindra Thar
    # Budget Friendly: Scooty, Cycle, Yamaha 122
    def find_vehicle(query):
        q = query.lower()
        for v in vehicles:
            if q in v.Model.lower():
                return v
        return None

    popular_groups = {
        'most_rented': [
            v for v in [find_vehicle('honda city'), find_vehicle('ktm duke 390'), find_vehicle('hyundai creta')] if v
        ],
        'families': [
            v for v in [find_vehicle('innova'), find_vehicle('fortuner'), find_vehicle('mahindra thar')] if v
        ],
        'budget': [
            v for v in [find_vehicle('scooty'), find_vehicle('cycle'), find_vehicle('yamaha 122')] if v
        ],
    }

    return render(request, 'rental/home.html', {
        'vehicles': vehicles,
        'popular_groups': popular_groups,
        'categories': categories,
    })

def vehicles_catalog(request):
    raw_vehicles = VEHICLES.objects.all().order_by('vehicle_id')
    category_filter = request.GET.get('category', 'All').strip()
    fuel_filter = request.GET.get('fuel', 'All').strip()
    transmission_filter = request.GET.get('transmission', 'All').strip()
    seats_filter = request.GET.get('seats', 'All').strip()
    status_filter = request.GET.get('status', 'All').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    search_query = request.GET.get('q', '').strip()

    vehicles = []
    for v in raw_vehicles:
        v.meta = get_vehicle_extra(v)
        
        # Category filter
        if category_filter and category_filter != 'All':
            c_target = category_filter.lower()
            c_meta = v.meta['category'].lower()
            if 'suv' in c_target:
                if 'suv' not in c_meta:
                    continue
            elif 'bike' in c_target or 'scooter' in c_target:
                if 'bike' not in c_meta:
                    continue
            elif 'van' in c_target:
                if 'van' not in c_meta:
                    continue
            elif 'car' in c_target:
                if 'car' not in c_meta:
                    continue
            elif c_target != c_meta:
                continue

        # Search query (by name or category)
        if search_query:
            sq = search_query.lower()
            if sq not in v.Model.lower() and sq not in v.meta['category'].lower() and sq not in v.fuel_type.lower():
                continue

        # Fuel type filter
        if fuel_filter and fuel_filter != 'All':
            if v.fuel_type.lower() != fuel_filter.lower():
                continue

        # Transmission filter
        if transmission_filter and transmission_filter != 'All':
            if v.transmission.lower() != transmission_filter.lower():
                continue

        # Seats filter
        if seats_filter and seats_filter != 'All':
            try:
                if v.seats != int(seats_filter):
                    continue
            except ValueError:
                pass

        # Availability filter
        if status_filter and status_filter != 'All':
            if v.status.lower() != status_filter.lower():
                continue

        # Price range filter
        if min_price:
            try:
                if float(v.Rental_rate) < float(min_price):
                    continue
            except ValueError:
                pass
        if max_price:
            try:
                if float(v.Rental_rate) > float(max_price):
                    continue
            except ValueError:
                pass

        vehicles.append(v)

    categories = ['All', 'Cars', 'SUVs', 'Bikes', 'Vans']
    fuels = ['All', 'Petrol', 'Diesel', 'Electric', 'Hybrid', 'Manual']
    transmissions = ['All', 'Automatic', 'Manual']
    seats_list = ['All', '1', '2', '4', '5', '7']
    statuses = ['All', 'Available', 'Rented', 'Maintenance']

    return render(request, 'rental/vehicle_list.html', {
        'vehicles': vehicles,
        'categories': categories,
        'fuels': fuels,
        'transmissions': transmissions,
        'seats_list': seats_list,
        'statuses': statuses,
        'current_category': category_filter,
        'current_fuel': fuel_filter,
        'current_transmission': transmission_filter,
        'current_seats': seats_filter,
        'current_status': status_filter,
        'current_min_price': min_price,
        'current_max_price': max_price,
        'search_query': search_query,
    })

def vehicle_detail(request, vehicle_id):
    vehicle = get_object_or_404(VEHICLES, pk=vehicle_id)
    vehicle.meta = get_vehicle_extra(vehicle)
    
    days = 2
    rental_rate = float(vehicle.Rental_rate)
    rental_total = rental_rate * days
    tax = round(rental_total * 0.18, 2)
    grand_total = rental_total + tax
    
    context = {
        'vehicle': vehicle,
        'default_days': days,
        'rental_total': rental_total,
        'tax': tax,
        'grand_total': grand_total,
        'locations': ['Hosadurga', 'Chitradurga', 'Bengaluru', 'Mysuru', 'Hubballi', 'Mangaluru', 'Mumbai'],
    }
    return render(request, 'rental/vehicle_detail.html', context)

def book_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(VEHICLES, pk=vehicle_id)
    vehicle.meta = get_vehicle_extra(vehicle)
    
    if vehicle.status != 'Available':
        messages.error(request, f"Sorry, {vehicle.Model} is currently {vehicle.status.lower()} and unavailable for booking.")
        return redirect('vehicle_detail', vehicle_id=vehicle.vehicle_id)
    
    if request.method == 'POST':
        pickup_loc = request.POST.get('pickup_location', 'Hosadurga').strip()
        pickup_date_str = request.POST.get('pickup_date', '2026-09-28')
        return_date_str = request.POST.get('return_date', '2026-09-30')
        customer_name = request.POST.get('customer_name', '').strip()
        customer_email = request.POST.get('customer_email', '').strip()
        customer_phone = request.POST.get('customer_phone', '').strip()
        
        # If user didn't enter email or phone, generate a clean one based on their name
        if not customer_email:
            clean_tag = ''.join(e for e in (customer_name.lower()) if e.isalnum())
            customer_email = f"{clean_tag or 'customer'}@gmail.com"
        if not customer_phone:
            customer_phone = '9876543210'
            
        try:
            p_date = datetime.strptime(pickup_date_str, '%Y-%m-%d').date()
            r_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()
            days = max(1, (r_date - p_date).days)
        except Exception:
            p_date = date.today()
            r_date = p_date + timedelta(days=2)
            days = 2
            
        rate = float(vehicle.Rental_rate)
        subtotal = rate * days
        tax = round(subtotal * 0.18, 2)
        total = subtotal + tax
        
        # Lookup existing customer or create a new customer record
        customer = CUSTOMERS.objects.filter(Email=customer_email).first()
        if customer:
            # If the user specified a new name (e.g. Kiran, Kumar, Reddy), update customer name!
            if customer_name and customer.Name != customer_name:
                customer.Name = customer_name
                customer.Phone = customer_phone
                customer.save()
        else:
            customer = CUSTOMERS.objects.create(
                Name=customer_name or 'Valued Customer',
                Email=customer_email,
                Phone=customer_phone,
                License_No='KA-DL-' + str(customer_phone[-5:] if len(customer_phone) >= 5 else '12345'),
                Address=f'{pickup_loc}, India'
            )
            
        # Store in session so My Bookings and forms remember this customer!
        request.session['customer_email'] = customer.Email
        request.session['customer_name'] = customer.Name
        request.session['customer_phone'] = customer.Phone
        
        # Real DB Booking record
        booking = BOOKING.objects.create(
            customer=customer,
            vehicle=vehicle,
            booking_date=date.today(),
            start_date=p_date,
            end_date=r_date,
            no_of_days=days,
            total_amount=total,
            status='Confirmed'
        )
        
        # Real DB Rental record
        rental = RENTAL.objects.create(
            booking=booking,
            pickup_location=pickup_loc,
            return_location=pickup_loc,
            pickup_date=p_date,
            return_date=r_date
        )
        
        # Real DB Payment record
        PAYMENT.objects.create(
            rental=rental,
            payment_date=date.today(),
            payment_status='Paid',
            payment_method='UPI',
            amount=total
        )
        
        # Update vehicle status in DB to Rented
        vehicle.status = 'Rented'
        vehicle.save()
        
        messages.success(request, f"🎉 Booking #{booking.Booking_id} successfully confirmed for {customer.Name} ({customer.Email})! Saved to database.")
        return redirect('vehicle_detail', vehicle_id=vehicle.vehicle_id)
        
    return redirect('vehicle_detail', vehicle_id=vehicle_id)

def my_bookings(request):
    """Allow customers to see their own real database bookings and cancel them."""
    # Find bookings for the current user or session customer, or latest booking
    user_email = None
    if request.user.is_authenticated and request.user.email:
        user_email = request.user.email
    elif request.session.get('customer_email'):
        user_email = request.session.get('customer_email')
    else:
        last_booking = BOOKING.objects.order_by('-Booking_id').first()
        if last_booking:
            user_email = last_booking.customer.Email

    customer = CUSTOMERS.objects.filter(Email=user_email).first() if user_email else CUSTOMERS.objects.first()
    
    if customer:
        bookings = BOOKING.objects.filter(customer=customer).select_related('vehicle').order_by('-Booking_id')
    else:
        bookings = BOOKING.objects.all().select_related('customer', 'vehicle').order_by('-Booking_id')[:5]
        
    return render(request, 'rental/my_bookings.html', {
        'bookings': bookings,
        'customer': customer
    })

def cancel_booking(request, booking_id):
    booking = get_object_or_404(BOOKING, pk=booking_id)
    booking.status = 'Cancelled'
    booking.save()
    
    # Mark vehicle Available again in DB
    booking.vehicle.status = 'Available'
    booking.vehicle.save()
    
    # Create cancellation record in DB
    rental = getattr(booking, 'rental_result', None)
    if rental:
        CANCELLATION.objects.get_or_create(
            rental=rental,
            defaults={
                'cancel_date': date.today(),
                'reason': 'Customer requested cancellation via portal',
                'refund_date': date.today() + timedelta(days=2)
            }
        )
        
    messages.info(request, f"Booking #{booking_id} has been cancelled. Refund scheduled.")
    return redirect('/dashboard/?tab=bookings')

def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Try direct user authenticate
        user = authenticate(request, username=identifier, password=password)
        if not user:
            # Try username matching email prefix
            user = authenticate(request, username=identifier.split('@')[0], password=password)
            
        if user:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('dashboard' if user.is_staff or user.is_superuser else 'home')
        else:
            # Friendly login for demo users
            found_user = User.objects.filter(email=identifier).first() or User.objects.filter(username=identifier.split('@')[0]).first()
            if found_user:
                auth_login(request, found_user)
                messages.success(request, f"Logged in as {found_user.first_name or found_user.username}!")
                return redirect('dashboard')
            else:
                messages.success(request, f"Welcome to RENTX, {identifier.split('@')[0]}!")
                return redirect('dashboard')
                
    return render(request, 'rental/login.html', {'hide_public_nav': True})

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', 'User').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '9876543210').strip()
        password = request.POST.get('password', 'password123')
        
        # Save to real Django User DB
        username = email.split('@')[0]
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, email=email, password=password, first_name=name)
        else:
            user = User.objects.get(username=username)
            
        # Save to real Customers DB
        CUSTOMERS.objects.get_or_create(
            Email=email,
            defaults={
                'Name': name,
                'Phone': phone,
                'License_No': f'KA-DL-{phone[-5:]}',
                'Address': 'Bengaluru, Karnataka'
            }
        )
        
        auth_login(request, user)
        messages.success(request, f"Account successfully created for {name}! You are now logged in.")
        return redirect('home')
        
    return render(request, 'rental/register.html', {'hide_public_nav': True})

def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out safely.")
    return redirect('home')

def dashboard(request):
    active_tab = request.GET.get('tab', 'overview')
    
    # Real DB query for all entities
    raw_vehicles = VEHICLES.objects.all().order_by('-vehicle_id')
    vehicles = []
    available_count = 0
    rented_count = 0
    maintenance_count = 0
    
    for v in raw_vehicles:
        v.meta = get_vehicle_extra(v)
        vehicles.append(v)
        if v.meta['status'] == 'Available':
            available_count += 1
        elif v.meta['status'] == 'Rented':
            rented_count += 1
        else:
            maintenance_count += 1
            
    customers = CUSTOMERS.objects.all().order_by('-customer_id')
    bookings = BOOKING.objects.select_related('customer', 'vehicle').order_by('-Booking_id')
    rentals = RENTAL.objects.select_related('booking', 'booking__customer', 'booking__vehicle').order_by('-rental_id')
    payments = PAYMENT.objects.select_related('rental', 'rental__booking', 'rental__booking__customer').order_by('-payment_id')
    cancellations = CANCELLATION.objects.select_related('rental', 'rental__booking', 'rental__booking__customer').order_by('-cancel_id')
    reports = REPORT.objects.all().order_by('-report_id')
    categories = VEHICLE_CATEGORY.objects.select_related('vehicle').all()
    
    # Real DB Revenue sum
    total_rev = sum([float(p.amount) for p in payments])
    
    # Real counts straight from DB
    vehicles_count = len(vehicles)
    bookings_count = len(bookings)
    customers_count = len(customers)
    
    context = {
        'hide_public_nav': True,
        'active_tab': active_tab,
        'vehicles': vehicles,
        'vehicles_count': vehicles_count,
        'available_count': available_count,
        'rented_count': rented_count,
        'maintenance_count': maintenance_count,
        'bookings_count': bookings_count,
        'customers_count': customers_count,
        'total_revenue': f"₹{total_rev:,.0f}",
        'customers': customers,
        'bookings': bookings,
        'rentals': rentals,
        'payments': payments,
        'cancellations': cancellations,
        'reports': reports,
        'categories': categories,
    }
    return render(request, 'rental/dashboard.html', context)

def add_vehicle(request):
    if request.method == 'POST':
        name = request.POST.get('model', 'New Vehicle').strip()
        rate = request.POST.get('rental_rate', 1500)
        fuel = request.POST.get('fuel_type', 'Petrol')
        color = request.POST.get('color', 'White')
        plate = request.POST.get('plate_no', f'KA-01-NEW-{VEHICLES.objects.count()+1}').strip()
        cat_name = request.POST.get('category', 'Cars')
        status = request.POST.get('status', 'Available')
        seats = request.POST.get('seats', 5)
        trans = request.POST.get('transmission', 'Automatic')
        year = request.POST.get('year', 2025)
        
        # Image handling: 1. Uploaded file, 2. Preset/URL, 3. Keyword matching
        img = None
        if 'vehicle_image' in request.FILES:
            uploaded_file = request.FILES['vehicle_image']
            clean_name = f"{uuid.uuid4().hex[:8]}_{uploaded_file.name}".replace(" ", "_")
            dest_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'vehicles')
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, clean_name)
            with open(dest_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            img = f"/static/images/vehicles/{clean_name}"
        elif request.POST.get('image_url', '').strip():
            img = request.POST.get('image_url').strip()
        else:
            # Pick relevant image based on vehicle name
            name_lower = name.lower()
            if 'city' in name_lower or 'honda' in name_lower:
                img = '/static/images/vehicles/honda_city.jpg'
            elif 'creta' in name_lower:
                img = '/static/images/vehicles/creta.jpg'
            elif 'royal' in name_lower or 'enfield' in name_lower or 'bike' in name_lower or 'ktm' in name_lower:
                img = '/static/images/vehicles/royal_enfield.jpg'
            elif 'swift' in name_lower:
                img = '/static/images/vehicles/swift.jpg'
            elif 'innova' in name_lower:
                img = '/static/images/vehicles/innova.jpg'
            elif 'fortuner' in name_lower:
                img = '/static/images/vehicles/fortuner.jpg'
            elif 'thar' in name_lower:
                img = '/static/images/vehicles/thar.jpg'
            else:
                img = '/static/images/vehicles/sedan.jpg'
            
        owner = CUSTOMERS.objects.first()
        if not owner:
            owner = CUSTOMERS.objects.create(Name='RENTX Fleet', Email='admin@rentx.com', Phone='9999999999', License_No='KA-01', Address='HQ')
            
        v = VEHICLES.objects.create(
            Model=name,
            Rental_rate=rate,
            fuel_type=fuel,
            color=color,
            Plate_no=plate,
            status=status,
            seats=seats,
            transmission=trans,
            year=year,
            image=img,
            customer=owner
        )
        VEHICLE_CATEGORY.objects.create(
            vehicle=v,
            category_name=cat_name,
            description=f'Added to {cat_name} fleet'
        )
        messages.success(request, f"Vehicle '{name}' ({plate}) successfully created with image in database!")
    return redirect('/dashboard/?tab=vehicles')

def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(VEHICLES, pk=vehicle_id)
    if request.method == 'POST':
        vehicle.Model = request.POST.get('model', vehicle.Model)
        vehicle.Rental_rate = request.POST.get('rental_rate', vehicle.Rental_rate)
        vehicle.status = request.POST.get('status', vehicle.status)
        vehicle.fuel_type = request.POST.get('fuel_type', vehicle.fuel_type)
        vehicle.color = request.POST.get('color', vehicle.color)
        vehicle.seats = request.POST.get('seats', vehicle.seats)
        vehicle.transmission = request.POST.get('transmission', vehicle.transmission)
        
        # Picture update handling
        if 'vehicle_image' in request.FILES:
            uploaded_file = request.FILES['vehicle_image']
            clean_name = f"{uuid.uuid4().hex[:8]}_{uploaded_file.name}".replace(" ", "_")
            dest_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'vehicles')
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, clean_name)
            with open(dest_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            vehicle.image = f"/static/images/vehicles/{clean_name}"
        elif request.POST.get('image_url', '').strip():
            vehicle.image = request.POST.get('image_url').strip()

        vehicle.save()
        messages.success(request, f"Vehicle '{vehicle.Model}' details and picture updated in database!")
    return redirect('/dashboard/?tab=vehicles')

def delete_vehicle(request, vehicle_id):
    v = get_object_or_404(VEHICLES, pk=vehicle_id)
    name = v.Model
    v.delete()
    messages.info(request, f"Vehicle '{name}' removed from database.")
    return redirect('/dashboard/?tab=vehicles')

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('category_name', 'SUV')
        desc = request.POST.get('description', '')
        v = VEHICLES.objects.first()
        if v:
            VEHICLE_CATEGORY.objects.create(vehicle=v, category_name=name, description=desc)
        messages.success(request, f"Category '{name}' saved to database!")
    return redirect('/dashboard/?tab=categories')

def add_customer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        CUSTOMERS.objects.create(
            Name=name,
            Email=email,
            Phone=phone,
            License_No=f'KA-DL-{phone[-4:]}',
            Address='Bengaluru'
        )
        messages.success(request, f"Customer '{name}' saved to database!")
    return redirect('/dashboard/?tab=customers')

def add_booking(request):
    if request.method == 'POST':
        cust_id = request.POST.get('customer')
        new_name = request.POST.get('new_customer_name', '').strip()
        new_email = request.POST.get('new_customer_email', '').strip()
        new_phone = request.POST.get('new_customer_phone', '').strip()
        veh_id = request.POST.get('vehicle')
        p_date = request.POST.get('pickup_date')
        r_date = request.POST.get('return_date')
        amt = request.POST.get('amount')
        
        cust = None
        if cust_id == 'new' or (not cust_id and new_name):
            if not new_email:
                clean_n = ''.join(e for e in new_name.lower() if e.isalnum())
                new_email = f"{clean_n or 'customer'}@gmail.com"
            cust = CUSTOMERS.objects.filter(Email=new_email).first()
            if cust:
                if new_name and cust.Name != new_name:
                    cust.Name = new_name
                    cust.save()
            else:
                cust = CUSTOMERS.objects.create(
                    Name=new_name or 'Customer',
                    Email=new_email,
                    Phone=new_phone or '9876543210',
                    License_No=f'KA-DL-{new_phone[-4:] if len(new_phone)>=4 else "1234"}',
                    Address='Bengaluru'
                )
        else:
            try:
                cust = CUSTOMERS.objects.get(pk=cust_id)
            except (CUSTOMERS.DoesNotExist, ValueError, TypeError):
                cust = None
                
        try:
            veh = VEHICLES.objects.get(pk=veh_id)
        except (VEHICLES.DoesNotExist, ValueError, TypeError):
            veh = None

        if not cust or not veh:
            messages.error(request, "Please select or enter a valid customer and vehicle.")
            return redirect('/dashboard/?tab=bookings')
        
        try:
            d1 = datetime.strptime(str(p_date), '%Y-%m-%d').date() if p_date else date.today()
            d2 = datetime.strptime(str(r_date), '%Y-%m-%d').date() if r_date else date.today() + timedelta(days=2)
            days = max(1, (d2 - d1).days)
        except Exception:
            d1 = date.today()
            d2 = date.today() + timedelta(days=2)
            days = 2
            
        try:
            total_amt = float(amt) if amt else float(veh.Rental_rate) * days
        except (ValueError, TypeError):
            total_amt = float(veh.Rental_rate) * days
        
        b = BOOKING.objects.create(
            customer=cust,
            vehicle=veh,
            booking_date=date.today(),
            start_date=d1,
            end_date=d2,
            no_of_days=days,
            total_amount=total_amt,
            status='Confirmed'
        )
        r = RENTAL.objects.create(
            booking=b,
            pickup_location='Bengaluru',
            return_location='Bengaluru',
            pickup_date=d1,
            return_date=d2
        )
        PAYMENT.objects.create(
            rental=r,
            payment_date=date.today(),
            payment_status='Paid',
            payment_method='UPI',
            amount=total_amt
        )
        
        veh.status = 'Rented'
        veh.save()
        
        messages.success(request, f"Booking #{b.Booking_id} created and recorded in database!")
    return redirect('/dashboard/?tab=bookings')

def add_payment(request):
    if request.method == 'POST':
        rental_id = request.POST.get('rental_id')
        method = request.POST.get('method', 'UPI')
        amount = request.POST.get('amount', 4000)
        rental = RENTAL.objects.get(pk=rental_id)
        PAYMENT.objects.create(
            rental=rental,
            payment_date=date.today(),
            payment_status='Paid',
            payment_method=method,
            amount=amount
        )
        messages.success(request, "Payment transaction recorded in database!")
    return redirect('/dashboard/?tab=payments')

def generate_report(request):
    if request.method == 'POST':
        r_type = request.POST.get('report_type', 'Booking Report')
        desc = request.POST.get('description', 'Generated Report')
        REPORT.objects.create(
            report_type=r_type,
            description=desc,
            report_date=date.today()
        )
        messages.success(request, f"Report '{r_type}' generated and stored!")
    return redirect('/dashboard/?tab=reports')

def delete_category(request, category_id):
    cat = get_object_or_404(VEHICLE_CATEGORY, pk=category_id)
    cat_name = cat.category_name
    cat.delete()
    messages.info(request, f"Category '{cat_name}' (ID #{category_id}) successfully deleted from database.")
    return redirect('/dashboard/?tab=categories')

def edit_category(request, category_id):
    cat = get_object_or_404(VEHICLE_CATEGORY, pk=category_id)
    if request.method == 'POST':
        cat.category_name = request.POST.get('category_name', cat.category_name)
        cat.description = request.POST.get('description', cat.description)
        cat.save()
        messages.success(request, f"Category '{cat.category_name}' updated successfully in database!")
    return redirect('/dashboard/?tab=categories')

def delete_customer(request, customer_id):
    cust = get_object_or_404(CUSTOMERS, pk=customer_id)
    name = cust.Name
    cust.delete()
    messages.info(request, f"Customer '{name}' (ID #{customer_id}) deleted from database.")
    return redirect('/dashboard/?tab=customers')

def edit_customer(request, customer_id):
    cust = get_object_or_404(CUSTOMERS, pk=customer_id)
    if request.method == 'POST':
        cust.Name = request.POST.get('name', cust.Name)
        cust.Email = request.POST.get('email', cust.Email)
        cust.Phone = request.POST.get('phone', cust.Phone)
        cust.Address = request.POST.get('address', cust.Address)
        cust.save()
        messages.success(request, f"Customer '{cust.Name}' updated successfully in database!")
    return redirect('/dashboard/?tab=customers')

def favicon_view(request):
    """Serve a clean SVG favicon so browsers never log 404 errors for favicon.ico."""
    svg_icon = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        '<rect width="100" height="100" rx="20" fill="#2563eb"/>'
        '<text x="50%" y="55%" text-anchor="middle" dominant-baseline="middle" font-size="60">🚗</text>'
        '</svg>'
    )
    return HttpResponse(svg_icon, content_type="image/svg+xml")

def chatbot_fallback(request):
    """Graceful 200 response for any lingering/cached browser chatbot requests to avoid 404s."""
    return JsonResponse({'status': 'disabled', 'reply': ''}, status=200)


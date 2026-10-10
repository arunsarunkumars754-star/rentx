import os

base_dir = r"c:\Users\Asus\vehicle-rental\rental\templates\rental"
os.makedirs(base_dir, exist_ok=True)

templates = {
    "base.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Vehicle Rental{% endblock %}</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Custom CSS -->
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #f8f9fa; }
        .navbar { box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .hero { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 100px 0; }
        .card { border: none; border-radius: 12px; box-shadow: 0 6px 16px rgba(0,0,0,0.08); transition: transform 0.3s; }
        .card:hover { transform: translateY(-5px); }
        .btn-primary { background-color: #2a5298; border: none; }
        .btn-primary:hover { background-color: #1e3c72; }
    </style>
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-light bg-white sticky-top">
  <div class="container">
    <a class="navbar-brand fw-bold" href="{% url 'home' %}">🚗 AutoRentals</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item">
          <a class="nav-link" href="{% url 'home' %}">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{% url 'vehicle_list' %}">Vehicles</a>
        </li>
        {% if user.is_authenticated %}
            <li class="nav-item">
            <a class="nav-link" href="{% url 'customer_dashboard' %}">Dashboard</a>
            </li>
            <li class="nav-item">
            <a class="nav-link text-danger" href="{% url 'logout' %}">Logout</a>
            </li>
        {% else %}
            <li class="nav-item">
            <a class="nav-link" href="{% url 'login' %}">Login</a>
            </li>
            <li class="nav-item">
            <a class="nav-link btn btn-primary text-white ms-2 px-3" href="{% url 'register' %}">Register</a>
            </li>
        {% endif %}
      </ul>
    </div>
  </div>
</nav>

<div class="container mt-4">
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        {% endfor %}
    {% endif %}
    
    {% block content %}{% endblock %}
</div>

<footer class="bg-dark text-white text-center py-4 mt-5">
    <p class="mb-0">&copy; 2026 AutoRentals. All rights reserved.</p>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
{% block extra_js %}{% endblock %}
</body>
</html>
""",

    "home.html": """{% extends 'rental/base.html' %}

{% block content %}
<div class="hero text-center rounded-4 mb-5">
    <h1 class="display-4 fw-bold">Rent Your Perfect Vehicle</h1>
    <p class="lead mt-3">Simple, fast and convenient vehicle rental management.</p>
    <div class="mt-4">
        <a href="{% url 'vehicle_list' %}" class="btn btn-light btn-lg px-4 me-2 text-primary fw-bold">Browse Vehicles</a>
        {% if not user.is_authenticated %}
            <a href="{% url 'register' %}" class="btn btn-outline-light btn-lg px-4">Login / Register</a>
        {% endif %}
    </div>
</div>

<h2 class="text-center fw-bold mb-4">Featured Vehicles</h2>
<div class="row">
    {% for vehicle in featured_vehicles %}
    <div class="col-md-4 mb-4">
        <div class="card h-100">
            {% if vehicle.image %}
                <img src="{{ vehicle.image.url }}" class="card-img-top" alt="{{ vehicle.model }}">
            {% else %}
                <div class="card-img-top bg-secondary text-white d-flex align-items-center justify-content-center" style="height: 200px;">No Image</div>
            {% endif %}
            <div class="card-body">
                <h5 class="card-title">{{ vehicle.model }}</h5>
                <p class="text-muted mb-1">{{ vehicle.category.category_name }} | {{ vehicle.fuel_type }}</p>
                <h6 class="text-primary fw-bold">${{ vehicle.rental_rate }} / day</h6>
            </div>
            <div class="card-footer bg-white border-0 text-center pb-3">
                <a href="{% url 'vehicle_detail' vehicle.pk %}" class="btn btn-outline-primary w-100 mb-2">View Details</a>
                <a href="{% url 'book_vehicle' vehicle.pk %}" class="btn btn-primary w-100">Book Now</a>
            </div>
        </div>
    </div>
    {% empty %}
    <div class="col-12 text-center">
        <p>No featured vehicles currently available.</p>
    </div>
    {% endfor %}
</div>
{% endblock %}
""",

    "vehicle_list.html": """{% extends 'rental/base.html' %}

{% block content %}
<div class="row mb-4 align-items-center">
    <div class="col-md-6">
        <h2 class="fw-bold m-0">Our Vehicles</h2>
    </div>
    <div class="col-md-6">
        <form method="GET" class="d-flex">
            <input type="text" name="model" class="form-control me-2" placeholder="Search by model...">
            <select name="category" class="form-select me-2">
                <option value="">All Categories</option>
                {% for cat in categories %}
                    <option value="{{ cat.category_id }}">{{ cat.category_name }}</option>
                {% endfor %}
            </select>
            <button class="btn btn-primary" type="submit">Filter</button>
        </form>
    </div>
</div>

<div class="row">
    {% for vehicle in vehicles %}
    <div class="col-md-4 mb-4">
        <div class="card h-100">
            {% if vehicle.image %}
                <img src="{{ vehicle.image.url }}" class="card-img-top" alt="{{ vehicle.model }}">
            {% else %}
                <div class="card-img-top bg-secondary text-white d-flex align-items-center justify-content-center" style="height: 200px;">No Image</div>
            {% endif %}
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <h5 class="card-title">{{ vehicle.model }}</h5>
                    {% if vehicle.is_available %}
                        <span class="badge bg-success align-self-start">Available</span>
                    {% else %}
                        <span class="badge bg-danger align-self-start">Unavailable</span>
                    {% endif %}
                </div>
                <p class="text-muted mb-1">{{ vehicle.category.category_name }} | {{ vehicle.fuel_type }} | {{ vehicle.color }}</p>
                <h6 class="text-primary fw-bold">${{ vehicle.rental_rate }} / day</h6>
            </div>
            <div class="card-footer bg-white border-0 text-center pb-3">
                <a href="{% url 'vehicle_detail' vehicle.pk %}" class="btn btn-outline-primary w-100 mb-2">View Details</a>
                {% if vehicle.is_available %}
                    <a href="{% url 'book_vehicle' vehicle.pk %}" class="btn btn-primary w-100">Book Now</a>
                {% endif %}
            </div>
        </div>
    </div>
    {% empty %}
    <div class="col-12 text-center">
        <p>No vehicles found matching your criteria.</p>
    </div>
    {% endfor %}
</div>
{% endblock %}
""",

    "vehicle_detail.html": """{% extends 'rental/base.html' %}

{% block content %}
<div class="card shadow-sm mt-4">
    <div class="row g-0">
        <div class="col-md-6">
            {% if vehicle.image %}
                <img src="{{ vehicle.image.url }}" class="img-fluid rounded-start h-100 object-fit-cover" alt="{{ vehicle.model }}">
            {% else %}
                <div class="bg-secondary text-white d-flex align-items-center justify-content-center h-100" style="min-height: 400px;">No Image Available</div>
            {% endif %}
        </div>
        <div class="col-md-6">
            <div class="card-body p-5">
                <h2 class="card-title fw-bold mb-1">{{ vehicle.model }}</h2>
                <p class="text-muted mb-4">{{ vehicle.category.category_name }}</p>
                
                <h3 class="text-primary fw-bold mb-4">${{ vehicle.rental_rate }} <span class="fs-6 text-muted fw-normal">/ day</span></h3>
                
                <ul class="list-group list-group-flush mb-4">
                    <li class="list-group-item px-0"><strong>Plate Number:</strong> {{ vehicle.plate_no }}</li>
                    <li class="list-group-item px-0"><strong>Fuel Type:</strong> {{ vehicle.fuel_type }}</li>
                    <li class="list-group-item px-0"><strong>Color:</strong> {{ vehicle.color }}</li>
                    <li class="list-group-item px-0">
                        <strong>Availability:</strong> 
                        {% if vehicle.is_available %}
                            <span class="text-success fw-bold">Available</span>
                        {% else %}
                            <span class="text-danger fw-bold">Unavailable</span>
                        {% endif %}
                    </li>
                </ul>
                
                {% if vehicle.is_available %}
                    <a href="{% url 'book_vehicle' vehicle.pk %}" class="btn btn-primary btn-lg w-100">Book Now</a>
                {% else %}
                    <button class="btn btn-secondary btn-lg w-100" disabled>Currently Unavailable</button>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",

    "login.html": """{% extends 'rental/base.html' %}
{% load django_bootstrap5 %}

{% block content %}
<div class="row justify-content-center mt-5">
    <div class="col-md-5">
        <div class="card p-4">
            <h3 class="text-center mb-4 fw-bold">Login to Your Account</h3>
            <form method="POST">
                {% csrf_token %}
                {% bootstrap_form form %}
                <button type="submit" class="btn btn-primary w-100 mt-3">Login</button>
            </form>
            <p class="text-center mt-3">Don't have an account? <a href="{% url 'register' %}">Register here</a></p>
        </div>
    </div>
</div>
{% endblock %}
""",

    "register.html": """{% extends 'rental/base.html' %}
{% load django_bootstrap5 %}

{% block content %}
<div class="row justify-content-center mt-5">
    <div class="col-md-6">
        <div class="card p-4">
            <h3 class="text-center mb-4 fw-bold">Create an Account</h3>
            <form method="POST">
                {% csrf_token %}
                {% bootstrap_form form %}
                <button type="submit" class="btn btn-primary w-100 mt-3">Register</button>
            </form>
            <p class="text-center mt-3">Already have an account? <a href="{% url 'login' %}">Login here</a></p>
        </div>
    </div>
</div>
{% endblock %}
""",

    "customer_dashboard.html": """{% extends 'rental/base.html' %}

{% block content %}
<div class="row mt-4">
    <div class="col-md-4">
        <div class="card p-4 mb-4">
            <h4 class="fw-bold">My Profile</h4>
            <hr>
            <p><strong>Name:</strong> {{ customer.name }}</p>
            <p><strong>Email:</strong> {{ customer.email }}</p>
            <p><strong>Phone:</strong> {{ customer.phone }}</p>
            <p><strong>Address:</strong> {{ customer.address }}</p>
        </div>
    </div>
    
    <div class="col-md-8">
        <div class="card p-4">
            <h4 class="fw-bold mb-4">My Bookings</h4>
            {% if bookings %}
                <div class="table-responsive">
                    <table class="table table-hover align-middle">
                        <thead class="table-light">
                            <tr>
                                <th>Booking ID</th>
                                <th>Vehicle</th>
                                <th>Dates</th>
                                <th>Total</th>
                                <th>Status</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for booking in bookings %}
                            <tr>
                                <td>#{{ booking.booking_id }}</td>
                                <td>{{ booking.vehicle.model }}</td>
                                <td>{{ booking.start_date|date:"M d, Y" }} <br><small>to {{ booking.end_date|date:"M d, Y" }}</small></td>
                                <td>${{ booking.total_amount }}</td>
                                <td>
                                    <span class="badge {% if booking.status == 'Confirmed' %}bg-success{% elif booking.status == 'Pending' %}bg-warning{% elif booking.status == 'Cancelled' %}bg-danger{% else %}bg-secondary{% endif %}">
                                        {{ booking.status }}
                                    </span>
                                </td>
                                <td>
                                    {% if booking.status == 'Pending' or booking.status == 'Confirmed' %}
                                        <a href="{% url 'cancel_booking' booking.pk %}" class="btn btn-sm btn-outline-danger">Cancel</a>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="text-center py-4">
                    <p class="text-muted">You have no bookings yet.</p>
                    <a href="{% url 'vehicle_list' %}" class="btn btn-primary">Browse Vehicles</a>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
""",

    "book_vehicle.html": """{% extends 'rental/base.html' %}
{% load django_bootstrap5 %}

{% block content %}
<div class="row mt-4">
    <div class="col-md-4">
        <div class="card mb-4">
            <div class="card-body">
                <h5 class="card-title fw-bold">Vehicle Details</h5>
                <hr>
                <p><strong>Model:</strong> {{ vehicle.model }}</p>
                <p><strong>Rate:</strong> $<span id="dailyRate">{{ vehicle.rental_rate }}</span> / day</p>
                <p><strong>Fuel:</strong> {{ vehicle.fuel_type }}</p>
            </div>
        </div>
    </div>
    
    <div class="col-md-8">
        <div class="card p-4">
            <h3 class="fw-bold mb-4">Book {{ vehicle.model }}</h3>
            <form method="POST">
                {% csrf_token %}
                <div class="row">
                    <div class="col-md-6 mb-3">
                        {% bootstrap_field form.start_date %}
                    </div>
                    <div class="col-md-6 mb-3">
                        {% bootstrap_field form.end_date %}
                    </div>
                </div>
                
                <div class="alert alert-info mt-3">
                    <strong>Total Calculated Amount: </strong> $<span id="totalAmount">0.00</span>
                </div>
                
                <button type="submit" class="btn btn-primary btn-lg w-100 mt-3">Confirm Booking</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const startDateInput = document.getElementById('id_start_date');
        const endDateInput = document.getElementById('id_end_date');
        const rateSpan = document.getElementById('dailyRate');
        const totalSpan = document.getElementById('totalAmount');
        
        function calculateTotal() {
            if (startDateInput.value && endDateInput.value) {
                const start = new Date(startDateInput.value);
                const end = new Date(endDateInput.value);
                const rate = parseFloat(rateSpan.innerText);
                
                const timeDiff = end.getTime() - start.getTime();
                let daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));
                
                if (daysDiff < 0) {
                    totalSpan.innerText = "Invalid Dates";
                    return;
                }
                
                if (daysDiff === 0) daysDiff = 1; // Minimum 1 day rental
                
                const total = daysDiff * rate;
                totalSpan.innerText = total.toFixed(2);
            }
        }
        
        startDateInput.addEventListener('change', calculateTotal);
        endDateInput.addEventListener('change', calculateTotal);
    });
</script>
{% endblock %}
""",

    "cancel_booking.html": """{% extends 'rental/base.html' %}

{% block content %}
<div class="row justify-content-center mt-5">
    <div class="col-md-6">
        <div class="card p-4 border-danger">
            <h3 class="text-center text-danger mb-4 fw-bold">Cancel Booking</h3>
            
            <div class="mb-4">
                <p><strong>Booking ID:</strong> #{{ booking.booking_id }}</p>
                <p><strong>Vehicle:</strong> {{ booking.vehicle.model }}</p>
                <p><strong>Dates:</strong> {{ booking.start_date }} to {{ booking.end_date }}</p>
                <p><strong>Total Amount:</strong> ${{ booking.total_amount }}</p>
            </div>
            
            <div class="alert alert-warning">
                Are you sure you want to cancel this booking? This action cannot be undone.
            </div>
            
            <form method="POST">
                {% csrf_token %}
                <div class="mb-3">
                    <label for="reason" class="form-label">Reason for Cancellation (Optional)</label>
                    <textarea name="reason" id="reason" class="form-control" rows="3"></textarea>
                </div>
                <div class="d-flex justify-content-between">
                    <a href="{% url 'customer_dashboard' %}" class="btn btn-secondary">Keep Booking</a>
                    <button type="submit" class="btn btn-danger">Yes, Cancel Booking</button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
"""
}

for filename, content in templates.items():
    filepath = os.path.join(base_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Templates created successfully!")

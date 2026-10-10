# Vehicle Rental Management System

A complete web application built with Django, MySQL, and Bootstrap 5.

## Features
- **Customer Portal**: Browse vehicles, book vehicles, manage profile, view bookings, and cancel bookings.
- **Admin Dashboard**: Manage customers, vehicle categories, vehicles, bookings, rentals, payments, cancellations, and view reports.
- **Booking Engine**: Date overlap checking, automatic pricing calculation, and status tracking.
- **Responsive Design**: Mobile-friendly UI using Bootstrap 5.

## Technology Stack
- **Backend**: Python 3, Django 4.2
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: MySQL

## Setup Instructions

### 1. Database Setup (MySQL)
Ensure MySQL is installed and running on your machine. Open your MySQL client/terminal and run:
```sql
CREATE DATABASE vehicle_rental_db;
```
*(If your MySQL user is not `root` or has a password, update `vehicle_rental/settings.py` -> `DATABASES` section accordingly).*

### 2. Environment Setup
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Migrations & Database Initialization
Once MySQL is configured in `settings.py`, run:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Admin)
```powershell
python manage.py createsuperuser
```
*(Enter admin, email, and password when prompted)*

### 5. Run the Server
```powershell
python manage.py runserver
```

## Sample Data

To load sample data easily, log into the `/admin/` portal and create:
1. **Vehicle Categories**: (e.g., Sedan, SUV, Hatchback, Bike)
2. **Vehicles**: Add realistic vehicles (e.g., Honda Civic, Toyota RAV4) assigned to the created categories. Ensure `is_available` is checked.

## Test Credentials
- **Admin**: The credentials you created in step 4.
- **Customer**: Create a new account via the `/register/` page on the main website.

## How to Explain in a Viva
- **Architecture**: MVT (Model-View-Template) architecture using Django.
- **Database**: Relational Database (MySQL) with clear foreign key constraints linking `Vehicle` to `VehicleCategory`, and `Booking` to `Customer` & `Vehicle`.
- **Logic**: Booking overlap is checked using Django ORM (`start_date__lte` and `end_date__gte`). Total amount is calculated dynamically on the frontend via JavaScript and validated/saved on the backend.
- **Security**: Django's built-in authentication, CSRF tokens on all POST forms, password hashing, and `@login_required` decorators restricting access to dashboards and booking functionalities.

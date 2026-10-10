from django.db import models

class REPORT(models.Model):
    report_id = models.AutoField(primary_key=True)
    report_type = models.CharField(max_length=255)
    description = models.TextField()
    report_date = models.DateField()

    class Meta:
        db_table = 'report'

    def __str__(self):
        return f"Report #{self.report_id} - {self.report_type}"


class CUSTOMERS(models.Model):
    customer_id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Address = models.TextField()
    Email = models.EmailField(unique=True)
    Phone = models.CharField(max_length=20)
    License_No = models.CharField(max_length=50)

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return self.Name


class VEHICLES(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    Plate_no = models.CharField(max_length=50, unique=True)
    Model = models.CharField(max_length=255)
    Rental_rate = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='Available') # Available, Rented, Maintenance
    image = models.CharField(max_length=255, default='', blank=True)
    seats = models.IntegerField(default=5)
    transmission = models.CharField(max_length=50, default='Automatic')
    year = models.IntegerField(default=2024)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.8)
    # Relationship A: CUSTOMERS (1) : VEHICLES (N)
    customer = models.ForeignKey(CUSTOMERS, on_delete=models.CASCADE, related_name='vehicles')

    class Meta:
        db_table = 'vehicles'

    def __str__(self):
        return self.Model


class VEHICLE_CATEGORY(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # Relationship B: VEHICLES (1) : VEHICLE_CATEGORY (N)
    vehicle = models.ForeignKey(VEHICLES, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        db_table = 'vehicle_category'

    def __str__(self):
        return self.category_name


class BOOKING(models.Model):
    Booking_id = models.AutoField(primary_key=True)
    booking_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    no_of_days = models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50, default='Confirmed') # Confirmed, Pending, Completed, Cancelled
    # FK: vehicle_id, customer_id
    vehicle = models.ForeignKey(VEHICLES, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(CUSTOMERS, on_delete=models.CASCADE, related_name='bookings')

    class Meta:
        db_table = 'booking'

    def __str__(self):
        return f"Booking #{self.Booking_id}"


class RENTAL(models.Model):
    rental_id = models.AutoField(primary_key=True)
    pickup_location = models.CharField(max_length=255)
    return_location = models.CharField(max_length=255)
    pickup_date = models.DateField()
    return_date = models.DateField()
    # Relationship G: RENTAL (1) : BOOKING (1) — booking_id FK
    booking = models.OneToOneField(BOOKING, on_delete=models.CASCADE, related_name='rental_result')

    class Meta:
        db_table = 'rental'

    def __str__(self):
        return f"Rental #{self.rental_id}"


class PAYMENT(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_date = models.DateField()
    payment_status = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # FK: rental_id — Relationship E: PAYMENT (1) : RENTAL (1)
    rental = models.OneToOneField(RENTAL, on_delete=models.CASCADE, related_name='payment')
    # Relationship D: REPORT (1) : PAYMENT (N)
    report = models.ForeignKey(REPORT, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)

    class Meta:
        db_table = 'payment'

    def __str__(self):
        return f"Payment #{self.payment_id}"


class CANCELLATION(models.Model):
    cancel_id = models.AutoField(primary_key=True)
    cancel_date = models.DateField()
    reason = models.TextField()
    refund_date = models.DateField(null=True, blank=True)
    # Relationship H: RENTAL (1) : CANCELLATION (1)
    rental = models.OneToOneField(RENTAL, on_delete=models.CASCADE, related_name='cancellation')

    class Meta:
        db_table = 'cancellation'

    def __str__(self):
        return f"Cancellation #{self.cancel_id}"

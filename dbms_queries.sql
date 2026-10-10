
-- Database: vehicle_rental_db
-- 

USE vehicle_rental_db;
-


SHOW TABLES;


DESCRIBE customers;
DESCRIBE vehicles;
DESCRIBE vehicle_category;
DESCRIBE booking;
DESCRIBE rental;
DESCRIBE payment;
DESCRIBE cancellation;
DESCRIBE report;

-- Add a new column to vehicles table (Example: insurance_expiry)
ALTER TABLE vehicles ADD COLUMN insurance_valid_until DATE;

-- Modify column data type
ALTER TABLE customers MODIFY Phone VARCHAR(25);

--  Add an index for faster search by vehicle status
CREATE INDEX idx_vehicle_status ON vehicles(status);


-- DATA MANIPULATION LANGUAGE (DML) COMMANDS


-- Insert a new customer
INSERT INTO customers (Name, Address, Email, Phone, License_No)
VALUES ('Vikram Rao', 'Indiranagar, Bangalore', 'vikram.rao@gmail.com', '9845099881', 'KA-03-2024-88990');

-- Update vehicle rental rate
UPDATE vehicles 
SET Rental_rate = 1950.00 
WHERE Model = 'Honda City';

--  Update booking status
UPDATE booking 
SET status = 'Completed' 
WHERE Booking_id = 1;

-- Delete cancelled bookings without active rentals
DELETE FROM cancellation 
WHERE cancel_id = 999;



--  SIMPLE SELECTION & FILTERING (DQL)


--  Display all available vehicles
SELECT vehicle_id, Model, Rental_rate, fuel_type, seats, transmission 
FROM vehicles 
WHERE status = 'Available';

--  Find luxury / high-end vehicles costing more than ₹2000 per day
SELECT Model, Rental_rate, fuel_type 
FROM vehicles 
WHERE Rental_rate >= 2000.00 
ORDER BY Rental_rate DESC;

--  Find vehicles with Automatic transmission and at least 5 seats
SELECT vehicle_id, Model, seats, transmission, Rental_rate 
FROM vehicles 
WHERE transmission = 'Automatic' AND seats >= 5;

-- Pattern matching: Find customers with Gmail addresses
SELECT customer_id, Name, Email, Phone 
FROM customers 
WHERE Email LIKE '%@gmail.com';

-- Range condition: Bookings made for 2 to 4 days
SELECT Booking_id, customer_id, vehicle_id, no_of_days, total_amount 
FROM booking 
WHERE no_of_days BETWEEN 2 AND 4;




-- Count total vehicles, minimum rate, maximum rate, and average rate
SELECT 
    COUNT(*) AS total_fleet_count,
    MIN(Rental_rate) AS min_rate,
    MAX(Rental_rate) AS max_rate,
    ROUND(AVG(Rental_rate), 2) AS average_rate
FROM vehicles;

-- Total revenue collected from completed payments
SELECT 
    payment_status,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_revenue
FROM payment
GROUP BY payment_status;

--  Total bookings and amount spent per customer
SELECT 
    c.customer_id,
    c.Name,
    COUNT(b.Booking_id) AS total_bookings,
    SUM(b.total_amount) AS total_spent
FROM customers c
JOIN booking b ON c.customer_id = b.customer_id
GROUP BY c.customer_id, c.Name
ORDER BY total_spent DESC;

--  Categories having more than 1 vehicle (HAVING clause)
SELECT 
    category_name, 
    COUNT(*) AS vehicle_count 
FROM vehicle_category 
GROUP BY category_name 
HAVING COUNT(*) >= 1;

--  Revenue grouped by Payment Method (UPI, Card, Net Banking)
SELECT 
    payment_method, 
    COUNT(*) AS count_used, 
    SUM(amount) AS total_collected 
FROM payment 
GROUP BY payment_method;


--  INNER JOIN: Display Booking Details with Customer Name and Vehicle Model
SELECT 
    b.Booking_id,
    c.Name AS customer_name,
    c.Phone AS customer_phone,
    v.Model AS vehicle_model,
    v.Plate_no,
    b.start_date,
    b.end_date,
    b.no_of_days,
    b.total_amount,
    b.status
FROM booking b
INNER JOIN customers c ON b.customer_id = c.customer_id
INNER JOIN vehicles v ON b.vehicle_id = v.vehicle_id
ORDER BY b.Booking_id DESC;

-- TABLE JOIN: Full Rental Lifecycle (Customer -> Booking -> Rental -> Payment)
SELECT 
    c.Name AS customer_name,
    v.Model AS vehicle_rented,
    r.rental_id,
    r.pickup_location,
    r.return_location,
    r.pickup_date,
    r.return_date,
    p.amount AS payment_amount,
    p.payment_method,
    p.payment_status
FROM customers c
JOIN booking b ON c.customer_id = b.customer_id
JOIN vehicles v ON b.vehicle_id = v.vehicle_id
JOIN rental r ON b.Booking_id = r.booking_id
JOIN payment p ON r.rental_id = p.rental_id;

--  LEFT OUTER JOIN: Find all vehicles and their bookings (including unbooked vehicles)
SELECT 
    v.vehicle_id,
    v.Model,
    v.Plate_no,
    v.status,
    b.Booking_id,
    b.start_date,
    b.end_date
FROM vehicles v
LEFT JOIN booking b ON v.vehicle_id = b.vehicle_id;

--  Identify customers who have NEVER placed any bookings
SELECT 
    c.customer_id, 
    c.Name, 
    c.Email 
FROM customers c
LEFT JOIN booking b ON c.customer_id = b.customer_id
WHERE b.Booking_id IS NULL;



--  NESTED QUERIES / SUBQUERIES (CORRELATED & NON-CORRELATED)


-- Subquery with AVG(): Vehicles that cost more than the average rental rate
SELECT vehicle_id, Model, Rental_rate, fuel_type 
FROM vehicles 
WHERE Rental_rate > (
    SELECT AVG(Rental_rate) FROM vehicles
);

--  Subquery with IN: Customers who made at least one booking
SELECT customer_id, Name, Email, Phone 
FROM customers 
WHERE customer_id IN (
    SELECT DISTINCT customer_id FROM booking
);

-- Subquery with NOT IN: Vehicles that have never been cancelled
SELECT vehicle_id, Model, Plate_no 
FROM vehicles 
WHERE vehicle_id NOT IN (
    SELECT b.vehicle_id 
    FROM booking b 
    JOIN rental r ON b.Booking_id = r.booking_id
    JOIN cancellation cn ON r.rental_id = cn.rental_id
);

--  Correlated Subquery: Find the highest paying customer
SELECT Name, Email 
FROM customers c 
WHERE EXISTS (
    SELECT 1 FROM booking b 
    WHERE b.customer_id = c.customer_id 
    AND b.total_amount = (SELECT MAX(total_amount) FROM booking)
);



-- View for Active Bookings Summary
CREATE OR REPLACE VIEW vw_active_bookings AS
SELECT 
    b.Booking_id,
    c.Name AS customer_name,
    c.Phone,
    v.Model AS vehicle_model,
    v.Plate_no,
    b.start_date,
    b.end_date,
    b.total_amount,
    b.status
FROM booking b
JOIN customers c ON b.customer_id = c.customer_id
JOIN vehicles v ON b.vehicle_id = v.vehicle_id
WHERE b.status IN ('Confirmed', 'Pending');

SELECT * FROM vw_active_bookings;

--  View for Total Revenue Analysis by Vehicle
CREATE OR REPLACE VIEW vw_vehicle_revenue_report AS
SELECT 
    v.vehicle_id,
    v.Model,
    v.Plate_no,
    COUNT(b.Booking_id) AS times_booked,
    COALESCE(SUM(p.amount), 0) AS total_revenue_generated
FROM vehicles v
LEFT JOIN booking b ON v.vehicle_id = b.vehicle_id
LEFT JOIN rental r ON b.Booking_id = r.booking_id
LEFT JOIN payment p ON r.rental_id = p.rental_id AND p.payment_status = 'Paid'
GROUP BY v.vehicle_id, v.Model, v.Plate_no;

SELECT * FROM vw_vehicle_revenue_report ORDER BY total_revenue_generated DESC;




-- Stored Procedure: Get All Available Vehicles By Fuel Type
DELIMITER //
CREATE PROCEDURE GetAvailableVehiclesByFuel(IN p_fuel VARCHAR(50))
BEGIN
    SELECT vehicle_id, Model, Rental_rate, fuel_type, seats, transmission
    FROM vehicles
    WHERE status = 'Available' AND fuel_type = p_fuel;
END //
DELIMITER ;


--  Stored Procedure: Calculate Total Spent by a Customer
DELIMITER //
CREATE PROCEDURE GetCustomerTotalSpending(IN p_cust_id INT, OUT p_total DECIMAL(10,2))
BEGIN
    SELECT COALESCE(SUM(total_amount), 0.00) INTO p_total
    FROM booking
    WHERE customer_id = p_cust_id;
END //
DELIMITER ;



--  Trigger: Automatically mark vehicle as 'Rented' when a booking is Confirmed
DELIMITER //
CREATE TRIGGER trg_after_booking_confirmed
AFTER INSERT ON booking
FOR EACH ROW
BEGIN
    IF NEW.status = 'Confirmed' THEN
        UPDATE vehicles 
        SET status = 'Rented' 
        WHERE vehicle_id = NEW.vehicle_id;
    END IF;
END //
DELIMITER ;

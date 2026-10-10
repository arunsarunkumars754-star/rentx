

CREATE DATABASE IF NOT EXISTS vehicle_rental_db;
USE vehicle_rental_db;

-- Disable foreign key checks while recreating tables
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS cancellation;
DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS rental;
DROP TABLE IF EXISTS booking;
DROP TABLE IF EXISTS vehicle_category;
DROP TABLE IF EXISTS vehicles;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS report;
SET FOREIGN_KEY_CHECKS = 1;

--  Table structure for table: report

CREATE TABLE report (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    report_type VARCHAR(255) NOT NULL,
    description TEXT,
    report_date DATE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--  Table structure for table: customers

CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Address TEXT,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Phone VARCHAR(20),
    License_No VARCHAR(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--  Table structure for table: vehicles

CREATE TABLE vehicles (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    Plate_no VARCHAR(50) UNIQUE NOT NULL,
    Model VARCHAR(255) NOT NULL,
    Rental_rate DECIMAL(10,2) NOT NULL,
    color VARCHAR(50),
    fuel_type VARCHAR(50),
    status VARCHAR(50) DEFAULT 'Available',
    image VARCHAR(255) DEFAULT '',
    seats INT DEFAULT 5,
    transmission VARCHAR(50) DEFAULT 'Automatic',
    year INT DEFAULT 2024,
    rating DECIMAL(3,1) DEFAULT 4.8,
    customer_id INT NOT NULL,
    CONSTRAINT fk_vehicle_customer FOREIGN KEY (customer_id) 
        REFERENCES customers(customer_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--  Table structure for table: vehicle_category

CREATE TABLE vehicle_category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL,
    description TEXT,
    vehicle_id INT NOT NULL,
    CONSTRAINT fk_category_vehicle FOREIGN KEY (vehicle_id) 
        REFERENCES vehicles(vehicle_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table: booking

CREATE TABLE booking (
    Booking_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_date DATE NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    no_of_days INT DEFAULT 0,
    total_amount DECIMAL(10,2) DEFAULT 0.00,
    status VARCHAR(50) DEFAULT 'Confirmed',
    customer_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    CONSTRAINT fk_booking_customer FOREIGN KEY (customer_id) 
        REFERENCES customers(customer_id) ON DELETE CASCADE,
    CONSTRAINT fk_booking_vehicle FOREIGN KEY (vehicle_id) 
        REFERENCES vehicles(vehicle_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--rental
CREATE TABLE rental (
    rental_id INT AUTO_INCREMENT PRIMARY KEY,
    pickup_location VARCHAR(255) NOT NULL,
    return_location VARCHAR(255) NOT NULL,
    pickup_date DATE NOT NULL,
    return_date DATE NOT NULL,
    booking_id INT UNIQUE NOT NULL,
    CONSTRAINT fk_rental_booking FOREIGN KEY (booking_id) 
        REFERENCES booking(Booking_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--payment
CREATE TABLE payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    payment_date DATE NOT NULL,
    payment_status VARCHAR(50) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    rental_id INT UNIQUE NOT NULL,
    report_id INT DEFAULT NULL,
    CONSTRAINT fk_payment_rental FOREIGN KEY (rental_id) 
        REFERENCES rental(rental_id) ON DELETE CASCADE,
    CONSTRAINT fk_payment_report FOREIGN KEY (report_id) 
        REFERENCES report(report_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table structure for table: cancellation

CREATE TABLE cancellation (
    cancel_id INT AUTO_INCREMENT PRIMARY KEY,
    cancel_date DATE NOT NULL,
    reason TEXT NOT NULL,
    refund_date DATE DEFAULT NULL,
    rental_id INT UNIQUE NOT NULL,
    CONSTRAINT fk_cancellation_rental FOREIGN KEY (rental_id) 
        REFERENCES rental(rental_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;





-- Dumping data for table `report`
INSERT INTO `report` (`report_id`, `report_type`, `description`, `report_date`) VALUES
    (7, 'Booking Report', 'Monthly booking trends, frequency of rentals, and vehicle popularity.', '2026-09-25'),
    (8, 'Revenue Report', 'Total revenue, gross transaction value, and payment channel distribution.', '2026-09-25'),
    (9, 'Vehicle Usage Report', 'Vehicle mileage tracking, fleet maintenance schedules, and utilization percentage.', '2026-09-25'),
    (10, 'Customer Report', 'Customer registration rate, loyalty metrics, and KYC verification records.', '2026-09-25'),
    (11, 'Cancellation Report', 'Cancellation frequency, customer feedback on cancellations, and refund processing.', '2026-09-25');

-- Dumping data for table `customers`
INSERT INTO `customers` (`customer_id`, `Name`, `Address`, `Email`, `Phone`, `License_No`) VALUES
    (9, 'Arun', 'Indiranagar, Bengaluru', 'arun@gmail.com', '9811043210', 'DL-01-2022-00123'),
    (10, 'Kiran', 'Koramangala, Bengaluru', 'kiran@gmail.com', '9898712345', 'KA-04-2021-99887'),
    (11, 'Rahul', 'Whitefield, Bengaluru', 'rahul@gmail.com', '9098776655', 'KA-01-2023-45678'),
    (12, 'Priya', 'HSR Layout, Bengaluru', 'priya@gmail.com', '8765432109', 'MH-02-2020-11223'),
    (13, 'Sneha', 'Jayanagar, Bengaluru', 'sneha@gmail.com', '7654321098', 'DL-03-2022-77889'),
    (14, 'Fleet Admin', 'RENTX Central HQ, Bengaluru', 'admin@rentx.com', '9000000000', 'SYS-FLEET-01'),
    (15, 'Deepak Verma', 'Bengaluru Airport, India', 'deepak@gmail.com', '9845012345', 'KA-DL-12345'),
    (16, 'reddy', 'Bengaluru, India', 'reddy@gmail.com', '9811043245', 'KA-DL-43245'),
    (17, 'jeevandeep', 'Hosadurga, India', 'jeevan@gmail.com', '9811043210', 'KA-DL-43210');

-- Dumping data for table `vehicles`
INSERT INTO `vehicles` (`vehicle_id`, `Plate_no`, `Model`, `Rental_rate`, `color`, `fuel_type`, `customer_id`, `image`, `rating`, `seats`, `status`, `transmission`, `year`) VALUES
    (19, 'KA-01-HC-1800', 'Honda City', 1800, 'White', 'Petrol', 14, '/static/images/vehicles/honda_city.jpg', 4.8, 5, 'Rented', 'Automatic', 2025),
    (20, 'KA-03-CR-2200', 'Hyundai Creta', 2200, 'Phantom Black', 'Diesel', 14, '/static/images/vehicles/creta.jpg', 4.7, 5, 'Available', 'Automatic', 2024),
    (21, 'KA-05-RE-0900', 'Royal Enfield', 900, 'Chrome Bronze', 'Petrol', 14, '/static/images/vehicles/royal_enfield.jpg', 4.9, 2, 'Available', 'Manual', 2024),
    (22, 'KA-02-SW-1500', 'Swift', 1500, 'Pearl Red', 'Petrol', 14, '/static/images/vehicles/swift.jpg', 4.6, 5, 'Available', 'Manual', 2024),
    (23, 'KA-04-IN-2500', 'Innova', 2500, 'Silver Metallic', 'Diesel', 14, '/static/images/vehicles/innova.jpg', 4.8, 7, 'Maintenance', 'Automatic', 2023),
    (24, 'KA-01-FT-3500', 'Fortuner', 3500, 'Super White', 'Diesel', 14, '/static/images/vehicles/fortuner.jpg', 4.9, 7, 'Rented', 'Automatic', 2025),
    (25, 'KA-04-TH-2800', 'Mahindra Thar', 2800, 'Mystic Copper', 'Diesel', 14, '/static/images/vehicles/thar.jpg', 4.8, 4, 'Rented', 'Automatic', 2024),
    (26, 'KA-03-NX-2000', 'Tata Nexon EV', 2000, 'Teal Blue', 'Electric', 14, '/static/images/vehicles/sedan.jpg', 4.7, 5, 'Available', 'Automatic', 2025),
    (27, 'KA-02-KT-1100', 'KTM Duke 390', 1100, 'Electric Orange', 'Petrol', 14, '/static/images/vehicles/royal_enfield.jpg', 4.9, 2, 'Available', 'Manual', 2024),
    (28, 'KA-01-M3-9999', 'BMW M3 Competition Track Edition', 7200, 'Frozen Black', 'Petrol', 9, '/static/images/vehicles/sedan.jpg', 4.8, 4, 'Rented', 'Automatic', 2026);

-- Dumping data for table `vehicle_category`
INSERT INTO `vehicle_category` (`category_id`, `category_name`, `description`, `vehicle_id`) VALUES
    (20, 'SUVs', 'Dynamic SUV with commanding road presence, panoramic sunroof and premium audio system.', 20),
    (21, 'Bikes', 'Iconic cruiser with timeless styling, throaty exhaust note and unmatched road presence.', 21),
    (22, 'Cars', 'Zippy, efficient, and effortless to park. Perfect for navigating city traffic with great fuel economy.', 22),
    (23, 'Vans', 'Supreme comfort for family and executive travels with plush captain seats and expansive luggage space.', 23),
    (24, 'SUVs', 'Formidable 4x4 SUV built to conquer any terrain with unmatched power and luxurious leather cabin.', 24),
    (25, 'SUVs', 'Legendary off-roader with convertible top and rugged capability for weekend adventures.', 25),
    (26, 'Cars', 'Eco-friendly, fast acceleration with 400km range and cutting-edge tech connectivity.', 26),
    (27, 'Bikes', 'High-performance naked streetfighter with razor sharp cornering dynamics.', 27),
    (28, 'Cars', 'Added to Cars fleet', 28);

-- Dumping data for table `booking`
INSERT INTO `booking` (`Booking_id`, `booking_date`, `start_date`, `end_date`, `no_of_days`, `total_amount`, `customer_id`, `vehicle_id`, `status`) VALUES
    (9, '2026-09-27', '2026-09-28', '2026-09-30', 2, 3600, 9, 19, 'Confirmed'),
    (10, '2026-09-27', '2026-09-29', '2026-10-02', 3, 4400, 10, 20, 'Cancelled'),
    (11, '2026-09-26', '2026-09-30', '2026-10-03', 3, 3200, 11, 22, 'Completed'),
    (12, '2026-09-26', '2026-10-01', '2026-10-04', 3, 7500, 12, 23, 'Confirmed'),
    (13, '2026-09-27', '2026-10-02', '2026-10-05', 3, 7000, 13, 24, 'Cancelled'),
    (14, '2026-09-27', '2026-09-28', '2026-09-30', 2, 4248, 15, 19, 'Cancelled'),
    (15, '2026-09-27', '2026-09-28', '2026-09-30', 2, 2596, 10, 27, 'Cancelled'),
    (16, '2026-09-27', '2026-09-28', '2026-10-01', 3, 6372, 16, 19, 'Confirmed'),
    (17, '2026-09-27', '2026-09-28', '2026-09-30', 2, 8260, 9, 24, 'Cancelled'),
    (18, '2026-09-27', '2026-09-28', '2026-10-01', 3, 25488, 17, 28, 'Confirmed'),
    (19, '2026-09-27', '2026-09-28', '2026-10-01', 3, 12390, 9, 24, 'Confirmed'),
    (20, '2026-09-27', '2026-09-28', '2026-09-30', 2, 6608, 9, 25, 'Confirmed');

-- Dumping data for table `rental`
INSERT INTO `rental` (`rental_id`, `pickup_location`, `return_location`, `pickup_date`, `return_date`, `booking_id`) VALUES
    (9, 'Bengaluru', 'Bengaluru', '2026-09-28', '2026-09-30', 9),
    (10, 'Bengaluru', 'Bengaluru', '2026-09-29', '2026-10-02', 10),
    (11, 'Bengaluru', 'Bengaluru', '2026-09-30', '2026-10-03', 11),
    (12, 'Bengaluru', 'Bengaluru', '2026-10-01', '2026-10-04', 12),
    (13, 'Bengaluru', 'Bengaluru', '2026-10-02', '2026-10-05', 13),
    (14, 'Bengaluru Airport', 'Bengaluru Airport', '2026-09-28', '2026-09-30', 14),
    (15, 'Bengaluru', 'Bengaluru', '2026-09-28', '2026-09-30', 15),
    (16, 'Bengaluru', 'Bengaluru', '2026-09-28', '2026-10-01', 16),
    (17, 'Bengaluru', 'Bengaluru', '2026-09-28', '2026-09-30', 17),
    (18, 'Hosadurga', 'Hosadurga', '2026-09-28', '2026-10-01', 18),
    (19, 'Bengaluru', 'Bengaluru', '2026-09-28', '2026-10-01', 19),
    (20, 'Bengaluru', 'Bengaluru', '2026-09-28', '2026-09-30', 20);

-- Dumping data for table `payment`
INSERT INTO `payment` (`payment_id`, `payment_date`, `payment_status`, `payment_method`, `amount`, `rental_id`, `report_id`) VALUES
    (9, '2026-09-27', 'Paid', 'UPI', 4248, 9, 8),
    (10, '2026-09-27', 'Pending', 'Card', 4400, 10, 8),
    (11, '2026-09-26', 'Paid', 'UPI', 3200, 11, 8),
    (12, '2026-09-26', 'Paid', 'Card', 7500, 12, 8),
    (13, '2026-09-27', 'Pending', 'Net Banking', 7000, 13, 8),
    (14, '2026-09-27', 'Paid', 'UPI', 4248, 14, NULL),
    (15, '2026-09-27', 'Paid', 'UPI', 2596, 15, NULL),
    (16, '2026-09-27', 'Paid', 'UPI', 6372, 16, NULL),
    (17, '2026-09-27', 'Paid', 'UPI', 8260, 17, NULL),
    (18, '2026-09-27', 'Paid', 'UPI', 25488, 18, NULL),
    (19, '2026-09-27', 'Paid', 'UPI', 12390, 19, NULL),
    (20, '2026-09-27', 'Paid', 'UPI', 6608, 20, NULL);

-- Dumping data for table `cancellation`
INSERT INTO `cancellation` (`cancel_id`, `cancel_date`, `reason`, `refund_date`, `rental_id`) VALUES
    (6, '2026-09-27', 'Change in plans', '2026-09-29', 9),
    (7, '2026-09-30', 'Personal work', '2026-10-02', 10),
    (8, '2026-10-01', 'Weather issue', '2026-10-03', 11),
    (9, '2026-10-05', 'Medical reason', '2026-10-07', 12),
    (10, '2026-10-06', 'Other', '2026-10-08', 13),
    (11, '2026-09-27', 'Customer requested cancellation via portal', '2026-09-29', 14),
    (12, '2026-09-27', 'Customer requested cancellation via portal', '2026-09-29', 15),
    (13, '2026-09-27', 'Customer requested cancellation via portal', '2026-09-29', 17);

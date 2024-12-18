CREATE TABLE client
(
	clientId INT PRIMARY KEY,
    clientName VARCHAR(50),
    PhoneNumber VARCHAR(25),
    email VARCHAR (50),
    address TEXT,
    dateOfBirth DATE,
    balance DECIMAL(10,2),
    createdAt TIMESTAMP
);

ALTER TABLE client MODIFY clientId INT NOT NULL AUTO_INCREMENT;

CREATE TABLE eventCategory
(
	categoryId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    categoryName VARCHAR(50),
    description TEXT
);

CREATE TABLE event(
	eventId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    categoryId INT,
    title TEXT,
    description TEXT,
    pricePerPax DECIMAL(10,2),
	FOREIGN KEY (categoryId) REFERENCES eventCategory(categoryId)
);

CREATE TABLE venue(
	venueId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    venueName VARCHAR(100),
    address TEXT,
    capacity INT,
    pricePerHour DECIMAL(10,2)
);

CREATE TABLE eventTask(
	taskId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    taskName VARCHAR(50),
    taskPrice DECIMAL (10,2)
);

CREATE TABLE booking(
	bookingId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    clientId INT,
    eventId INT,
    venueId INT,
    numberOfGuest INT,
    status ENUM ('Pending' , 'Confirmed' ) DEFAULT 'Pending',
    totalAmount DECIMAL(10,2),
    bookedAt DATE,
    FOREIGN KEY (clientId) REFERENCES client(clientId),
    FOREIGN KEY (eventId) REFERENCES event(eventId),
    FOREIGN KEY (venueId) REFERENCES venue(venueId)
    
);



CREATE TABLE bookedTask(
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    bookingId INT NOT NULL,
    taskId INT NOT NULL,
    FOREIGN KEY (bookingId) REFERENCES booking(bookingId),
    FOREIGN KEY (taskId) REFERENCES eventTask(taskId)
);

CREATE TABLE schedule(
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    bookingId INT NOT NULL,
    startDate DATE NOT NULL,
    endDate DATE NOT NULL, 
    startTime TIME NOT NULL, 
    endTime TIME NOT NULL,
    FOREIGN KEY (bookingId) REFERENCES booking (bookingId)
);

CREATE TABLE payment(
	paymentId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    bookingId INT NOT NULL,
    paymentDate DATE,
    paymentStatus ENUM ('Pending', 'Confirmed' , 'Declined') DEFAULT 'Pending',
    paidAmount DECIMAL (10,2) CHECK (paidAmount > 0),
    FOREIGN KEY (bookingId) REFERENCES booking (bookingId)
);

CREATE TABLE bookingHistory(
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    clientId INT NOT NULL,
    clientName VARCHAR(50),
    eventId INT NOT NULL,
    eventTitle TEXT,
    categoryId INT NOT NULL,
    categoryName VARCHAR (25),
    venueId INT NOT NULL,
    venueName VARCHAR(100),
    venueTotalPrice DECIMAL(10,2),
    scheduleId INT NOT NULL,
    startDate DATE,
    endDate DATE,
    numberOfGuest INT,
    totalPaxAmount DECIMAL(10,2),
    bookedAt DATE
);

CREATE TABLE bookingHistoryDetails(
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    historyId INT NOT NULL,
    taskId INT NOT NULL,
    taskName VARCHAR(50),
    taskPrice DECIMAL (10,2),
    totalTaskPrice DECIMAL (10,2),
    totalPaidAmount DECIMAL (10,2),
    FOREIGN KEY (historyId) REFERENCES bookingHistory (id)
);



-- DMl
INSERT INTO client (clientName, PhoneNumber, email, address, dateOfBirth, balance, createdAt)
VALUES
('John Doe', '1234567890', 'john.doe@example.com', '123 Main St', '1985-05-15', 1500.50, NOW()),
('Jane Smith', '9876543210', 'jane.smith@example.com', '456 Oak St', '1990-08-25', 3000.00, NOW());
('Alice Johnson', '5553334444', 'alice.johnson@example.com', '789 Elm St', '1992-11-30', 2000.00, NOW());



INSERT INTO eventCategory (categoryName, description)
VALUES
('Conference', 'Corporate conferences and business events'),
('Wedding', 'Wedding ceremonies and receptions'),
('Party', 'Casual parties and gatherings');


INSERT INTO event (categoryId, title, description, pricePerPax)
VALUES
(1, 'Tech Conference 2024', 'A gathering of tech leaders and innovators.', 500.00),
(2, 'Wedding Ceremony', 'A beautiful wedding ceremony in a garden setting.', 300.00),
(3, 'Birthday Party', 'A fun-filled birthday celebration.', 150.00);


INSERT INTO venue (venueName, address, capacity, pricePerHour)
VALUES
('Grand Ballroom', '789 Luxury Rd', 500, 2000.00),
('Garden Venue', '101 Nature Ave', 300, 1200.00),
('Rooftop Lounge', '202 Skyline Dr', 200, 1500.00);


INSERT INTO eventTask (taskName, taskPrice)
VALUES
('Catering Service', 5000.00),
('Photography', 2000.00),
('Sound System', 1500.00);

INSERT INTO booking (clientId, eventId, venueId, numberOfGuest, status, totalAmount, bookedAt)
VALUES
(1, 1, 1, 200, 'Confirmed', 150000.00, '2024-01-10'),
(2, 2, 2, 100, 'Pending', 90000.00, '2024-01-15');


INSERT INTO bookedTask (bookingId, taskId)
VALUES
(1, 1),
(1, 2),
(2, 3);


INSERT INTO schedule (bookingId, startDate, endDate, startTime, endTime)
VALUES
(1, '2024-01-20', '2024-01-20', '10:00:00', '18:00:00'),
(2, '2024-02-14', '2024-02-14', '12:00:00', '16:00:00');

INSERT INTO payment (bookingId, paymentDate, paymentStatus, paidAmount)
VALUES
(1, '2024-01-12', 'Confirmed', 75000.00),
(2, '2024-01-18', 'Pending', 30000.00);

INSERT INTO bookingHistory (clientId, clientName, eventId, eventTitle, categoryId, categoryName, venueId, venueName, venueTotalPrice, scheduleId, startDate, endDate, numberOfGuest, totalPaxAmount, bookedAt)
VALUES
(1, 'John Doe', 1, 'Tech Conference 2024', 1, 'Conference', 1, 'Grand Ballroom', 8000.00, 1, '2024-01-20', '2024-01-20', 200, 100000.00, '2024-01-10');

INSERT INTO bookingHistoryDetails (historyId, taskId, taskName, taskPrice, totalTaskPrice, totalPaidAmount)
VALUES
(1, 1, 'Catering Service', 5000.00, 10000.00, 75000.00),
(1, 2, 'Photography', 2000.00, 4000.00, 75000.00);

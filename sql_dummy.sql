INSERT INTO roomtype(roomtype, residentrate, transientrate, roomextensionrate, maximumoccupants, roomtypedelete)
	VALUES
		('Regular-Twin',42150.00, 2810.00, 225.00, 4, false),
		('Regular-Triple', 52500.00, 3500.00, 225.00, 4, false),
		('Deluxe-Twin', 52500.00, 3500.00, 300.00, 4, false),
		('Presidential',NULL ,20000.00, 2000.00, 6, false);

INSERT INTO room(RoomTypeID, RoomNumber, RoomDelete)
	VALUES
		(4, 200, false),
		(1, 203, false),
		(1, 204, false),
		(1, 205, false),
		(1, 206, false),
		(1, 207, false),
		(2, 208, false),
		(2, 209, false),
		(2, 210, false),
		(2, 211, false),
		(2, 212, false),
		(3, 213, false),
		(3, 214, false),
		(3, 215, false),
		(3, 216, false),
		(3, 217, false);

INSERT INTO discount(discounttype, discountpercentage, discountdelete)
	VALUES
		('Maintenance', 1.00, false),
		('Person With Disabilities', .20, false),
		('UP Alumni', .03, false),
		('Senior Citizen', .20, false);

INSERT INTO groupguest(groupguestname, groupguestdelete)
	VALUES
		('PAP LGBT', false),
		('PACIWU', false),
		('HOLDEN', false);

INSERT INTO guest (Surname, Firstname, Middlename, Address, Mobile, Telephone, Occupation, Nationality, Passport, GuestDelete)
VALUES 
    ('Smith', 'John', 'Parker', '123 Main St, Cityville', '+1 415-555-5555', 'john.smith@example.com', 'Engineer', 'American', 'US123456', false),
    ('Johnson', 'Alice', 'Cooper', '456 Oak St, Townsville', '+1 416-555-5555', 'alice.cooper.johnson@example.com@example.com', 'Doctor', 'Canadian', 'CA789012', false),
    ('Brown', 'Robert', 'Lee', '789 Elm St, Villagetown', '+44 20 7946 0958', ' robert.lee.brown@example.com', 'Teacher', 'British', 'UK345678', false),
    ('Davis', 'Emily', 'Morgan', '101 Pine St, Hamletville', '+61 2 5555 5555', 'emily.morgan.davis@example.com', 'Artist', 'Australian', 'AU901234', false),
    ('Taylor', 'John', 'Duane', '202 Cedar St, Countryside', '+91 98765 43210', 'johnduanetaylor@example.com', 'Lawyer', 'Indian', 'IN567890', false);

INSERT INTO statusname(statusname, statusdescription, statusnamedelete)
	VALUES 
		('Reserved', 'An advanced reservation has been made with no initial deposit', false),
		('Booked', 'A booking has been made with initial deposit', false),
		('Confirmed', 'Guest has arrived in UH and is currently checked-in', false),
		('Cancelled', 'A reservation or booking which has been cancelled', false),
		('Closed', 'A booking with completed payment and front desk transactions', false),
		('Under Repair', 'Room cannot be used', false);

INSERT INTO staff (StaffLastName, StaffFirstName, StaffUsername, StaffPassword, StaffDelete)
VALUES 
    ('Miller', 'Eva', 'evamiller', '6e0daa0a792dcaef24738984267b05c5153663f16fa31a96325ab2fc1ca713b8',false),
    ('Anderson', 'Daniel', 'danielanderson', '5efc2b017da4f7736d192a74dde5891369e0685d4d38f2a455b6fcdab282df9c',false),
    ('Garcia', 'Sophia', 'sophia12', 'f3d63c9346b22494e1dd0aca73a12ed26270ad605bd8ba9824a404334582cf55',false),
    ('Johnson', 'Matthew', 'mattyj','d62fe12c0e3448d785d9ba72de8a3e6cc4d60914f83df062f6c34011d7b02c26', false),
    ('Lee', 'Olivia', 'oliveoil','a62f7c6b5388edf117fd63491912d64916b3835940743a1a14dce6b0de69d611', false);

INSERT INTO ratetype(ratetype, ratetypedelete)
	VALUES
		('Resident',false),
		('Transient', false);
INSERT INTO booking (RoomID, DiscountID, GuestID, StaffID, GroupGuestID, RateTypeID, NumberOfOccupants, CheckInDate, CheckOutDate, ArrivalTime, DepartureTime, BookingDelete)
VALUES 
    (1, 1, 3, 5, 1, 2, 4, '2023-01-01', '2023-01-04', '2023-01-01 14:00:00', '2023-01-04 12:00:00', false),
    (2, 2, 1, 4, 1, 2, 3, '2023-01-01', '2023-01-05', '2023-01-01 14:00:00', '2023-01-05 14:00:00', false),
    (3, NULL, 5, 3, 2, 2, 3, '2023-01-02', '2023-01-14', '2023-01-02 14:00:00', '2023-01-14 15:00:00', false),
    (4, NULL, 4, 2, NULL, 2, 2, '2023-01-03', '2023-01-10', '2023-01-03 12:00:00', '2023-01-10 11:30:00', false),
    (5, 3, 2, 1, NULL, 1, 1, '2023-01-04', '2023-03-20', '2023-01-04 10:00:00', '2023-03-20 15:30:00', false);

INSERT INTO statuschange (bookingid, statusnameid, statuschangedelete)
	VALUES
		(1, 1, false),
		(2, 2, false),
		(3, 4, false),
		(4, 6, false),
		(5, 2, false);

INSERT INTO paymenttype(paymenttype, paymenttypedelete)
	VALUES
		('Initial Deposit', false),
		('Partial', false),
		('Full', false);

INSERT INTO modeofpayment (modeofpayment, modeofpaymentdelete)
	VALUES
		('Cash', false),
		('Cheque', false),
		('E-Wallet', false),
		('Debit Card', false),
		('Credit Card', false);

INSERT INTO payment (GuestID, StaffID, BookingID, PaymentTypeID, ModeOfPaymentID, EarnedRoomFee, DiscountAmount, ExtensionCharges, AdditionalCharges, TotalAmount, Deposit, Balance, PaymentDelete)
VALUES 
    (3, 5, 1, 1, 1, 80000.00, 0.00, 0.00, 0.00, 80000.00,40000.00,40000.00, false),
    (1, 4, 2, 2, 3, 14050.00, 2810.00, 450.00, 100.00, 11790.00,8000.00,3790.00, false),
    (4, 2, 4, 3, 5, 22480.00, 0.00, 450.00, 1200.00, 24130.00,24130.00, 0.00, false),
    (2, 1, 5, 1, 4, 84300.00, 2529.00, 1575.00, 300.00, 83646.00,42150.00, 41496.00, false),
    (5, 3, 3, 2, 2, 36530.00, 0.00, 675.00, 40.00, 37245.00,19000.00, 18245.00, false);

Create Table roomtype (
	RoomTypeID serial primary key not null,
	RoomType varchar(128),
	ResidentRate decimal(10,2),
	TransientRate decimal(10,2),
	RoomExtensionRate decimal(10,2),
	MaximumOccupants int,
	RoomTypeDelete bool
);

Create Table room (
	RoomID serial primary key not null,
	RoomTypeID int,
	RoomNumber varchar(70) unique,
	RoomDelete bool,
	CONSTRAINT fk_roomtype
		FOREIGN KEY (RoomTypeID)
		REFERENCES roomtype(RoomTypeId)
);

Create Table discount (
	DiscountID serial primary key not null,
	DiscountType varchar(128),
	DiscountPercentage decimal(5,2),
	DiscountDelete bool
);

Create Table groupguest (
	GroupGuestID serial primary key not null,
	GroupGuestName varchar(128),
	GroupGuestDelete bool
);

Create Table guest (
	GuestID serial primary key not null,
	Surname varchar(255),
	Firstname varchar(255),
	Middlename varchar(255),
	Address varchar,
	Mobile varchar(20),
	Email varchar(255),
	Occupation varchar(70),
	Nationality varchar(70),
	Passport varchar(70),
	GuestDelete bool
);

Create Table statusname  (
	StatusNameID serial primary key not null,
	StatusName varchar(128),
	StatusDescription varchar,
	StatusNameDelete bool
);

Create Table staff  (
	StaffID serial primary key not null,
	StaffLastName varchar(128),
	StaffFirstName varchar(128),
	StaffUserName varchar(32) unique,
	StaffPassword varchar,
	StaffModifiedDate Timestamp without time zone default now(),
	StaffActive bool default false,
	StaffDelete bool default false,
	StaffAccess bool default false,
);

Create Table ratetype(
	RateTypeID serial primary key not null,
	RateType Varchar(70),
	RateTypeDelete bool
);

CREATE TABLE booking (
    BookingID SERIAL PRIMARY KEY NOT NULL,
    RoomID INT,
    DiscountID INT,
    GuestID INT,
    StaffID INT,
    GroupGuestID INT,
    RateTypeID INT,
    NumberOfOccupants INT,
    CheckInDate DATE,
    CheckOutDate DATE,
    ArrivalTime TIMESTAMP WITHOUT TIME ZONE,
    DepartureTime TIMESTAMP WITHOUT TIME ZONE,
    DaysDuration INT,
    MonthsDuration INT,
    HourExtension INT,
    BookingModifiedDate TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    BookingDelete BOOLEAN,
    CONSTRAINT fk_room
		FOREIGN KEY (RoomID)
		REFERENCES Room(RoomID),
    CONSTRAINT fk_discount 
		FOREIGN KEY (DiscountID) 
		REFERENCES Discount(DiscountID),
    CONSTRAINT fk_guest 
		FOREIGN KEY (GuestID) 
		REFERENCES Guest(GuestID),
    CONSTRAINT fk_staff 
		FOREIGN KEY (StaffID) 
		REFERENCES Staff(StaffID),
    CONSTRAINT fk_groupguest 
		FOREIGN KEY (GroupGuestID) 
		REFERENCES GroupGuest(GroupGuestID),
	CONSTRAINT fk_ratetype
		FOREIGN KEY (ratetypeid)
		REFERENCES ratetype(ratetypeid)
);

CREATE OR REPLACE FUNCTION update_booking_duration()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.ArrivalTime < (NEW.ArrivalTime::date + INTERVAL '14 hours') THEN
        NEW.HourExtension := EXTRACT(HOUR FROM NEW.ArrivalTime::date + INTERVAL '14 hours' - NEW.ArrivalTime);
    ELSE
        NEW.HourExtension := 0;
    END IF;

    IF NEW.DepartureTime > (NEW.DepartureTime::date + INTERVAL '12 hours') THEN
        NEW.HourExtension := NEW.HourExtension + EXTRACT(HOUR FROM NEW.DepartureTime - (NEW.DepartureTime::date + INTERVAL '12 hours'));
    END IF;

    NEW.daysduration := EXTRACT(DAY FROM AGE(NEW.CheckOutDate, NEW.CheckInDate)) - 1;

    NEW.monthsduration := EXTRACT(MONTH FROM AGE(NEW.CheckOutDate, NEW.CheckInDate)) +
                          EXTRACT(YEAR FROM AGE(NEW.CheckOutDate, NEW.CheckInDate)) * 12;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_booking_duration
BEFORE INSERT OR UPDATE ON booking
FOR EACH ROW
EXECUTE FUNCTION update_booking_duration();

Create Table statuschange(
	StatusChangeID serial primary key not null,
	BookingID int,
	StatusNameID int,
	StatusModifiedDate Timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
	StatusChangeDelete bool,
	CONSTRAINT fk_booking
		FOREIGN KEY (BookingID)
		REFERENCES booking(bookingid),
	CONSTRAINT fk_statusname
		FOREIGN KEY (statusnameid)
		REFERENCES statusname(statusnameid)
);

Create Table paymenttype(
	PaymentTypeID serial primary key not null,
	PaymentType varchar(70),
	PaymentTypeDelete bool
);

Create Table modeofpayment(
	ModeOfPaymentID serial primary key not null,
	ModeOfPayment varchar(70),
	ModeOfPaymentDelete bool
);

CREATE TABLE payment (
    PaymentID serial primary key not null,
    GuestID int,
    StaffID int,
    BookingID int,
    PaymentTypeID int,
    ModeOfPaymentID int,
    EarnedRoomFee decimal(10,2),
    DiscountAmount decimal(10,2),
    ExtensionCharges decimal(10,2),
    AdditionalCharges decimal(10,2),
    TotalAmount decimal(10,2),
    Deposit decimal(10,2),
    Balance decimal(10,2),
    PaymentModifiedDate Timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    PaymentDelete bool,
    CONSTRAINT fk_guest
        FOREIGN KEY (guestid) REFERENCES guest(guestid),  
    CONSTRAINT fk_staff
        FOREIGN KEY (staffid) REFERENCES staff(staffid),
    CONSTRAINT fk_booking
        FOREIGN KEY (bookingid) REFERENCES booking(bookingid),
    CONSTRAINT fk_paymenttype
        FOREIGN KEY (paymenttypeid) REFERENCES paymenttype(paymenttypeid),
    CONSTRAINT fk_modeofpayment
        FOREIGN KEY (modeofpaymentid) REFERENCES modeofpayment(modeofpaymentid),
  );

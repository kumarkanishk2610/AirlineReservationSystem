import sqlite3
import random
import string
from faker import Faker
import datetime
import time
import os

os.system('cls')
start_time = time.time()
fake = Faker('en_IN')
conn = sqlite3.connect('skyvoyage.db')
cursor = conn.cursor()

cursor.execute  ('''CREATE TABLE IF NOT EXISTS Passenger (
                    PNR varchar(7) primary key,
                    Salutation varchar(4) NOT NULL,
                    FirstName varchar(16) NOT NULL,
                    LastName varchar(16),
                    MobileNo number(10),
                    email varchar(50),
                    IDCardType varchar(20) NOT NULL,
                    IDCardValue varchar(20) NOT NULL,
                    FL_NO varchar(7) NOT NULL,
                    SRC varchar(3) NOT NULL,
                    DST varchar(3) NOT NULL,
                    DepDt Date NOT NULL,
                    BoardingTime Time NOT NULL,
                    DepTime Time NOT NULL,
                    ArrDt Date NOT NULL,
                    ArrTime Time NOT NULL,
                    Duration Time NOT NULL,
                    Price number(10) NOT NULL,
                    BookingClass varchar(16) NOT NULL,
                    BoardingZone varchar(5) NOT NULL,
                    SeatNumber varchar(10) NOT NULL,
                    GateNumber varchar(5) NOT NULL,
                    SeqNo int NOT NULL,
                    MealPreference varchar(20),
                    SpecialAssistance varchar(20),
                    CheckIn varchar(16),
                    UNIQUE (FL_NO, SeatNumber)
                )''')

# Function to generate random data for passengers
def generate_passenger_data(num):
    def generate_salutation(gender):
        if gender == 'male':
            return random.choice(["Mr.", "Dr."])
        elif gender == 'female':
            return random.choice(["Mrs.", "Ms.", "Dr."])
    # Function to generate Aadhaar card number
    
    def generate_aadhaar():
        return ''.join(random.choices(string.digits, k=12))
    
    # Function to generate PAN card number
    def generate_pan():
        return ''.join(random.choices(string.ascii_uppercase, k=5)) + ''.join(random.choices(string.digits, k=4)) + random.choice(string.ascii_uppercase)
    
    # Function to generate passport number
    def generate_passport():
        return ''.join(random.choices(string.ascii_uppercase, k=1)) + ''.join(random.choices(string.digits, k=2)) + ' ' + ''.join(random.choices(string.digits,     k=4)) + ''.join(random.choices(string.digits, k=1))
    
    # Function to generate driving license number
    def generate_driving_license():
        state_code = ''.join(random.choices(string.ascii_uppercase, k=2))
        city_code = ''.join(random.choices(string.digits, k=2))
        issue_year = ''.join(random.choices(string.digits, k=4))
        unique_id = ''.join(random.choices(string.digits, k=7))
        return f"{state_code}-{city_code}-{issue_year}-{unique_id}"
    
    # Function to generate ID card value based on type
    def generate_id_card_value(id_card_type):
        if id_card_type == "Aadhaar Card":
            return generate_aadhaar()
        elif id_card_type == "PAN Card":
            return generate_pan()
        elif id_card_type == "Passport":
            return generate_passport()
        elif id_card_type == "Driving License":
            return generate_driving_license()
        else:
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
    def generate_unique_seat_number(cursor, fl_no):
        while True:
            seat_number = f"{random.randint(1, 31)}{random.choice('ABCDEF')}"
            cursor.execute("SELECT COUNT(*) FROM Passenger WHERE FL_NO=? AND SeatNumber=?", (fl_no, seat_number))
            count = cursor.fetchone()[0]
            if count == 0:
                return seat_number
    
    cursor.execute("SELECT COUNT(*) FROM Passenger")
    current_entries = cursor.fetchone()[0]
    remaining_entries = num - current_entries
    counter = 0
    try:
        for i in range(remaining_entries):
            pnr = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
            gender = random.choice(['male', 'female'])
            salutation = generate_salutation(gender)
            first_name = fake.first_name_male() if gender == 'male' else fake.first_name_female()
            last_name = fake.last_name()
            mobile_no = random.choice([6, 7, 8, 9]) * 10**9 + random.randint(10**8, 10**9 - 1)
            email = fake.email()
            id_card_type = random.choice(["Aadhaar Card", "PAN Card", "Passport", "Driving License", "Voter ID", "Student ID", "Employee ID"])
            id_card_value = generate_id_card_value(id_card_type)
            # Fetch FL_NO from flights table
            cursor.execute("SELECT FL_NO FROM Flights ORDER BY RANDOM() LIMIT 1")
            fl_no = cursor.fetchone()[0]
            # Fetch other flight details based on FL_NO
            cursor.execute("SELECT SRC, DST, DepDt, DepTime, ArrDt, ArrTime, Duration, Price, BookingClass FROM Flights WHERE FL_NO=?", (fl_no,))
            src, dst, dep_dt, dep_time, arr_dt, arr_time, duration, price, booking_class = cursor.fetchone()

            dep_time = datetime.datetime.strptime(dep_time, '%H:%M')  # Assuming dep_time is in HH:MM format

            # Calculate boarding time
            boarding_time = dep_time - datetime.timedelta(minutes=30)
            boarding_time = boarding_time.strftime("%H:%M")
            dep_time = dep_time.strftime("%H:%M")

            #boarding_time = dep_time - 30  # Assuming dep_time is in minutes format
            boarding_zone = "Zone " + str(random.randint(1, 4))
            #seat_number = f"{random.randint(1, 31)}{random.choice('ABCDEF')}"  # Assuming seat numbers are from 1A to 31F
            seat_number = generate_unique_seat_number(cursor, fl_no)
            gate_number = random.randint(1, 150)
            seq_no = random.randint(1, 200)
            meal_preference = random.choice(["No Meal", "Veg", "Non Veg", "Any"])
            special_assistance = random.choices(["Not Required", "Speech Impaired", "Visually Impaired", "Hearing Impaired", "Wheelchair Assistance"], weights=[99,     1, 1, 1, 1])[0]
            check_in = "Not Completed"

            cursor.execute('''INSERT INTO Passenger (PNR, Salutation, FirstName, LastName, MobileNo, email, IDCardType, IDCardValue, FL_NO, SRC, DST, DepDt,    BoardingTime, DepTime, ArrDt, ArrTime, Duration, Price, BookingClass, BoardingZone, SeatNumber, GateNumber, SeqNo, MealPreference, SpecialAssistance,  CheckIn) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (pnr, salutation, first_name, last_name, mobile_no, email, id_card_type, id_card_value, fl_no, src, dst, dep_dt, boarding_time, dep_time,    arr_dt, arr_time, duration, price, booking_class, boarding_zone, seat_number, gate_number, seq_no, meal_preference, special_assistance,    check_in))


            counter+=1
            if (counter==67):
                counter=0
                conn.commit()
                elapsed_time = time.time() - start_time
                avg_time_per_entry = elapsed_time / (i + 1) if i != 0 else 0
                remaining_time = avg_time_per_entry * (remaining_entries-i)
                hours = int(remaining_time) // 3600
                minutes = int((remaining_time % 3600) // 60)
                seconds = int(remaining_time % 60)

                print(f"\t{current_entries + i}/{num} entries generated. Estimated time left: {hours:02d}:{minutes:02d}:{seconds:02d}", end='\r')
    except KeyboardInterrupt:
        print("\n\tGeneration interrupted by user. Exiting...")
    conn.commit()
    conn.close()
    print("\tGeneration Completed Successfully!")
        
# Generate 1,000,000 entries
num=8388608
generate_passenger_data(num)
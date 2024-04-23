import sqlite3
from datetime import datetime, timedelta
import random
from faker import Faker
from tabulate import tabulate
from tkcalendar import Calendar
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import time
import os
import string
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
from tkinter.scrolledtext import ScrolledText

conn = sqlite3.connect('skyvoyage.db')
cursor = conn.cursor()

#cursor.execute("drop table flights")
cursor.execute('''
                CREATE TABLE IF NOT EXISTS Flights(
                Airline varchar(24),
                FL_NO varchar2(7) primary key,
                SRC varchar2(3),
                DST varchar2(3),
                DepDt Date,
                DepTime Time,
                ArrDt Date,
                ArrTime Time,
                Duration Time,
                Price number(10),
                FlightStatus varchar2(8),
                AvailableSeats number(4),
                BookingClass varchar2(16)
               )
               ''')
print("Flight Table Created Successsfully.")


airlines = {
    'AI ': 'Air India',
    'AXB': 'Air India Express',
    'IAD': 'AIX Connect',
    'AKJ': 'Akasa Air',
    '6E ': 'Indigo',
    'SG ': 'SpiceJet',
    'UK ': 'Vistara'
}
cabin_config = {
    'Boeing 737': '3+3',
    'Boeing 747': '3+4+3',
    'Boeing 787': '3+3+3',
    'Airbus A320neo': '3+3',
    'Airbus A321neo': '3+3',
    'Airbus A320': '3+3'
}

# Function to generate random FL_NO
def generate_flight_number():
    airline_code = random.choice(list(airlines.keys()))
    return airline_code + str(random.randint(100, 9999))

# Function to generate random airport code
def generate_minor_airport_code(cursor):
    # Fetch all airport codes from the Airports table
    cursor.execute ("SELECT AirportCode FROM Airports WHERE Traffic<7")
    airport_codes = cursor.fetchall()
    return random.choice(airport_codes)[0]

def generate_major_airport_code(cursor):
    # Fetch all airport codes from the Airports table
    cursor.execute("SELECT AirportCode FROM Airports WHERE Traffic>=7")
    airport_codes = cursor.fetchall()
    return random.choice(airport_codes)[0]

# Function to generate random date and time within April-May 2024
def generate_datetime():
    start_date = datetime(2024, 4, 1)
    end_date = datetime(2024, 5, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# Function to generate random flight status
def generate_flight_status():
    return random.choice(['ON TIME', 'DELAYED', 'CANCELLED'])

# Function to generate random price
def generate_price():
    return random.randint(2000, 17000)

# Function to generate random available seats
def generate_available_seats():
    return random.randint(100, 100)

# Function to generate random booking class
def generate_booking_class():
    return random.choice(['Economy', 'Business', 'First'])

def generate_time():
    hour = random.randint(0, 23)
    minute = random.randint(0, 11) * 5  # Generate minutes in multiples of 5
    return f"{hour:02d}:{minute:02d}"

def generate_duration():
    hours = random.randint(0, 3)  # Random hours between 0 and 3
    minutes = random.randint(0, 11) * 5  # Random minutes in multiples of 5
    return timedelta(hours=hours, minutes=minutes)

# Generate random entries
n = 69000  # Number of entries to generate
#for _ in range(n):
while True:
    cursor.execute("SELECT COUNT(*) FROM Flights")
    num_flights = cursor.fetchone()[0]
    if num_flights < 69300:
        # Your code to generate flights goes here
        while True:
            FL_NO = generate_flight_number().strip(' ')  # Generate a flight number and remove whitespaces
            cursor.execute('''SELECT FL_NO FROM Flights WHERE FL_NO = ?''', (FL_NO,))
            existing_fl_no = cursor.fetchone()
            if existing_fl_no is None:  # Check if the generated flight number doesn't exist
                break
            else:
                print(f"Duplicate flight number generated: {FL_NO}. Regenerating...")

        Airline = airlines.get(FL_NO[:3])  # Use .get() to handle potential KeyError
        if Airline is None:
            print(f"Invalid airline code in FL_NO: {FL_NO[:2]}")
            print(f"Generated FL_NO: {FL_NO}")
            continue
        print(f"Generated FL_NO: {FL_NO}, Airline: {Airline}")  # Print generated flight number and airline

        # Generate SRC and DST ensuring they are not the same
        while True:
            weightskew=random.randint(1, 10)
            if weightskew>=8:
                weighttype=["MajorMajor"]
                SRC = generate_major_airport_code(cursor)
                DST = generate_major_airport_code(cursor)

            else:
                weighttype=random.choice(["minorMajor","Majorminor"])
                if weighttype=="minorMajor":
                    SRC = generate_minor_airport_code(cursor)
                    DST = generate_major_airport_code(cursor)

                if weighttype=="Majorminor":
                    SRC = generate_major_airport_code(cursor)
                    DST = generate_minor_airport_code(cursor)

            if SRC != DST:  # Check if SRC is different from DST
                break
            else:
                print("SRC is the same as DST. Regenerating DST...")

        DepDt = generate_datetime().date()
        DepTime = generate_time()  # Use generate_time function to generate random time

        # Generate random duration in minutes
        duration_minutes = generate_duration().total_seconds() // 60

        # Calculate arrival date and time
        ArrDt = DepDt
        ArrTime = (datetime.strptime(DepTime, '%H:%M') + timedelta(minutes=duration_minutes)).strftime('%H:%M')  # Corrected format to '%H:%M'

        # Adjust arrival date and time if exceeds 24-hour format
        if ArrTime >= '24:00':
            ArrDt += timedelta(days=1)
            ArrTime = (datetime.strptime(ArrTime, '%H:%M') - timedelta(hours=24)).strftime('%H:%M')

        # Check if arrival time crosses 00:00 barrier and adjust arrival date accordingly
        if datetime.strptime(ArrTime, '%H:%M') < datetime.strptime(DepTime, '%H:%M'):
            ArrDt += timedelta(days=1)

        # Format duration as HH:MM
        Duration = "{:02d}:{:02d}".format(int(duration_minutes // 60), int(duration_minutes % 60))

        #AircraftName = random.choice(['Boeing 737', 'Boeing 747', 'Boeing 787', 'Airbus A320neo', 'Airbus A321neo', 'Airbus A320'])
        FlightStatus = generate_flight_status()
        Price = generate_price()
        AvailableSeats = generate_available_seats()
        BookingClass = generate_booking_class()
        #CabinCfg = cabin_config[AircraftName]

        # Insert into database
        cursor.execute('''INSERT INTO Flights VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (Airline, FL_NO, SRC, DST, DepDt, DepTime, ArrDt, ArrTime, Duration, Price, FlightStatus, AvailableSeats, BookingClass))
        #, AircraftName, CabinCfg
        #, ?, ?
    else:
        print("Random entries inserted successfully.")
        conn.commit()
        print("Committed Successfully.")
        break
    
conn.commit()
conn.close()
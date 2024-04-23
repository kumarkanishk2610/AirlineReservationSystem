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

airport_data = [
    ('Ahmedabad', 'AMD', '7'),
    ('Bengaluru', 'BLR', '10'),
    ('Chennai', 'MAA', '9'),
    ('Delhi', 'DEL', '10'),
    ('Guwahati', 'GAU', '7'),
    ('Hyderabad', 'HYD', '8'),
    ('Kolkata', 'CCU', '9'),
    ('Mumbai', 'BOM', '10'),
    
    
    ('Agartala', 'IXA', '4'),
    ('Agra', 'AGR', '4'),
    ('Aizawl', 'AJL', '2'),
    ('Amritsar', 'ATQ', '5'),
    ('Aurangabad', 'IXU', '3'),
    ('Bagdogra', 'IXB', '2'),
    ('Bareilly', 'BEK', '1'),
    ('Belagavi', 'IXG', '1'),
    ('Bhopal', 'BHO', '4'),
    ('Bhubaneswar', 'BBI', '6'),
    ('Chandigarh', 'IXC', '6'),
    ('Coimbatore', 'CJB', '6'),
    ('Darbhanga', 'DBR', '1'),
    ('Dehradun', 'DED', '3'),
    ('Deoghar', 'DGH', '2'),
    ('Dibrugarh', 'DIB', '3'),
    ('Dimapur', 'DMU', '2'),
    ('Durgapur', 'RDP', '4'),
    ('Gaya', 'GAY', '3'),
    ('Goa', 'GOI', '6'),
    ('Gorakhpur', 'GOP', '1'),
    ('Gwalior', 'GWL', '3'),
    ('Hubli', 'HBX', '2'),
    ('Imphal', 'IMF', '2'),
    ('Indore', 'IDR', '4'),
    ('Itanagar', 'HGI', '2'),
    ('Jabalpur', 'JLR', '2'),
    ('Jaipur', 'JAI', '5'),
    ('Jammu', 'IXJ', '4'),
    ('Jodhpur', 'JDH', '4'),
    ('Jorhat', 'JRH', '1'),
    ('Kadapa', 'CDP', '1'),
    ('Kannur', 'CNN', '2'),
    ('Kanpur', 'KNU', '3'),
    ('Kochi', 'COK', '3'),
    ('Kolhapur', 'KLH', '2'),
    ('Kozhikode', 'CCJ', '2'),
    ('Kurnool', 'KJB', '2'),
    ('Leh', 'IXL', '2'),
    ('Lucknow', 'LKO', '5'),
    ('Madurai', 'IXM', '4'),
    ('Mangaluru', 'IXE', '4'),
    ('Mysuru', 'MYQ', '6'),
    ('Nagpur', 'NAG', '3'),
    ('North Goa', 'GOX', '1'),
    ('Pantnagar', 'PGH', '1'),
    ('Patna', 'PAT', '4'),
    ('Port-Blair', 'IXZ', '1'),
    ('Prayagraj', 'IXD', '2'),
    ('Pune', 'PNQ', '5'),
    ('Raipur', 'RPR', '2'),
    ('Rajahmundry', 'RJA', '1'),
    ('Rajkot', 'RAJ', '2'),
    ('Ranchi', 'IXR', '2'),
    ('Shillong', 'SHL', '3'),
    ('Shirdi', 'SAG', '1'),
    ('Silchar', 'IXS', '2'),
    ('Srinagar', 'SXR', '3'),
    ('Surat', 'STV', '3'),
    ('Thiruvananthapuram', 'TRV', '3'),
    ('Tiruchirappalli', 'TRZ', '1'),
    ('Tirupati', 'TIR', '1'),
    ('Tuticorin', 'TCR', '1'),
    ('Udaipur', 'UDR', '3'),
    ('Vadodara', 'BDQ', '2'),
    ('Varanasi', 'VNS', '4'),
    ('Vijayawada', 'VGA', '2'),
    ('Visakhapatnam', 'VTZ', '2')
]

cursor.execute('''CREATE TABLE IF NOT EXISTS Airports (
                    AirportName VARCHAR(100),
                    AirportCode VARCHAR(3) PRIMARY KEY,
                    Traffic number(2)
                )''')

for airport_info in airport_data:
    cursor.execute('''
        INSERT INTO Airports (AirportName, AirportCode, Traffic)
        SELECT ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM Airports WHERE AirportCode = ?
        );
    ''', (*airport_info, airport_info[1]))


print("Airport data added successfully.")
conn.commit()
conn.close()
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
import hashlib

conn = sqlite3.connect('skyvoyage.db')
cursor = conn.cursor()


global LoginStatus
LoginStatus = False

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        full_name TEXT NOT NULL,
        security_question TEXT,
        security_answer TEXT,
        privileges TEXT
    )
''')

def hasher(keyword):
    # Convert the password to bytes before hashing
    utf_bytes = keyword.encode('utf-8')

    # Choose a hashing algorithm (e.g., SHA-256)
    hash_algorithm = hashlib.sha256()

    # Update the hash object with the password bytes
    hash_algorithm.update(utf_bytes)

    # Get the hashed password in hexadecimal format
    hashed_keyword = hash_algorithm.hexdigest()

    return hashed_keyword

def parse_flight_data(data):
    """
    Parse the flight data into a list of dictionaries.
    """
    flight_list = []
    for flight_info in data:
        flight_dict = {
            "Airline": flight_info[0],
            "Flight No.": flight_info[1],
            "Source": flight_info[2],
            "Destination": flight_info[3],
            "Departure Date": flight_info[4],
            "Departure Time": flight_info[5],
            "Arrival Date": flight_info[6],
            "Arrival Time": flight_info[7],
            "Duration": flight_info[8],
            "Price": '₹' + str(flight_info[9]),
            #"Flight Status": flight_info[10],
            "Available Seats": flight_info[11],
            "Booking Class": flight_info[12],
            #"Aircraft Name": flight_info[13],
            #"Cabin Configuration": flight_info[14]
        }
        flight_list.append(flight_dict)
    return flight_list

def display_flight_table(parent, flight_data):
    """
    Create and display the flight table in the specified parent widget.
    """
    # Create the treeview widget
    for widget in search_output_frame.winfo_children():
        widget.destroy()
    global tree
    tree = ttk.Treeview(parent)

    try:
        columns = list(flight_data[0].keys())
        tree["columns"] = tuple(columns)
        tree.heading("#0", text="")
        for column in columns:
            tree.heading(column, text=column)
    except IndexError:
        # Handle the case when flight_data is not in the expected format
        print("Flight Table list index error encountered. Ignoring.")

    # Set column widths
    column_widths = {
        "#0": 0,
        "Airline": 150,
        "Flight No.": 100,
        "Source": 70,
        "Destination": 70,
        "Departure Date": 100,
        "Departure Time": 100,
        "Arrival Date": 100,
        "Arrival Time": 100,
        "Duration": 70,
        "Price": 70,
        #"Flight Status": 100,
        "Available Seats": 70,
        "Booking Class": 100,
        #"Aircraft Name": 150,
        #"Cabin Configuration": 150
    }
    for column, width in column_widths.items():
        tree.column(column, width=width)

    # Insert data rows
    for i, flight in enumerate(flight_data, start=1):
        tree.insert("", "end", values=tuple(flight.values()))

    # Pack the treeview widget
    tree.pack(fill="both", expand=True)
    book_button = tk.Button(search_output_frame, text="Select Flight", font=("Helvetica", 12), command=book_flight, bg="#3498db", fg="white", bd=0, relief=tk.FLAT)
    book_button.pack(pady=(10,50))
    #book_button.grid(row=8, columnspan=2, pady=(10, 0), padx=10, sticky="ew")
    

def book_flight():
    # Get the selected flight number
    selected_item = tree.selection()[0]
    flight_number = tree.item(selected_item, option="values")[1]
    # Print selected flight number
    print("Flight Number:", flight_number)

    # Retrieve selected flight details from the database
    cursor.execute('''
        SELECT * FROM Flights WHERE FL_NO = ?
        ''', (flight_number,))
    selected_flight = cursor.fetchone()

    # Destroy any existing widgets in the search_output_frame
    for widget in search_output_frame.winfo_children():
        widget.destroy()

    # Create a frame to contain all the labels
    booking_details_frame = tk.Frame(search_output_frame)
    booking_details_frame.pack(side="top", anchor="nw", pady=10)

    # Create labels to display flight data inside the booking_details_frame
    booking_itinerary_label = tk.Label(booking_details_frame, text="Your Itinerary:", font=("Helvetica", 12))
    booking_itinerary_label.pack(anchor="nw")
    
    booking_flight_number_label = tk.Label(booking_details_frame, text="\tFlight Number: "+ selected_flight[0] + " - " + selected_flight[1], font=("Helvetica", 12))
    booking_flight_number_label.pack(anchor="nw")
    
    booking_source_label = tk.Label(booking_details_frame, text="\tSource: " + selected_flight[2], font=("Helvetica", 12))
    booking_source_label.pack(anchor="nw")
    
    booking_destination_label = tk.Label(booking_details_frame, text="\tDestination: " + selected_flight[3], font=("Helvetica", 12))
    booking_destination_label.pack(anchor="nw")
    
    booking_departure_label = tk.Label(booking_details_frame, text="\tDeparture:" + selected_flight[5] + ", " + selected_flight[4], font=("Helvetica", 12))
    booking_departure_label.pack(anchor="nw")
    
    booking_arrival_label = tk.Label(booking_details_frame, text="\tArrival: " + selected_flight[7] + ", " + selected_flight[6], font=("Helvetica", 12))
    booking_arrival_label.pack(anchor="nw")
    
    booking_duration_label = tk.Label(booking_details_frame, text="\tDuration: " + selected_flight[8], font=("Helvetica", 12))
    booking_duration_label.pack(anchor="nw")
    
    booking_price_label = tk.Label(booking_details_frame, text="\tPrice: Rs. " + str(selected_flight[9]), font=("Helvetica", 12))
    booking_price_label.pack(anchor="nw")
    
    booking_available_seats_label = tk.Label(booking_details_frame, text="\tAvailable Seats: " + str(selected_flight[11]), font=("Helvetica", 12))
    booking_available_seats_label.pack(anchor="nw")
    

    # Frame for the input fields
    input_frame = tk.Frame(search_output_frame)
    input_frame.pack(side="top", anchor="nw", pady=5)

    # Frame for the combobox and entry boxes
    entry_frame = tk.Frame(search_output_frame)
    entry_frame.pack(side="top", anchor="nw", pady=5)


    # Salutation Label
    salutation_label = tk.Label(input_frame, text="Salutation:")
    salutation_label.pack(side="left", padx=(0, 5))

    # First Name Label
    first_name_label = tk.Label(input_frame, text="First Name:")
    first_name_label.pack(side="left", padx=(0, 5))

    # Last Name Label
    last_name_label = tk.Label(input_frame, text="\t      Last Name:")
    last_name_label.pack(side="left", padx=(0, 5))    # Last Name Label

    #id card Label
    id_card_type_label = tk.Label(input_frame, text="ID Card Type:")
    id_card_type_label.pack(side="left", padx=(75, 5))

    id_card_label = tk.Label(input_frame, text="Card Number:")
    id_card_label.pack(side="left", padx=(22, 5))



    
    # Salutation Combobox
    salutation_combo = ttk.Combobox(entry_frame, values=["Mr.", "Ms.", "Mrs.", "Dr."], width=5)
    salutation_combo.pack(side="left", padx=(5, 10))

    # First Name Entry
    first_name_entry = tk.Entry(entry_frame)
    first_name_entry.pack(side="left", padx=(0, 15))

    # Last Name Entry
    last_name_entry = tk.Entry(entry_frame)
    last_name_entry.pack(side="left", padx=(0, 20))

    #id card entry
    id_card_type_combo = ttk.Combobox(entry_frame, values=["Aadhaar Card", "PAN Card", "Passport", "Driving License", "Voter ID", "Student ID", "Employee ID", "Other"], width=12)
    id_card_type_combo.pack(side="left", padx=(0, 10))
    
    id_card_entry = tk.Entry(entry_frame)
    id_card_entry.pack(side="left", padx=(0, 20))
    


    # Frame for the input fields
    input_frame2 = tk.Frame(search_output_frame)
    input_frame2.pack(side="top", anchor="nw", pady=5)

    # Frame for the combobox and entry boxes
    entry_frame2 = tk.Frame(search_output_frame)
    entry_frame2.pack(side="top", anchor="nw", pady=5)


    # Meal Preference
    meal_label = tk.Label(input_frame2, text="Meal Preference:")
    meal_label.pack(side="left", padx=(0, 5))

    # Meal Preference Combobox
    meal_combo = ttk.Combobox(entry_frame2, values=["No Meal", "Veg", "Non Veg", "Any"], width=10)
    meal_combo.pack(side="left", padx=(5, 10))

    special_assistance_label = tk.Label(input_frame2, text="Special Assistance:")
    special_assistance_label.pack(side="left", padx=(0, 5))

    # Meal Preference Combobox
    special_assistance_combo = ttk.Combobox(entry_frame2, values=["Not Required", "Speech Impaired", "Hearing Impaired", "Visually Impaired", "Wheelchair Assistance", "Unaccompanied Minor"], width=20)
    special_assistance_combo.pack(side="left", padx=(5, 10))

    mobileno_label = tk.Label(input_frame2, text="Mobile Number:")
    mobileno_label.pack(side="left", padx=(45, 5))

    mobileno_entry = tk.Entry(entry_frame2)
    mobileno_entry.pack(side="left", padx=(0, 20))

    
    email_label = tk.Label(input_frame2, text="Email Address:")
    email_label.pack(side="left", padx=(45, 5))

    email_entry = tk.Entry(entry_frame2)
    email_entry.pack(side="left", padx=(0, 20))
    
    
    cursor.execute("SELECT SeatNumber FROM Passenger WHERE FL_NO = ?", (flight_number,))
    reserved_seats = [seat[0] for seat in cursor.fetchall()]
    
    
    # implement seat selection part here
    seat_selection_frame = tk.Frame(search_output_frame)
    #seat_selection_frame.config(bg="black")
    seat_selection_frame.pack(side="left", anchor="nw", pady=10)
    

    # Create the seat selection interface inside seat_selection_frame
    global seat_selection_label
    seat_selection_label = tk.Label(seat_selection_frame, text="Select Your Seat:", font=("Helvetica", 12))
    seat_selection_label.pack(anchor="nw")


    # Load the seat icon image
    seat_icon = tk.PhotoImage(file="seat_icon.png")
    # Create a nested loop to generate seat buttons
    for col in range(1, 32):  # Change range to 31 for columns
        col_frame = tk.Frame(seat_selection_frame)  # Create a frame for each column
        col_frame.pack(side=tk.LEFT)  # Pack column frames vertically

        for rowx, seat_label in enumerate(['F', 'E', 'D', '', 'C', 'B', 'A']):  # Insert an empty string for the blank line
            if seat_label == '':  # Add padding for the blank line
                tk.Label(col_frame, text=' ', width=4, height=1).pack(side=tk.TOP, padx=2, pady=10)
            else:
                seat = f"{col}{seat_label}"  # Increment row number by 1
                if seat not in reserved_seats:
                    command = lambda s=seat: select_seat(flight_number, s)
                    state = "normal"
                else:
                    command = None
                    state = "disabled"
                button = tk.Button(col_frame, image=seat_icon, compound="center",
                                   width=40, height=40, state=state, command=command,
                                   borderwidth=0, highlightthickness=0)
                button.image = seat_icon  # Keep a reference to the image to prevent garbage collection
                button.pack(side=tk.TOP, padx=2, pady=2)  # Pack buttons within column frames
                button.config(text=seat+"  ")  # Set the seat label as text on the button, overlapping the image

                # Bind the button to a function that changes its background color when clicked
                #button.bind("<Button-1>", lambda event, b=button: button.config(bg="yellow"))
                
    
    passenger_data={}
    confirm_book_button = tk.Button(search_output_frame, text="Book Flight", font=("Helvetica", 12), command=lambda: confirm_booking(), bg="#3498db", fg="white", bd=0, relief=tk.FLAT)
    confirm_book_button.pack(side=tk.BOTTOM, pady=(0,50))

    
    


    def select_seat(flight_number, s):
        seat_selection_label.config(text=f"Select Your Seat: {s}")
        global selectedseat
        selectedseat = s

    def confirm_booking():
        cursor.execute("SELECT SRC, DST, DepDt, DepTime, ArrDt, ArrTime, Duration, Price, BookingClass FROM Flights WHERE FL_NO = ?", (flight_number,))
        flight_data = cursor.fetchone()

        #dep_time_obj = datetime.strptime(book_DepTime, "%H:%M")
        #boarding_time_obj = dep_time_obj - timedelta(minutes=30)
        #book_BoardingTime = boarding_time_obj.strftime("%H:%M:%S")

        passenger_data =    {
                                "PNR": ''.join(random.choices(string.ascii_uppercase + string.digits, k=7)),
                                "Salutation": salutation_combo.get(),
                                "FirstName": first_name_entry.get(),
                                "LastName": last_name_entry.get(),
                                "IDCardType": id_card_type_combo.get(),
                                "IDCardValue": id_card_entry.get(),
                                "FL_NO": selected_flight,
                                "SRC": flight_data[0],
                                "DST": flight_data[1],
                                "DepDt": flight_data[2],
                                "BoardingTime": (datetime.strptime(flight_data[3], "%H:%M") - timedelta(minutes=30)).strftime("%H:%M:%S"),
                                "DepTime": flight_data[3],
                                "ArrDt": flight_data[4],
                                "ArrTime": flight_data[5],
                                "Duration": flight_data[6],
                                "Price": flight_data[7],
                                "BookingClass": flight_data[8],
                                "BoardingZone": "Zone " + str(random.randint(1,4)),
                                "SeatNumber": selectedseat,
                                "GateNumber": "TBA",
                                "SeqNo": (random.randint(1,186)),
                                "MealPreference": meal_combo.get(),
                                "SpecialAssistance": special_assistance_combo.get()
                            }



        print("\n\n\n\n")
        print((''.join(random.choices(string.ascii_uppercase + string.digits, k=7))),)
        print(salutation_combo.get(), first_name_entry.get(),last_name_entry.get(),)
        print(id_card_type_combo.get(), id_card_entry.get(), selected_flight[1], flight_data[0],)
        print(flight_data[1], flight_data[2], (datetime.strptime(flight_data[3], "%H:%M") - timedelta(minutes=30)).strftime("%H:%M:%S"), flight_data[3],)
        print(flight_data[4], flight_data[5], flight_data[6], flight_data[7],)
        print(flight_data[8], ("Zone " + str(random.randint(1,4))), selectedseat,)
        print("TBA", (random.randint(1,186)), meal_combo.get(),)
        print(special_assistance_combo.get())
        print("\n\n\n\n")
        pnr=''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
        try:
            cursor.execute("""
                            INSERT INTO Passenger
                                (   PNR, Salutation, FirstName, LastName, MobileNo, email,
                                    IDCardType, IDCardValue, FL_NO, SRC,
                                    DST, DepDt, BoardingTime, DepTime,
                                    ArrDt, ArrTime, Duration, Price,
                                    BookingClass, BoardingZone, SeatNumber,
                                    GateNumber, SeqNo, MealPreference,
                                    SpecialAssistance
                                )
                            VALUES
                                (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
                        """,    (
                                    pnr, salutation_combo.get(), first_name_entry.get(),last_name_entry.get(), mobileno_entry.get(), email_entry.get(),
                                    id_card_type_combo.get(), id_card_entry.get(), selected_flight[1], flight_data[0],
                                    flight_data[1], flight_data[2], (datetime.strptime(flight_data[3], "%H:%M") - timedelta(minutes=30)).strftime("%H:%M:%S"), flight_data[3],
                                    flight_data[4], flight_data[5], flight_data[6], flight_data[7],
                                    flight_data[8], ("Zone " + str(random.randint(1,4))), selectedseat,
                                    "TBA", (random.randint(1,186)), meal_combo.get(),
                                    special_assistance_combo.get())
                                )
            conn.commit()
            messagebox.showinfo("Booking Successful", f"Your PNR is {pnr}.\nPlease visit the Booking Management Page for more details.")
            book_management()
            # If no exception is raised, the command was successfully executed
        except Exception as e:
            # If an exception is raised, there was an error
            #print("Error:", e)
            error = str(e)
            messagebox.showerror("Error!", error)


def map_sortby(sortby):
    mapping = {
        "Duration": "Duration",
        "Price": "Price",
        "Departure Time": "DepTime",
        "Arrival Time": "ArrTime",
        "Available Seats": "AvailableSeats desc"
    }
    return mapping.get(sortby, sortby)

def home_app():
    # Placeholder function for booking management
    print("Home App...")
    home_frame.pack_forget()
    search_frame.pack_forget()
    checkin_frame.pack_forget()
    booking_management_frame.pack_forget()
    modify_booking_parent_frame.pack_forget()
    support_frame.pack_forget()
    my_bookings_frame.pack_forget()
    home_frame.pack(fill=tk.BOTH, expand=True)
    

def search_flights():
    # Placeholder function for searching flights
    print("Searching flights...")
    

    home_frame.pack_forget()
    search_frame.pack_forget()
    checkin_frame.pack_forget()
    booking_management_frame.pack_forget()
    modify_booking_parent_frame.pack_forget()
    support_frame.pack_forget()
    my_bookings_frame.pack_forget()
    if LoginStatus == True:
        search_frame.pack(fill=tk.BOTH, expand=True)
    else:
        home_frame.pack(fill=tk.BOTH, expand=True)
        messagebox.showinfo("Login Required", "Please Login to Continue!")
    #output_text.pack(padx=0, pady=0, fill=tk.BOTH, expand=True)  

    #global source, destination, date, flight_class
    source = search_source_entry.get()
    destination = search_destination_entry.get()
    date = search_calendar.get_date()
    flight_class = search_class_combobox.get()
    sortby = map_sortby(search_sortby_combobox.get())
    
    parsed_date = datetime.strptime(date, "%m/%d/%y")
    formatted_date = parsed_date.strftime("%Y-%m-%d")
    

    query = '''
    SELECT * FROM Flights 
    WHERE SRC = ? AND DST = ? AND DepDt = ? AND BookingClass = ? AND FlightStatus is NOT "CANCELLED"
    ORDER BY {};
    '''.format(sortby)
    
    cursor.execute(query, (source, destination, formatted_date, flight_class))
    
    
    data=cursor.fetchall()
    print(data)
    
    rows=(tabulate(data, headers=[i[0] for i in cursor.description]))
    #output_text.config(text=data)
    flight_data = parse_flight_data(data)
    display_flight_table(search_output_frame, flight_data)

def book_management():
    # Placeholder function for booking management
    print("Booking management...")
    home_frame.pack_forget()
    search_frame.pack_forget()
    checkin_frame.pack_forget()
    booking_management_frame.pack_forget()
    modify_booking_parent_frame.pack_forget()
    support_frame.pack_forget()
    my_bookings_frame.pack_forget()
    
    if LoginStatus == True:
        booking_management_frame.pack(fill=tk.BOTH, expand=True)
    else:
        home_frame.pack(fill=tk.BOTH, expand=True)
        messagebox.showinfo("Login Required", "Please Login to Continue!")

def online_check_in():
    # Placeholder function for online check-in
    print("Online check-in...")
    home_frame.pack_forget()
    search_frame.pack_forget()
    checkin_frame.pack_forget()
    booking_management_frame.pack_forget()
    modify_booking_parent_frame.pack_forget()
    support_frame.pack_forget()
    my_bookings_frame.pack_forget()
    if LoginStatus == True:
        checkin_frame.pack(fill=tk.BOTH, expand=True)
    else:
        home_frame.pack(fill=tk.BOTH, expand=True)
        messagebox.showinfo("Login Required", "Please Login to Continue!")

def itinerary_management():
    # Placeholder function for itinerary management
    print("Itinerary management...")
    home_frame.pack_forget()
    search_frame.pack_forget()
    checkin_frame.pack_forget()
    booking_management_frame.pack_forget()
    modify_booking_parent_frame.pack_forget()
    support_frame.pack_forget()
    my_bookings_frame.pack_forget()
    if LoginStatus == True:
        modify_booking_parent_frame.pack(fill=tk.BOTH, expand=True)
    else:
        home_frame.pack(fill=tk.BOTH, expand=True)
        messagebox.showinfo("Login Required", "Please Login to Continue!")
    

def my_bookings():
    # Placeholder function for itinerary management
    print("My Bookings...")
    home_frame.pack_forget()
    search_frame.pack_forget()
    checkin_frame.pack_forget()
    booking_management_frame.pack_forget()
    modify_booking_parent_frame.pack_forget()
    support_frame.pack_forget()
    if LoginStatus == True:
        my_bookings_frame.pack(fill=tk.BOTH, expand=True)
    else:
        home_frame.pack(fill=tk.BOTH, expand=True)
        messagebox.showinfo("Login Required", "Please Login to Continue!")

    query = "SELECT * FROM Passenger WHERE email = ?"
    global useremail
    value = (useremail,)
    # Execute the query
    cursor.execute(query, value)
    temp=cursor.fetchall()
    print(temp)
    passengers = temp
    # Display the result
    if passengers:
        result_text = "Passengers found:\n\n"
        for passenger in passengers:
            result_text += f"PNR:\t\t {passenger[0]}\n"
            result_text += f"Name:\t\t {passenger[1]} {passenger[2]} {passenger[3]}\n"
            result_text += f"Mobile:\t\t {passenger[4]}\n"
            result_text += f"Email:\t\t {passenger[5]}\n\n"
            result_text += f"ID Card Type:\t\t {passenger[6]}\n"
            result_text += f"ID Card Value:\t\t {passenger[7]}\n\n"
            result_text += f"Flight No:\t\t {passenger[8]}\n"
            result_text += f"Source:\t\t {passenger[9]}\n"
            result_text += f"Destination:\t\t {passenger[10]}\n\n"
            result_text += f"Departure Date:\t\t {passenger[11]}\n"
            result_text += f"Boarding Time:\t\t {passenger[12]}\n"
            result_text += f"Departure Time:\t\t {passenger[13]}\n"
            result_text += f"Arrival Date:\t\t {passenger[14]}\n"
            result_text += f"Arrival Time:\t\t {passenger[15]}\n"
            result_text += f"Duration:\t\t {passenger[16]}\n\n"
            result_text += f"Price:\t\t Rs. {passenger[17]}\n"
            result_text += f"Booking Class:\t\t {passenger[18]}\n\n"
            result_text += f"Boarding Zone:\t\t {passenger[19]}\n"
            result_text += f"Seat Number:\t\t {passenger[20]}\n"
            result_text += f"Gate Number:\t\t {passenger[21]}\n"
            result_text += f"Sequence Number:\t\t {passenger[22]}\n\n"
            result_text += f"Meal Preference:\t\t {passenger[23]}\n"
            result_text += f"Special Assistance:\t\t {passenger[24]}\n\n\n\n\n\n\n\n\n\n"
        mybookings_result_scroll_text.delete('1.0', tk.END)  # Clear previous text
        mybookings_result_scroll_text.insert(tk.END, result_text)
    else:
        mybookings_result_scroll_text.delete('1.0', tk.END)  # Clear previous text
        mybookings_result_scroll_text.insert(tk.END, "Passenger not found")


def customer_support():
    # Placeholder function for customer support
    print("Customer support...")
    home_frame.pack_forget()
    search_frame.pack_forget()
    checkin_frame.pack_forget()
    booking_management_frame.pack_forget()
    modify_booking_parent_frame.pack_forget()
    support_frame.pack_forget()
    my_bookings_frame.pack_forget()
    if LoginStatus == True:
        support_frame.pack(fill=tk.BOTH, expand=True) 
    else:
        home_frame.pack(fill=tk.BOTH, expand=True)
        messagebox.showinfo("Login Required", "Please Login to Continue!")    

def travel_alerts():
    # Placeholder function for travel alerts
    print("Travel alerts...")
    home_frame.pack_forget()
    search_frame.pack_forget()
    checkin_frame.pack_forget()
    booking_management_frame.pack_forget()
    modify_booking_parent_frame.pack_forget()
    support_frame.pack_forget()

def exit_app():
    root.destroy()

root = tk.Tk()
root.attributes('-fullscreen', True)

# Create frame for logo and buttons
frame = tk.Frame(root)
frame.pack(side=tk.TOP, fill=tk.X)

# Home button
#home_image = tk.PhotoImage(file="home_icon.png").subsample(2)  # Scale by a factor of 2
#home_button = tk.Button(frame, image=home_image, command=home_app, bd=0, highlightthickness=0)
#home_button.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.NW)  # Anchor to top-left corner

# Load and scale SkyVoyage logo
logo_image = tk.PhotoImage(file="SkyVoyageLogoHorizontal.png").subsample(3)  # Scale by a factor of 2
logo_button = tk.Button(frame, image=logo_image, command=home_app, bd=0, highlightthickness=0)
logo_button.pack(side=tk.LEFT, pady=10)  # Anchor to top-left corner
# Close button
close_image = tk.PhotoImage(file="close_icon.png").subsample(2)  # Scale by a factor of 2
close_button = tk.Button(frame, image=close_image, command=exit_app, bd=0, highlightthickness=0)
close_button.pack(side=tk.RIGHT, padx=10, pady=10, anchor=tk.NE)  # Anchor to top-right corner

# Create frame for blue buttons
blue_buttons_frame = tk.Frame(frame)
blue_buttons_frame.pack(side=tk.TOP, pady=50)

# Button configurations
button_config = {
    "bd": 0,
    "highlightthickness": 0,
    "bg": "#3498db",
    "fg": "white",
    "font": ("Helvetica", 12),
    "padx": 20,
    "pady": 10
}

def update_menu_login_button():
    if LoginStatus:
        menu_login_button.config(text="Logout", command=logout_function)
    else:
        menu_login_button.config(text="Login", command=home_app)

def logout_function():
    global LoginStatus
    LoginStatus = False
    home_app()
    messagebox.showinfo("Logout", "Logout Successful!")


# Button text and commands
button_texts = ["Book/Search Flights", "Booking Lookup", "Online Check-in", "Modify Booking", "Customer Support", "My Bookings"]
button_commands = [search_flights, book_management, online_check_in, itinerary_management, customer_support, my_bookings]

# Create and pack blue buttons
for text, command in zip(button_texts, button_commands):
    button = tk.Button(blue_buttons_frame, text=text, command=command, **button_config)
    button.pack(side=tk.LEFT, padx=10, pady=10)

menu_login_button = tk.Button(blue_buttons_frame, text="Login", command=update_menu_login_button, **button_config)
menu_login_button.pack(side=tk.LEFT, padx=10, pady=10)


# Home label
home_frame = tk.Frame(root, bg="#f2f2f2", relief=tk.GROOVE)
home_frame.pack(fill=tk.BOTH, expand=True)

home_label = tk.Label(home_frame, text="Welcome to SkyVoyage!", fg="white", bg="#3498db", font=("Helvetica", 20, "bold"), anchor=tk.W, padx=20, pady=10)
home_label.pack(fill=tk.X)

# Create a frame to contain login-related widgets
login_frame = tk.Frame(home_frame, bg="#f2f2f2")
login_frame.pack(side=tk.LEFT, padx=20, pady=20, anchor=tk.NW)

# Username entry
username_label = tk.Label(login_frame, text="Username:", font=("Helvetica", 12))
username_label.pack(pady=(20, 5), anchor=tk.W)
username_entry = tk.Entry(login_frame, font=("Helvetica", 12))
username_entry.pack(pady=5, padx=10, fill=tk.X)

# Password entry
password_label = tk.Label(login_frame, text="Password:", font=("Helvetica", 12))
password_label.pack(pady=(10, 5), anchor=tk.W)
password_entry = tk.Entry(login_frame, show="*", font=("Helvetica", 12))
password_entry.pack(pady=5, padx=10, fill=tk.X)

# Create a style for the buttons with a shorter height
button_style = ttk.Style()
button_style.configure("Custom.TButton", font=("Helvetica", 12), padding=10)

# Login button
def login():
    # Retrieve the input values from the entry fields
    global username
    global password
    global LoginStatus
    if LoginStatus==True:
        messagebox.showinfo("Alert","You have already Logged In!")
    else:
        username = hasher(username_entry.get())
        password = hasher(password_entry.get())

        # Query the database to check if the username and password match
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            # If a user with the given credentials is found, display a success message
            messagebox.showinfo("Login", "Login successful!")
            LoginStatus = True
            global useremail
            useremail = user[2]
            update_menu_login_button()
        else:
            # If no user with the given credentials is found, display an error message
            messagebox.showerror("Login Error", "Invalid username or password.")


# Signup button
def signup():
    def submit_signup():
        # Retrieve the input values from the entry fields
        username = hasher(username_entry.get())
        password = hasher(password_entry.get())
        email = email_entry.get()
        full_name = full_name_entry.get()
        security_question = security_question_entry.get()
        if security_answer_entry.get(): 
            security_answer = hasher(security_answer_entry.get())
        else:
            security_answer = ''

        try:
            # Check if username is empty
            if not username:
                raise ValueError("Username cannot be empty")

            # Check if password is empty
            if not password_entry.get():
                raise ValueError("Password cannot be empty")

            # Check if email is empty
            if not email:
                raise ValueError("Email cannot be empty")

            # Attempt to insert the user information into the database
            cursor.execute("INSERT INTO users (username, password, email, full_name, security_question, security_answer) VALUES (?, ?, ?, ?, ?, ?)",
                           (username, password, email, full_name, security_question, security_answer))
            conn.commit()

            # Display a success message
            messagebox.showinfo("Sign Up", "User signed up successfully!")

            # Close the signup window
            signup_window.destroy()
        except sqlite3.IntegrityError as e:
            # Check for unique constraint violations
            if "UNIQUE constraint failed: users.username" in str(e):
                messagebox.showerror("Error", "Username already exists. Please choose a different username.")
            elif "UNIQUE constraint failed: users.email" in str(e):
                messagebox.showerror("Error", "Email already exists. Please use a different email address, or reset your password.")
        except ValueError as e:
            # Display custom error messages for specific cases
            messagebox.showerror("Error", str(e))
        except Exception as e:
            # Display a generic error message for other exceptions
            messagebox.showerror("Error", f"Failed to sign up: {str(e)}")


    # Create the signup window
    signup_window = tk.Toplevel(root)
    signup_window.title("Sign Up")

    # Create a frame to contain signup-related widgets
    signup_frame = tk.Frame(signup_window, bg="#f2f2f2")
    signup_frame.pack(padx=20, pady=20)

    # Username entry
    username_label = tk.Label(signup_frame, text="Username:", font=("Helvetica", 12), bg="#f2f2f2")
    username_label.grid(row=0, column=0, pady=5, padx=5, sticky="w")
    username_entry = tk.Entry(signup_frame, font=("Helvetica", 12))
    username_entry.grid(row=0, column=1, pady=5, padx=5, sticky="e")

    # Password entry
    password_label = tk.Label(signup_frame, text="Password:", font=("Helvetica", 12), bg="#f2f2f2")
    password_label.grid(row=1, column=0, pady=5, padx=5, sticky="w")
    password_entry = tk.Entry(signup_frame, show="*", font=("Helvetica", 12))
    password_entry.grid(row=1, column=1, pady=5, padx=5, sticky="e")

    # Email entry
    email_label = tk.Label(signup_frame, text="Email:", font=("Helvetica", 12), bg="#f2f2f2")
    email_label.grid(row=2, column=0, pady=5, padx=5, sticky="w")
    email_entry = tk.Entry(signup_frame, font=("Helvetica", 12))
    email_entry.grid(row=2, column=1, pady=5, padx=5, sticky="e")

    # Full Name entry
    full_name_label = tk.Label(signup_frame, text="Full Name:", font=("Helvetica", 12), bg="#f2f2f2")
    full_name_label.grid(row=3, column=0, pady=5, padx=5, sticky="w")
    full_name_entry = tk.Entry(signup_frame, font=("Helvetica", 12))
    full_name_entry.grid(row=3, column=1, pady=5, padx=5, sticky="e")

    # Security Question entry
    security_question_label = tk.Label(signup_frame, text="Security Question:", font=("Helvetica", 12), bg="#f2f2f2")
    security_question_label.grid(row=4, column=0, pady=5, padx=5, sticky="w")
    security_question_entry = tk.Entry(signup_frame, font=("Helvetica", 12))
    security_question_entry.grid(row=4, column=1, pady=5, padx=5, sticky="e")

    # Security Answer entry
    security_answer_label = tk.Label(signup_frame, text="Security Answer:", font=("Helvetica", 12), bg="#f2f2f2")
    security_answer_label.grid(row=5, column=0, pady=5, padx=5, sticky="w")
    security_answer_entry = tk.Entry(signup_frame, font=("Helvetica", 12))
    security_answer_entry.grid(row=5, column=1, pady=5, padx=5, sticky="e")

    # Submit button
    submit_button = ttk.Button(signup_frame, text="Submit", command=submit_signup, style="Custom.TButton")
    submit_button.grid(row=6, columnspan=2, pady=10, padx=10, sticky="ew")

login_button = ttk.Button(login_frame, text="Login", command=login, style="Custom.TButton")
login_button.pack(pady=5, padx=10, anchor=tk.W, fill=tk.X)

signup_button = ttk.Button(login_frame, text="Sign Up", command=signup, style="Custom.TButton")
signup_button.pack(pady=5, padx=10, anchor=tk.W, fill=tk.X)

# Forgot Password button
def forgot_password():
    # Add your forgot password functionality here
    messagebox.showinfo("Forgot Password", "Forgot Password button clicked!")

forgot_password_button = ttk.Button(login_frame, text="Forgot Password", command=forgot_password, style="Custom.TButton")
forgot_password_button.pack(pady=5, padx=10, anchor=tk.W, fill=tk.X)

# Home image
home_image_bottom = tk.PhotoImage(file="home_image.png")  # Scale by a factor of 2
home_image_label = tk.Label(home_frame, image=home_image_bottom)
home_image_label.pack(side=tk.BOTTOM, pady=20, fill=tk.X, padx=50)


# Create frame for search flights
search_frame = tk.Frame(root, bg="#f2f2f2", relief=tk.GROOVE)
search_frame.pack(fill=tk.BOTH, expand=True)
# Search label
search_label = tk.Label(search_frame, text="Search Flights", fg="white", bg="#3498db", font=("Helvetica", 20, "bold"), anchor=tk.W, padx=20, pady=10)
search_label.pack(fill=tk.X)

# Create inner frame for inputs
search_input_frame = tk.Frame(search_frame, bg="#f2f2f2")
search_input_frame.pack(side="left",fill=tk.BOTH, padx=(10, 0), pady=(20, 20))


search_blank_label1 = tk.Label(search_input_frame,text='')
#search_blank_label2 = tk.Label(search_input_frame,text='')
search_blank_label3 = tk.Label(search_input_frame,text='')
search_blank_label4 = tk.Label(search_input_frame,text='')
search_blank_label5 = tk.Label(search_input_frame,text='')
# Source label and entry
search_source_label = tk.Label(search_input_frame, text="Source:", font=("Helvetica", 12), bg="#f2f2f2")
search_source_label.grid(row=0, column=0, sticky="w", padx=0, pady=0)
search_source_entry = tk.Entry(search_input_frame, font=("Helvetica", 12), width=16, relief=tk.SOLID)
search_source_entry.grid(row=1, column=0, sticky="w", padx=0, pady=0)

# Destination label and entry
search_destination_label = tk.Label(search_input_frame, text="Destination:", font=("Helvetica", 12), bg="#f2f2f2")
search_destination_label.grid(row=0, column=1, sticky="w", padx=15, pady=0)
search_destination_entry = tk.Entry(search_input_frame, font=("Helvetica", 12), width=16, relief=tk.SOLID)
search_destination_entry.grid(row=1, column=1, sticky="w", padx=15, pady=0)

search_blank_label1.grid(row=2, column= 0)
#search_blank_label2.grid(row=3, column= 0)


# Date label and search_calendar
search_date_label = tk.Label(search_input_frame, text="Date:", font=("Helvetica", 12), bg="#f2f2f2")
search_date_label.grid(row=3, column=0, sticky="w", padx=(0, 5), pady=0)
# Add a search_calendar widget (Assuming you have a search_calendar widget implemented)
search_calendar = Calendar(search_input_frame, font=("Helvetica", 12), selectmode='day', year=2024, month=4, day=14, relief=tk.FLAT)
search_calendar.grid(row=4, column=0, columnspan=2, sticky="w", padx=(0, 10), pady=0)


search_blank_label4.grid(row=5, column=0 )

#Class label and Combobox
search_class_var = tk.StringVar()
search_class_label = tk.Label(search_input_frame, text="Class:", font=("Helvetica", 12))
search_class_label.grid(row=6, column=0, padx=0, pady=0, sticky="w")
search_class_combobox = ttk.Combobox(search_input_frame, values=["Economy", "Business", "First"], font=("Helvetica", 12), width=14)
search_class_combobox.grid(row=6, column=1, padx=(0,15), pady=0, sticky="e")
search_class_combobox.current(0)  # Set the default selection to "Economy"

search_sortby_var = tk.StringVar()
search_sortby_label = tk.Label(search_input_frame, text="Sort By:", font=("Helvetica", 12))
search_sortby_label.grid(row=7, column=0, padx=0, pady=0, sticky="w")
search_sortby_combobox = ttk.Combobox(search_input_frame, values=["Duration", "Price", "Departure Time", "Arrival Time", "Available Seats"], font=("Helvetica", 12), width=14)
search_sortby_combobox.grid(row=7, column=1, padx=(0,15), pady=0, sticky="e")
search_sortby_combobox.current(0)


search_blank_label5.grid(row=7, column=0 )
search_blank_label3.grid(row=5, column=0 )

# Search button
search_button = tk.Button(search_input_frame, text="Search", font=("Helvetica", 12), command=search_flights, bg="#3498db", fg="white", bd=0, relief=tk.FLAT)
search_button.grid(row=8, columnspan=2, pady=(10, 0), padx=10, sticky="ew")


# Create frame for outputs
global search_output_frame
search_output_frame = tk.Frame(search_frame, bg="#f2f2f2")
search_output_frame.pack(side="right",fill=tk.BOTH, expand=True, padx=0, pady=(0, 0))

# Example output widget (you can add more as needed)
#output_text = tk.Frame(output_frame, height=10, width=2000,  bg="yellow")
#output_text.pack(padx=0, pady=0, fill=tk.BOTH, expand=True)

#output_text = tk.Label(output_frame, text="", font=("Consolas", 10), anchor="nw")
#output_text.pack(padx=0, pady=0, fill=tk.BOTH, expand=True)




booking_management_frame = ttk.Frame(root)

booking_management_label = tk.Label(booking_management_frame, text="Booking Management", fg="white", bg="#3498db", font=("Helvetica", 20, "bold"), anchor=tk.W, padx=20, pady=10)
booking_management_label.pack(fill=tk.X)

lookup_frame = ttk.Frame(booking_management_frame)
lookup_frame.pack(padx=10, pady=10, fill='both')
lookup_type_label = ttk.Label(lookup_frame, text="Choose lookup type:")
lookup_type_label.pack(padx=10, pady=5, anchor='w')
lookup_type = tk.StringVar()
lookup_type.set("mobile")  # Default to mobile number lookup
lookup_type_radio1 = ttk.Radiobutton(lookup_frame, text="Mobile Number", variable=lookup_type, value="mobile")
lookup_type_radio2 = ttk.Radiobutton(lookup_frame, text="PNR + Last Name", variable=lookup_type, value="pnr")
lookup_type_radio1.pack(padx=10, pady=5, anchor='w')
lookup_type_radio2.pack(padx=10, pady=5, anchor='w')
mobile_frame = ttk.Frame(booking_management_frame)
mobile_frame.pack(padx=10, pady=5, fill='both')
mobile_label = ttk.Label(mobile_frame, text="Mobile Number:\t")
mobile_label.pack(side='left', padx=10, pady=5)
mobile_entry = ttk.Entry(mobile_frame)
mobile_entry.pack(side='left', padx=10, pady=5, fill='x')
pnr_frame = ttk.Frame(booking_management_frame)
pnr_frame.pack(padx=10, pady=5, fill='both')
pnr_label = ttk.Label(pnr_frame, text="PNR:\t\t")
pnr_label.pack(side='left', padx=10, pady=5)
booking_management_pnr_entry = ttk.Entry(pnr_frame)
booking_management_pnr_entry.pack(side='left', padx=10, pady=5)
last_name_label = ttk.Label(pnr_frame, text="Last Name:")
last_name_label.pack(side='left', padx=10, pady=5)
booking_management_last_name_entry = ttk.Entry(pnr_frame)
booking_management_last_name_entry.pack(side='left', padx=10, pady=5)
def search_passenger():
    # Get the selected lookup type
    lookup = lookup_type.get()
    # Perform the query based on the selected lookup type
    if lookup == "mobile":
        # Get the input value
        value = mobile_entry.get()
        query = "SELECT * FROM Passenger WHERE MobileNo = ?"
        value = (value,)
    else:
        entered_pnr = booking_management_pnr_entry.get()
        entered_last_name = booking_management_last_name_entry.get()
        query = "SELECT * FROM Passenger WHERE PNR = ? AND LastName = ?"
        value = (entered_pnr, entered_last_name,)
    # Execute the query
    cursor.execute(query, value)
    temp1=cursor.fetchall()
    print(temp1)
    passengers = temp1
    # Display the result
    if passengers:
        result_text = "Passengers found:\n\n"
        for passenger in passengers:
            result_text += f"PNR:\t\t {passenger[0]}\n"
            result_text += f"Name:\t\t {passenger[1]} {passenger[2]} {passenger[3]}\n"
            result_text += f"Mobile:\t\t {passenger[4]}\n"
            result_text += f"Email:\t\t {passenger[5]}\n\n"
            result_text += f"ID Card Type:\t\t {passenger[6]}\n"
            result_text += f"ID Card Value:\t\t {passenger[7]}\n\n"
            result_text += f"Flight No:\t\t {passenger[8]}\n"
            result_text += f"Source:\t\t {passenger[9]}\n"
            result_text += f"Destination:\t\t {passenger[10]}\n\n"
            result_text += f"Departure Date:\t\t {passenger[11]}\n"
            result_text += f"Boarding Time:\t\t {passenger[12]}\n"
            result_text += f"Departure Time:\t\t {passenger[13]}\n"
            result_text += f"Arrival Date:\t\t {passenger[14]}\n"
            result_text += f"Arrival Time:\t\t {passenger[15]}\n"
            result_text += f"Duration:\t\t {passenger[16]}\n\n"
            result_text += f"Price:\t\t Rs. {passenger[17]}\n"
            result_text += f"Booking Class:\t\t {passenger[18]}\n\n"
            result_text += f"Boarding Zone:\t\t {passenger[19]}\n"
            result_text += f"Seat Number:\t\t {passenger[20]}\n"
            result_text += f"Gate Number:\t\t {passenger[21]}\n"
            result_text += f"Sequence Number:\t\t {passenger[22]}\n\n"
            result_text += f"Meal Preference:\t\t {passenger[23]}\n"
            result_text += f"Special Assistance:\t\t {passenger[24]}\n\n\n\n\n\n\n\n\n\n"
        result_scroll_text_booking_lookup.delete('1.0', tk.END)  # Clear previous text
        result_scroll_text_booking_lookup.insert(tk.END, result_text)
    else:
        result_scroll_text_booking_lookup.delete('1.0', tk.END)  # Clear previous text
        result_scroll_text_booking_lookup.insert(tk.END, "Passenger not found")
search_button = tk.Button(booking_management_frame, text="Search", font=("Helvetica", 12), command=search_passenger, bg="#3498db", fg="white", bd=0, relief=tk.FLAT, height=1, width=10)
search_button.pack(anchor='nw', padx=20, pady=10)
result_scroll_text_booking_lookup = ScrolledText(booking_management_frame, wrap=tk.WORD, font=("Helvetica", 12), width=80, height=80)
result_scroll_text_booking_lookup.pack(padx=10, pady=5, anchor='w', fill='x', expand=True)

def passenger_check_in(pnr):
    # Update the CheckIn status in the Passenger table
    query = "UPDATE Passenger SET CheckIn = ? WHERE PNR = ?"
    values = ("Completed", pnr)
    cursor.execute(query, values)
    conn.commit()
    # Notify the user that check-in is complete
    messagebox.showinfo("Check-In Successful", "Check-in is complete for PNR: {}".format(pnr))

def perform_check_in(pnr):
    # Check if the PNR exists in the database
    query = "SELECT * FROM Passenger WHERE PNR = ?"
    cursor.execute(query, (pnr,))
    passenger = cursor.fetchone()

    if passenger:
        # Perform check-in for the passenger
        passenger_check_in(pnr)
    else:
        # Notify the user that the PNR is invalid
        messagebox.showerror("Error", "Invalid PNR. Please enter a valid PNR.")

def check_in():
    pnr = pnr_entry.get()
    perform_check_in(pnr)

checkin_frame = ttk.Frame(root)
checkin_frame.pack(padx=10, pady=10)

checkin_label = tk.Label(checkin_frame, text="Web Check-In", fg="white", bg="#3498db", font=("Helvetica", 20, "bold"), anchor=tk.W, padx=20, pady=10)
checkin_label.pack(fill=tk.X)

checkinheading_label = ttk.Label(checkin_frame, text="\nWeb Check In Terms & Conditions", font=("Helvetica",24))
checkinheading_label.pack(padx=5, pady=5, side="top")

tnc_label = ttk.Label(checkin_frame, font=("Helvetica",12), text="  1. By proceeding with the web check-in process, you agree to abide by the following terms and conditions:\n  2. Web check-in is available for passengers with confirmed bookings only.\n  3. Passengers must complete the web check-in process within the specified time frame provided by the airline.\n  4. The web check-in facility is subject to availability and may be limited or unavailable for certain flights or routes.\n  5. Passengers must provide accurate and valid travel information during the web check-in process, including passport details and contact information.\n  6. Passengers are responsible for ensuring that they have all necessary travel documents, including a valid passport, visa (if applicable), and any other required documentation.\n  7. The airline reserves the right to deny boarding to passengers who do not comply with the web check-in requirements or fail to meet the necessary travel documentation criteria.\n  8. Web check-in does not guarantee seat assignment or availability of specific seats. Seat allocation is subject to availability and may be assigned at the discretion of the airline.\n  9. Passengers must adhere to the airline's baggage policies and regulations regarding carry-on and checked baggage.\n10. The airline reserves the right to modify, suspend, or terminate the web check-in facility at any time without prior notice.\n11. Passengers are advised to arrive at the airport well in advance of the scheduled departure time to complete security checks and other necessary procedures.\n12. The airline shall not be liable for any loss, damage, or inconvenience arising from the use of the web check-in facility or any failure or delay in the web check-in process.\n13. Passengers are responsible for reviewing and accepting the airline's terms and conditions of carriage, which govern the use of the web check-in facility and travel on the airline's flights.\n14. The airline reserves the right to refuse or revoke web check-in privileges to passengers who violate any of the terms and conditions outlined herein or engage in behavior deemed inappropriate or disruptive.\n15. By proceeding with the web check-in process, passengers acknowledge and agree to comply with all applicable laws, regulations, and airline policies governing air travel.")

tnc_label.pack(padx=20, pady=(50,50), side="top")

confirm_checkin_frame = ttk.Frame(checkin_frame)
confirm_checkin_frame.pack(padx=10, pady=10, side='top', anchor='n')
pnr_label = ttk.Label(confirm_checkin_frame, text="Enter PNR:", font=("Helvetica",12))
pnr_label.pack(padx=5, pady=5, side="left", anchor='center')

pnr_entry = ttk.Entry(confirm_checkin_frame)
pnr_entry.pack(padx=5, pady=5, side="left")

check_in_button = ttk.Button(confirm_checkin_frame, text="Check-In", command=check_in)
check_in_button.pack(padx=5, pady=5, side="left")

def toggle_entry_state(entry, check_var):
    if check_var.get():
        entry.config(state=tk.NORMAL)
    else:
        entry.delete(0, tk.END)
        entry.config(state=tk.DISABLED)

def authenticate():
    auth_pnr = modify_pnr_entry.get()
    auth_last_name = modify_last_name_entry.get()
    modify_pnr_entry.config(state='readonly')
    modify_last_name_entry.config(state='readonly')
    
    cursor.execute("SELECT * FROM Passenger WHERE pnr = ? AND LastName = ?", (auth_pnr, auth_last_name))
    
    # Fetch the retrieved entry
    passengers = cursor.fetchall()
    
    # Display the retrieved entry in a message box
    if passengers:
        result_text = "Existing Booking:\n________________________________________________________________________________\n\n"
        for passenger in passengers:
            result_text += f"PNR:\t\t {passenger[0]}\n"
            result_text += f"Name:\t\t {passenger[1]} {passenger[2]} {passenger[3]}\n"
            result_text += f"Mobile:\t\t {passenger[4]}\n"
            result_text += f"Email:\t\t {passenger[5]}\n\n"
            result_text += f"ID Card Type:\t\t {passenger[6]}\n"
            result_text += f"ID Card Value:\t\t {passenger[7]}\n\n"
            result_text += f"Flight No:\t\t {passenger[8]}\n"
            result_text += f"Source:\t\t {passenger[9]}\n"
            result_text += f"Destination:\t\t {passenger[10]}\n\n"
            result_text += f"Departure Date:\t\t {passenger[11]}\n"
            result_text += f"Boarding Time:\t\t {passenger[12]}\n"
            result_text += f"Departure Time:\t\t {passenger[13]}\n"
            result_text += f"Arrival Date:\t\t {passenger[14]}\n"
            result_text += f"Arrival Time:\t\t {passenger[15]}\n"
            result_text += f"Duration:\t\t {passenger[16]}\n\n"
            result_text += f"Price:\t\t Rs. {passenger[17]}\n"
            result_text += f"Booking Class:\t\t {passenger[18]}\n\n"
            result_text += f"Boarding Zone:\t\t {passenger[19]}\n"
            result_text += f"Seat Number:\t\t {passenger[20]}\n"
            result_text += f"Gate Number:\t\t {passenger[21]}\n"
            result_text += f"Sequence Number:\t\t {passenger[22]}\n\n"
            result_text += f"Meal Preference:\t\t {passenger[23]}\n"
            result_text += f"Special Assistance:\t\t {passenger[24]}\n\n\n\n\n\n\n\n\n\n"
        result_scroll_text.delete('1.0', tk.END)  # Clear previous text
        result_scroll_text.insert(tk.END, result_text)
        
        modify_frame.grid(row=2, column=0, padx=10)
        messagebox.showinfo("Success", "Passenger found successfully.")

    else:
        result_scroll_text.delete('1.0', tk.END)  # Clear previous text
        result_scroll_text.insert(tk.END, "Passenger not found, please try again.")
        modify_frame.grid_forget()
        messagebox.showerror("Error", "Passenger not found. Please try again.")
        authreset()
        
def authreset():
    modify_pnr_entry.config(state='normal')
    modify_pnr_entry.delete(0, 'end')
    modify_last_name_entry.config(state='normal')
    modify_last_name_entry.delete(0, 'end')
    modify_frame.grid_forget()
    result_scroll_text.delete('1.0', tk.END)



def select_modified_seat():
    # Create the popup window
    modpnr = modify_pnr_entry.get()
    modlast_name = modify_last_name_entry.get()

    cursor.execute("SELECT FL_NO FROM Passenger WHERE PNR = ? AND LastName = ?", (modpnr, modlast_name))
    flight_number = cursor.fetchone()

    cursor.execute("SELECT SeatNumber FROM Passenger WHERE FL_NO = ?", (flight_number[0],))
    reserved_seats = [seat[0] for seat in cursor.fetchall()]

    popup = tk.Toplevel(root)
    popup.title("Seat Selection")

    # Create the seat selection interface inside popup
    seat_selection_frame = ttk.Frame(popup)
    seat_selection_frame.pack(padx=20, pady=20)

    # Load the seat icon image
    seat_icon = tk.PhotoImage(file="seat_icon.png")
    seat_selection_label = tk.Label(seat_selection_frame, text="Select Your Seat:", font=("Helvetica", 12))
    seat_selection_label.pack(anchor="nw")

    def select_seat(flight_number, s):
        seat_selection_label.config(text=f"Select Your Seat: {s}")
        global selected_seat
        selected_seat = s

    # Create a nested loop to generate seat buttons
    for col in range(1, 32):  # Change range to 31 for columns
        col_frame = tk.Frame(seat_selection_frame)  # Create a frame for each column
        col_frame.pack(side=tk.LEFT)  # Pack column frames vertically

        for rowx, seat_label in enumerate(['F', 'E', 'D', '', 'C', 'B', 'A']):  # Insert an empty string for the blank line
            if seat_label == '':  # Add padding for the blank line
                tk.Label(col_frame, text=' ', width=4, height=1).pack(side=tk.TOP, padx=2, pady=10)
            else:
                seat = f"{col}{seat_label}"  # Increment row number by 1
                if seat not in reserved_seats:
                    command = lambda s=seat: select_seat(flight_number, s)
                    state = "normal"
                else:
                    command = None
                    state = "disabled"
                button = tk.Button(col_frame, image=seat_icon, compound="center",
                                   width=40, height=40, state=state, command=command,
                                   borderwidth=0, highlightthickness=0)
                button.image = seat_icon  # Keep a reference to the image to prevent garbage collection
                button.pack(side=tk.TOP, padx=2, pady=2)  # Pack buttons within column frames
                button.config(text=seat+"  ")  # Set the seat label as text on the button, overlapping the image

    # Create a frame for the "Submit" button
    submit_frame = ttk.Frame(popup)
    submit_frame.pack(pady=10)

    def submit_seat():
        if 'selected_seat' in globals():
            print("Selected Seat:", selected_seat)
            # You can do further processing here
            global modified_seat
            modified_seat=selected_seat
            seatbuttontext="Selected Seat ("+ str(modified_seat) + ")"
            seat_number_button.configure(text=seatbuttontext)
            popup.destroy()  # Close the popup window
        else:
            messagebox.showerror("Error","Please Select a Seat!")
            select_modified_seat()

    # Place the "Submit" button in the submit_frame
    submit_button = tk.Button(submit_frame, text="Submit", command=submit_seat, 
                              font=("Helvetica", 12), bg="#3498db", fg="white", 
                              activebackground="#2980b9", activeforeground="white", 
                              bd=0, padx=10, pady=5)
    submit_button.pack(side=tk.TOP)

    

    

def cancel():
    pass


def generate_sql_query():
    # Initialize the SQL query
    sql_query = "UPDATE Passenger SET"
    
    # Initialize a list to store modifications
    modifications = []

    # Check if mobile number modification is requested
    if mobile_number_var.get():
        modifications.append("MobileNo = '{}'".format(mobile_number_entry.get()))

    # Check if email modification is requested
    if email_var.get():
        modifications.append("email = '{}'".format(email_entry.get()))

    # Check if ID card modification is requested
    if id_card_var.get():
        modifications.append("IDCardType = '{}'".format(id_card_combobox.get()))

    # Check if ID card number modification is requested
    if id_card_number_var.get():
        modifications.append("IDCardValue = '{}'".format(id_card_number_entry.get()))

    # Check if seat number modification is requested
    if seat_number_var.get():
        modifications.append("SeatNumber = '{}'".format(modified_seat))

    # Check if meal preference modification is requested
    if meal_preference_var.get():
        modifications.append("MealPreference = '{}'".format(meal_preference_combobox.get()))

    # Check if special assistance modification is requested
    if special_assistance_var.get():
        modifications.append("SpecialAssistance = '{}'".format(special_assistance_combobox.get()))

    # Join all modifications into a single string separated by commas
    if modifications:
        sql_query += " " + ", ".join(modifications)
    else:
        # If no modifications are requested, return None
        return None

    # Add condition for updating based on PNR and Last Name
    pnr = modify_pnr_entry.get()
    last_name = modify_last_name_entry.get()
    sql_query += " WHERE PNR = '{}' AND LastName = '{}'".format(pnr, last_name)
    messagebox.showinfo("Success", "Modification Successful!")
    cursor.execute(sql_query)
    conn.commit()

    auth_pnr = modify_pnr_entry.get()
    auth_last_name = modify_last_name_entry.get()
    modify_pnr_entry.config(state='readonly')
    modify_last_name_entry.config(state='readonly')
    
    cursor.execute("SELECT * FROM Passenger WHERE pnr = ? AND LastName = ?", (auth_pnr, auth_last_name))
    
    # Fetch the retrieved entry
    passengers = cursor.fetchall()
    
    # Display the retrieved entry in a message box
    if passengers:
        result_text = "Modified Booking:\n________________________________________________________________________________\n\n"
        for passenger in passengers:
            result_text += f"PNR:\t\t {passenger[0]}\n"
            result_text += f"Name:\t\t {passenger[1]} {passenger[2]} {passenger[3]}\n"
            result_text += f"Mobile:\t\t {passenger[4]}\n"
            result_text += f"Email:\t\t {passenger[5]}\n\n"
            result_text += f"ID Card Type:\t\t {passenger[6]}\n"
            result_text += f"ID Card Value:\t\t {passenger[7]}\n\n"
            result_text += f"Flight No:\t\t {passenger[8]}\n"
            result_text += f"Source:\t\t {passenger[9]}\n"
            result_text += f"Destination:\t\t {passenger[10]}\n\n"
            result_text += f"Departure Date:\t\t {passenger[11]}\n"
            result_text += f"Boarding Time:\t\t {passenger[12]}\n"
            result_text += f"Departure Time:\t\t {passenger[13]}\n"
            result_text += f"Arrival Date:\t\t {passenger[14]}\n"
            result_text += f"Arrival Time:\t\t {passenger[15]}\n"
            result_text += f"Duration:\t\t {passenger[16]}\n\n"
            result_text += f"Price:\t\t Rs. {passenger[17]}\n"
            result_text += f"Booking Class:\t\t {passenger[18]}\n\n"
            result_text += f"Boarding Zone:\t\t {passenger[19]}\n"
            result_text += f"Seat Number:\t\t {passenger[20]}\n"
            result_text += f"Gate Number:\t\t {passenger[21]}\n"
            result_text += f"Sequence Number:\t\t {passenger[22]}\n\n"
            result_text += f"Meal Preference:\t\t {passenger[23]}\n"
            result_text += f"Special Assistance:\t\t {passenger[24]}\n\n\n\n\n\n\n\n\n\n"
        result_scroll_text2.delete('1.0', tk.END)  # Clear previous text
        result_scroll_text2.insert(tk.END, result_text)
        
        modify_frame.grid(row=2, column=0, padx=10)

    else:
        result_scroll_text2.delete('1.0', tk.END)  # Clear previous text
        result_scroll_text2.insert(tk.END, "MODIFICATION FAILED!")
        modify_frame.grid_forget()
        messagebox.showerror("Error", "Modification Failed! Please try again.")
        authreset()










# Function for updating entry box state when checkbox is clicked
def toggle_mobile_number_state():
    toggle_entry_state(mobile_number_entry, mobile_number_var)

def toggle_email_state():
    toggle_entry_state(email_entry, email_var)

def toggle_id_card_state():
    if id_card_var.get():
        id_card_combobox.config(state="readonly")
    else:
        id_card_combobox.set("")  # Clear the selection
        id_card_combobox.config(state="disabled")


def toggle_id_card_number_state():
    toggle_entry_state(id_card_number_entry, id_card_number_var)

def toggle_seat_number_state():
    if seat_number_var.get():
        seat_number_button.config(state=tk.NORMAL)
    else:
        seat_number_button.config(state=tk.DISABLED)

def toggle_meal_preference_state():
    if meal_preference_var.get():
        meal_preference_combobox.config(state="readonly")
    else:
        meal_preference_combobox.set("")  # Clear the selection
        meal_preference_combobox.config(state="disabled")


def toggle_special_assistance_state():
    if special_assistance_var.get():
        special_assistance_combobox.config(state="readonly")
    else:
        special_assistance_combobox.set("")  # Clear the selection
        special_assistance_combobox.config(state="disabled")


# Create modify booking frame
modify_booking_parent_frame = ttk.Frame(root)
modify_booking_parent_frame.pack(padx=20, pady=20, expand=True, fill="both")


Itenerary_Management_label = tk.Label(modify_booking_parent_frame, text="Modify Booking", fg="white", bg="#3498db", font=("Helvetica", 20, "bold"), anchor=tk.W, padx=20, pady=10)
Itenerary_Management_label.pack(fill=tk.X)


# Create the container frame
modify_booking_frame = ttk.Frame(modify_booking_parent_frame)
modify_booking_frame.place(relx=0.5, rely=0.5, anchor="center")  # Anchor to the center of the screen





# Authentication Section Frame
auth_frame = ttk.Frame(modify_booking_frame, width=30, height = 15)
auth_frame.grid(row=1, column=0, padx=(40, 35))

auth_label = ttk.Label(auth_frame, text="Enter your details:")
auth_label.grid(row=0, column=0, columnspan=2, pady=5)

modify_pnr_label = ttk.Label(auth_frame, text="PNR:")
modify_pnr_entry = ttk.Entry(auth_frame)
modify_pnr_label.grid(row=1, column=0, sticky=tk.W, pady=5)
modify_pnr_entry.grid(row=1, column=1, pady=5)

modify_last_name_label = ttk.Label(auth_frame, text="Last Name:")
modify_last_name_entry = ttk.Entry(auth_frame)
modify_last_name_label.grid(row=2, column=0, sticky=tk.W, pady=5)
modify_last_name_entry.grid(row=2, column=1, pady=5)

auth_button = ttk.Button(auth_frame, text="Lookup Itenerary", command=authenticate)
auth_button.grid(row=3, column=1, columnspan=1, pady=10)

auth_reset_button = ttk.Button(auth_frame, text="Reset", command=authreset)
auth_reset_button.grid(row=3, column=0, columnspan=1, pady=10)

cancel_button = ttk.Button(auth_frame, text="Cancel Booking", command=cancel)
cancel_button.grid(row=4, column=0, columnspan=2, pady=10)

# Modification Section Frame
modify_frame = ttk.Frame(modify_booking_frame, width=30, height = 15)


modify_label = ttk.Label(modify_frame, text="Select modifications:")
modify_label.grid(row=0, column=0, columnspan=2, pady=5)

# Individual declaration of checkboxes and entry boxes in the modify_frame
mobile_number_var = tk.BooleanVar()
mobile_number_checkbox = ttk.Checkbutton(modify_frame, text="Mobile Number", variable=mobile_number_var, command=toggle_mobile_number_state)
mobile_number_checkbox.grid(row=1, column=0, pady=5, sticky=tk.W)
mobile_number_entry = ttk.Entry(modify_frame, state=tk.DISABLED)
mobile_number_entry.grid(row=1, column=1, pady=5)

email_var = tk.BooleanVar()
email_checkbox = ttk.Checkbutton(modify_frame, text="Email", variable=email_var, command=toggle_email_state)
email_checkbox.grid(row=2, column=0, pady=5, sticky=tk.W)
email_entry = ttk.Entry(modify_frame, state=tk.DISABLED)
email_entry.grid(row=2, column=1, pady=5)

id_card_var = tk.BooleanVar()
id_card_checkbox = ttk.Checkbutton(modify_frame, text="ID Card Type", variable=id_card_var, command=toggle_id_card_state)
id_card_checkbox.grid(row=3, column=0, pady=5, sticky=tk.W)
id_card_combobox = ttk.Combobox(modify_frame, state="readonly", values=["Aadhaar Card", "PAN Card", "Passport", "Driving License", "Voter ID", "Student ID", "Employee ID", "Other"], width=10)
id_card_combobox.grid(row=3, column=1, pady=5, padx=0, sticky="ew")
id_card_combobox.config(state="disabled")


id_card_number_var = tk.BooleanVar()
id_card_number_checkbox = ttk.Checkbutton(modify_frame, text="ID Card Number", variable=id_card_number_var, command=toggle_id_card_number_state)
id_card_number_checkbox.grid(row=4, column=0, pady=5, sticky=tk.W)
id_card_number_entry = ttk.Entry(modify_frame, state=tk.DISABLED)
id_card_number_entry.grid(row=4, column=1, pady=5)

seat_number_var = tk.BooleanVar()
seat_number_checkbox = ttk.Checkbutton(modify_frame, text="Seat Number", variable=seat_number_var, command=toggle_seat_number_state)
seat_number_checkbox.grid(row=5, column=0, pady=5, sticky=tk.W)
seat_number_button = ttk.Button(modify_frame, text="Select Seat", state=tk.DISABLED, command=select_modified_seat)
seat_number_button.grid(row=5, column=1, pady=5, padx=(0, 0), sticky="ew")

meal_preference_var = tk.BooleanVar()
meal_preference_checkbox = ttk.Checkbutton(modify_frame, text="Meal Preference", variable=meal_preference_var, command=toggle_meal_preference_state)
meal_preference_checkbox.grid(row=6, column=0, pady=5, sticky=tk.W)
meal_preference_combobox = ttk.Combobox(modify_frame, state="readonly", values=["No Meal", "Veg", "Non Veg", "Any"], width=10)
meal_preference_combobox.grid(row=6, column=1, pady=5, padx=(0, 0), sticky="ew")
meal_preference_combobox.config(state="disabled")

special_assistance_var = tk.BooleanVar()
special_assistance_checkbox = ttk.Checkbutton(modify_frame, text="Special Assistance", variable=special_assistance_var, command=toggle_special_assistance_state)
special_assistance_checkbox.grid(row=7, column=0, pady=5, sticky=tk.W)
special_assistance_combobox = ttk.Combobox(modify_frame, state="readonly", width=10, values=["Not Required", "Speech Impaired", "Hearing Impaired", "Visually Impaired", "Wheelchair Assistance", "Unaccompanied Minor"])
special_assistance_combobox.grid(row=7, column=1, pady=5, padx=(0, 0), sticky="ew")
special_assistance_combobox.config(state="disabled")

modify_button = ttk.Button(modify_frame, text="Modify Booking", command=generate_sql_query)
modify_button.grid(row=9, column=0, columnspan=2, pady=10)

result_scroll_text = ScrolledText(modify_booking_frame, wrap=tk.WORD, font=("Helvetica", 12), height=15)
result_scroll_text.grid(row=1, column=1, padx=10, pady=10)

result_scroll_text2 = ScrolledText(modify_booking_frame, wrap=tk.WORD, font=("Helvetica", 12), height=15)
result_scroll_text2.grid(row=2, column=1, padx=10, pady=10)


# Create a frame for the "My Bookings" page
my_bookings_frame = tk.Frame(root, bg="#f2f2f2", relief=tk.GROOVE)


# Label for the "My Bookings" page
my_bookings_label = tk.Label(my_bookings_frame, text="My Bookings", fg="white", bg="#3498db", font=("Helvetica", 20, "bold"), anchor=tk.W, padx=20, pady=10)
my_bookings_label.pack(fill=tk.X)

# Create a frame to contain the bookings
bookings_frame = tk.Frame(my_bookings_frame, bg="#f2f2f2")
bookings_frame.pack(padx=20, pady=20)
mybookings_result_scroll_text = ScrolledText(my_bookings_frame, wrap=tk.WORD, font=("Helvetica", 12), width=80, height=80)
mybookings_result_scroll_text.pack(padx=10, pady=5, anchor='w', fill='x', expand=True)


support_frame = ttk.Frame(root)
    
# Add the frame to the root window


custsupp_label = tk.Label(support_frame, text="Customer Support", fg="white", bg="#3498db", font=("Helvetica", 20, "bold"), anchor=tk.W, padx=20, pady=10)
custsupp_label.pack(fill=tk.X)

# Customer support text
support_text = """
Can't find what you were looking for?
Need assistance with something not available on our app?
Don't worry, we've got you covered!
Our dedicated support team is available around the clock to provide expert guidance
and resolve any issues you may encounter.
Reach out to us via:

Mobile: +91 8758 XXX XXX
Email:   kb4464@srmist.edu.in

Whether it's day or night, weekday or weekend, we're here to assist you 24/7.
Your satisfaction is our priority, and we're committed to ensuring
your experience with us is seamless and stress-free.
Let us help you navigate any challenges and make your journey with us a smooth one.
\n\n\n\n\n\n\n\n
"""

# Create a label to display the support text
support_label = tk.Label(support_frame, text=support_text, justify=tk.LEFT, padx=20, pady=20, font=("Helvetica", 16))
support_label.pack(fill=tk.BOTH, expand=True)


# Start the Tkinter event loop
root.mainloop()
conn.commit()
conn.close()
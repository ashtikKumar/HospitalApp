# TableViewer.py
import sqlite3

def print_room_table():
    conn = sqlite3.connect('new_test12.db')
    cursor = conn.cursor()
    print("\n-- Room Table --")
    cursor.execute("SELECT * FROM ROOM_TABLE")
    rooms = cursor.fetchall()
    if rooms:
        for room in rooms:
            print(f"ID: {room[0]} | Room ID: {room[1]} | Floor ID: {room[2]} | Type: {room[3]} | Rent: ₹{room[4]}")
    else:
        print("No data found in ROOM_TABLE.")
    conn.close()

def print_booking_table():
    conn = sqlite3.connect('new_test12.db')
    cursor = conn.cursor()
    print("\n-- Booking Table --")
    cursor.execute("SELECT * FROM BOOKING_TABLE")
    bookings = cursor.fetchall()
    if bookings:
        for booking in bookings:
            print(f"Booking ID: {booking[0]} | Room ID: {booking[1]} | Start Date: {booking[2]} | End Date: {booking[3]}")
    else:
        print("No data found in BOOKING_TABLE.")
    conn.close()

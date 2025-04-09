import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('new_test12.db')
cursor = conn.cursor()

def generate_date_range(start_date, end_date):
    return [
        (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range((datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days + 1)
    ]

def get_fully_available_rooms(start_date, end_date):
    cursor.execute("""
        SELECT * FROM ROOM_TABLE 
        WHERE ROOM_ID NOT IN (
            SELECT ROOM_ID FROM BOOKING_TABLE 
            WHERE START_DATE <= ? AND END_DATE >= ?
        )
    """, (end_date, start_date))
    return cursor.fetchall()

def calculate_total_rent_for_full_rooms(rooms, date_range):
    total = 0
    for room in rooms:
        rent = room[4] * len(date_range)
        total += rent
        print(f"Room ID: {room[1]} | Start Date: {date_range[0]} | End Date: {date_range[-1]} | Total Rent: ₹{rent}")
    return total

def get_partial_availability(start_date, end_date, date_range):
    cursor.execute("""
        SELECT DISTINCT ROOM_TABLE.* FROM ROOM_TABLE
        LEFT JOIN BOOKING_TABLE ON ROOM_TABLE.ROOM_ID = BOOKING_TABLE.ROOM_ID
        WHERE ROOM_TABLE.ROOM_ID NOT IN (
            SELECT ROOM_ID FROM BOOKING_TABLE 
            WHERE START_DATE <= ? AND END_DATE >= ?
        )
    """, (start_date, end_date))
    rooms = cursor.fetchall()

    results = []
    for room in rooms:
        room_id = room[1]
        rent_per_day = room[4]

        # Fetch overlapping bookings
        cursor.execute("""
            SELECT START_DATE, END_DATE FROM BOOKING_TABLE
            WHERE ROOM_ID = ? AND NOT (END_DATE < ? OR START_DATE > ?)
        """, (room_id, start_date, end_date))
        bookings = cursor.fetchall()

        booked_dates = set()
        for b_start, b_end in bookings:
            b_range = generate_date_range(b_start, b_end)
            booked_dates.update(b_range)

        available_dates = [d for d in date_range if d not in booked_dates]
        if available_dates:
            rent = rent_per_day * len(available_dates)
            results.append((available_dates[0], room_id, available_dates[-1], rent))

    # Sort by first available date
    results.sort()
    return results

def print_available_rooms(start_date, end_date):
    date_range = generate_date_range(start_date, end_date)

    # Case 1: Fully available rooms
    full_rooms = get_fully_available_rooms(start_date, end_date)
    if full_rooms:
        print("Checking for Fully Available Rooms\n")
        total = calculate_total_rent_for_full_rooms(full_rooms, date_range)
        print(f"\nTotal Rent (Fully Available Rooms): ₹{total}")
        return

    # Case 2: Partially available rooms
    print("No fully available rooms.")
    print("Checking for Partially Available Rooms:\n")
    partial_rooms = get_partial_availability(start_date, end_date, date_range)
    if not partial_rooms:
        print("No rooms are available in the given date range.")
        return
    total = 0
    for start, room_id, end, rent in partial_rooms:
        print(f"Room ID: {room_id} | Start Date: {start} | End Date: {end} | Total Rent: ₹{rent}")
        total += rent

    print(f"\nTotal Rent (Partially Available Rooms): ₹{total}")


def occupancy_report(date):
    print(f"Occupancy on : {date}")
    cursor.execute("SELECT COUNT(*) FROM BOOKING_TABLE WHERE START_DATE <= ? AND END_DATE >= ?", (date, date))
    filled = cursor.fetchone()[0]

    total_rooms = cursor.execute("SELECT COUNT(*) FROM ROOM_TABLE").fetchone()[0]
    percentage = (filled / total_rooms) * 100
    print(f"Total rooms: {total_rooms}")
    print(f"Occupied rooms: {filled}")
    print(f"Occupancy percentage: {percentage:.2f}%")

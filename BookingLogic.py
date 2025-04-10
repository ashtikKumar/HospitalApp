import sqlite3
from datetime import datetime, timedelta

DB_NAME = 'JnJ_Hospitals.db'


def connect():
    return sqlite3.connect(DB_NAME)


def generate_date_range(start_date, end_date):
    return [
        (datetime.strptime(start_date, "%Y-%m-%d") +
         timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range((datetime.strptime(end_date, "%Y-%m-%d") -
                        datetime.strptime(start_date, "%Y-%m-%d")).days + 1)
    ]


def get_fully_available_rooms(start_date, end_date):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM ROOM_TABLE 
        WHERE ROOM_ID NOT IN (
            SELECT ROOM_ID FROM BOOKING_TABLE 
            WHERE START_DATE <= ? AND END_DATE >= ?
        )
    """, (end_date, start_date))
    rooms = cursor.fetchall()
    conn.close()
    return rooms


def get_partial_availability(start_date, end_date, date_range):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        """
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

        cursor.execute(
            """
            SELECT START_DATE, END_DATE FROM BOOKING_TABLE
            WHERE ROOM_ID = ? AND NOT (END_DATE < ? OR START_DATE > ?)
        """, (room_id, start_date, end_date))
        bookings = cursor.fetchall()

        booked_dates = set()
        for b_start, b_end in bookings:
            booked_dates.update(generate_date_range(b_start, b_end))

        available_dates = [d for d in date_range if d not in booked_dates]
        if available_dates:
            rent = rent_per_day * len(available_dates)
            results.append(
                (available_dates[0], room_id, available_dates[-1], rent))

    conn.close()
    results.sort()
    return results


# def handle_booking():
#     start_date = input("Enter Start Date (YYYY-MM-DD): ").strip()
#     end_date = input("Enter End Date (YYYY-MM-DD): ").strip()
#     date_range = generate_date_range(start_date, end_date)

#     full_rooms = get_fully_available_rooms(start_date, end_date)
#     available_rooms = []
#     total_rent = 0

#     if full_rooms:
#         for room in full_rooms:
#             rent = room[4] * len(date_range)
#             total_rent += rent
#             available_rooms.append({
#                 'room_id': room[1],
#                 'start_date': start_date,
#                 'end_date': end_date,
#                 'rent': rent
#             })
#     else:
#         partials = get_partial_availability(start_date, end_date, date_range)
#         if not partials:
#             print("No rooms available in the given date range.")
#             return
#         for start, room_id, end, rent in partials:
#             total_rent += rent
#             available_rooms.append({
#                 'room_id': room_id,
#                 'start_date': start,
#                 'end_date': end,
#                 'rent': rent
#             })

#     print("\nAvailable Rooms:")
#     for room in available_rooms:
#         print(
#             f"Room ID: {room['room_id']} | Start: {room['start_date']} | End: {room['end_date']} | Rent: ₹{room['rent']}"
#         )

#     print(f"\nTotal Rent: ₹{total_rent}")
#     confirm = input("\nWould you like to proceed with booking? (yes/no): "
#                     ).strip().lower()
#     if confirm == 'yes':
#         conn = connect()
#         cursor = conn.cursor()
#         for room in available_rooms:
#             cursor.execute("SELECT MAX(ID) FROM BOOKING_TABLE")
#             max_id = cursor.fetchone()[0]
#             booking_id = (max_id or 0) + 1
#             cursor.execute(
#                 "INSERT INTO BOOKING_TABLE (ID, ROOM_ID, START_DATE, END_DATE) VALUES (?, ?, ?, ?)",
#                 (booking_id, room['room_id'], room['start_date'],
#                  room['end_date']))
#         conn.commit()
#         conn.close()
#         print("\nBooking successful!")


# def handle_booking():
#     start_date = input("Enter Start Date (YYYY-MM-DD): ").strip()
#     end_date = input("Enter End Date (YYYY-MM-DD): ").strip()
#     date_range = generate_date_range(start_date, end_date)

#     full_rooms = get_fully_available_rooms(start_date, end_date)
#     available_rooms = []
#     total_rent = 0

#     if full_rooms:
#         # ✅ Take only the first available room
#         room = full_rooms[0]
#         rent = room[4] * len(date_range)
#         total_rent += rent
#         available_rooms.append({
#             'room_id': room[1],
#             'start_date': start_date,
#             'end_date': end_date,
#             'rent': rent
#         })
#     else:
#         partials = get_partial_availability(start_date, end_date, date_range)
#         if not partials:
#             print("No rooms available in the given date range.")
#             return
#         # ✅ Take only the first partially available room
#         start, room_id, end, rent = partials[0]
#         total_rent += rent
#         available_rooms.append({
#             'room_id': room_id,
#             'start_date': start,
#             'end_date': end,
#             'rent': rent
#         })

#     print("\nAvailable Room:")
#     for room in available_rooms:
#         print(
#             f"Room ID: {room['room_id']} | Start: {room['start_date']} | End: {room['end_date']} | Rent: ₹{room['rent']}"
#         )

#     print(f"\nTotal Rent: ₹{total_rent}")
#     confirm = input("\nWould you like to proceed with booking? (yes/no): "
#                     ).strip().lower()
#     if confirm == 'yes':
#         conn = connect()
#         cursor = conn.cursor()
#         for room in available_rooms:
#             cursor.execute("SELECT MAX(ID) FROM BOOKING_TABLE")
#             max_id = cursor.fetchone()[0]
#             booking_id = (max_id or 0) + 1
#             cursor.execute(
#                 "INSERT INTO BOOKING_TABLE (ID, ROOM_ID, START_DATE, END_DATE) VALUES (?, ?, ?, ?)",
#                 (booking_id, room['room_id'], room['start_date'],
#                  room['end_date']))
#         conn.commit()
#         conn.close()
#         print("\nBooking successful!")


def handle_booking():
    start_date = input("Enter Start Date (YYYY-MM-DD): ").strip()
    end_date = input("Enter End Date (YYYY-MM-DD): ").strip()
    date_range = generate_date_range(start_date, end_date)

    full_rooms = get_fully_available_rooms(start_date, end_date)
    available_rooms = []
    total_rent = 0

    if full_rooms:
        # ✅ Case 1: Only use the first fully available room
        room = full_rooms[0]
        rent = room[4] * len(date_range)
        total_rent = rent
        available_rooms.append({
            'room_id': room[1],
            'start_date': start_date,
            'end_date': end_date,
            'rent': rent
        })

        print("\nAvailable Room:")
        room = available_rooms[0]
        print(
            f"Room ID: {room['room_id']} | Start: {room['start_date']} | End: {room['end_date']} | Rent: ₹{room['rent']}")
    else:
        # ✅ Case 2: Show ALL partial availability options
        partials = get_partial_availability(start_date, end_date, date_range)
        if not partials:
            print("No rooms available in the given date range.")
            return

        for start, room_id, end, rent in partials:
            total_rent += rent
            available_rooms.append({
                'room_id': room_id,
                'start_date': start,
                'end_date': end,
                'rent': rent
            })

        print("\nAvailable Rooms:")
        for room in available_rooms:
            print(
                f"Room ID: {room['room_id']} | Start: {room['start_date']} | End: {room['end_date']} | Rent: ₹{room['rent']}")

    print(f"\nTotal Rent: ₹{total_rent}")
    confirm = input("\nWould you like to proceed with booking? (yes/no): ").strip().lower()
    if confirm == 'yes':
        conn = connect()
        cursor = conn.cursor()
        for room in available_rooms:
            cursor.execute("SELECT MAX(ID) FROM BOOKING_TABLE")
            max_id = cursor.fetchone()[0]
            booking_id = (max_id or 0) + 1
            cursor.execute(
                "INSERT INTO BOOKING_TABLE (ID, ROOM_ID, START_DATE, END_DATE) VALUES (?, ?, ?, ?)",
                (booking_id, room['room_id'], room['start_date'], room['end_date']))
        conn.commit()
        conn.close()
        print("\nBooking successful!")


def occupancy_report(date):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM BOOKING_TABLE WHERE START_DATE <= ? AND END_DATE >= ?",
        (date, date))
    filled = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ROOM_TABLE")
    total_rooms = cursor.fetchone()[0]
    conn.close()

    percentage = (filled / total_rooms) * 100
    print(f"Total rooms: {total_rooms}")
    print(f"Occupied rooms: {filled}")
    print(f"Occupancy on {date}: {percentage:.2f}%")


def print_room_table():
    conn = connect()
    cursor = conn.cursor()
    print("\n-- Room Table --")
    cursor.execute("SELECT * FROM ROOM_TABLE")
    rooms = cursor.fetchall()
    if rooms:
        print(f"{'ID':<5}{'Room ID':<10}{'Floor ID':<10}{'Type':<10}{'Rent (₹)':<10}")
        print("-" * 45)

        for room in rooms:
            print(f"{room[0]:<5}{room[1]:<10}{room[2]:<10}{room[3]:<10}{room[4]:<10}")
    else:
        print("No data found in ROOM_TABLE.")

    conn.close()



def print_booking_table():
    conn = connect()
    cursor = conn.cursor()
    print("\n-- Booking Table --")
    print(f"{'Booking ID':<12} | {'Room ID':<8} | {'Start Date':<12} | {'End Date':<12}")
    print("-" * 55)
    cursor.execute("SELECT * FROM BOOKING_TABLE")
    for booking in cursor.fetchall():
        print(f"{booking[0]:<12} | {booking[1]:<8} | {booking[2]:<12} | {booking[3]:<12}")
    conn.close()


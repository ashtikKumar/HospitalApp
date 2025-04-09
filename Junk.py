'''

subprocess.run(["python", "BookingTable.py"])
subprocess.run(["python", "RoomTable.py"])



# Print the table
cursor.execute("SELECT * FROM BOOKING_TABLE")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Print the table
cursor.execute("SELECT * FROM ROOM_TABLE")
rows = cursor.fetchall()
for row in rows:
    print(row)


# Drop the tables
cursor.execute("DROP TABLE BOOKING_TABLE")
cursor.execute("DROP TABLE ROOM_TABLE")
# Commit the changes
conn.commit()


# Check for rooms which are booked in the given date range
def check_availability(start_date, end_date):
    cursor.execute(
        "SELECT ROOM_ID FROM BOOKING_TABLE WHERE START_DATE <= ? AND END_DATE >= ?", (end_date, start_date))
    booked_rooms = cursor.fetchall()
    return booked_rooms

# Use the function
start_date = '2025-03-25'
end_date = '2025-03-27'
booked_rooms = check_availability(start_date, end_date)
print("Booked rooms:", booked_rooms)

# Check for available rooms
def check_available_rooms(start_date, end_date):
    cursor.execute(
        "SELECT ROOM_ID FROM ROOM_TABLE WHERE ROOM_ID NOT IN (SELECT ROOM_ID FROM BOOKING_TABLE WHERE START_DATE <= ? AND END_DATE >= ?)", (end_date, start_date))
    available_rooms = cursor.fetchall()
    return available_rooms

# Use the function
start_date = '2025-03-25'
end_date = '2025-03-27'
available_rooms = check_available_rooms(start_date, end_date)
print("Available rooms:", available_rooms)
'''

# from datetime import datetime
# import sqlite3
# conn = sqlite3.connect('new_test12.db')
# cursor = conn.cursor()

# def occupancy_report(start_date, ):
#     print(f" occupancy on : {start_date}")
#     # date = parse_date(start_date)
#     total_rooms = cursor.execute(" SELECT COUNT(*) FROM ROOM_TABLE").fetchone()[0]
    
#     filled = cursor.fetchone()[0]
#     percentage = (filled / total_rooms) * 100    
#     print(f"Total rooms: {total_rooms}")


'''

# def print_available_rooms(start_date, end_date):
#   cursor.execute(
#     "SELECT ROOM_ID FROM ROOM_TABLE WHERE ROOM_ID NOT IN (SELECT ROOM_ID FROM BOOKING_TABLE WHERE START_DATE <= ? AND END_DATE >= ?)", (start_date, end_date)
#   )
#   available_rooms = cursor.fetchall()
#   for room in available_rooms:
#     cursor.execute(
#       "SELECT * FROM ROOM_TABLE WHERE ROOM_ID = ?", (room[0],)
#     )
#     room_details = cursor.fetchone()
#     print("Room ID:", room_details[1], end=" ")
#     print("Floor ID:", room_details[2], end=" ")
#     print("Room Type:", room_details[3], end=" ")
#     print("Rent:", room_details[4], "\n")


# def available_rooms(start_date, end_date):

# def print_available_rooms(start_date, end_date):
#     cursor.execute(
#         "SELECT ROOM_ID FROM ROOM_TABLE WHERE ROOM_ID NOT IN (SELECT ROOM_ID FROM BOOKING_TABLE WHERE START_DATE <= ? AND END_DATE >= ?)", (start_date, end_date)
#     )
#     available_rooms = cursor.fetchall()
#     for room in available_rooms:
#         cursor.execute(
#             "SELECT * FROM ROOM_TABLE WHERE ROOM_ID = ?", (room[0],)
#         )
#         room_details = cursor.fetchone()
#         print("Room ID:", room_details[1], end=" ")
#         print("Floor ID:", room_details[2], end=" ")
#         print("Room Type:", room_details[3], end=" ")
#         print("Rent:", room_details[4], "\n")

# def print_available_rooms(start_date, end_date):
#     #print("Case 1: Fully Available Rooms\n")
#     cursor.execute("""
#         SELECT * FROM ROOM_TABLE 
#         WHERE ROOM_ID NOT IN (
#             SELECT ROOM_ID FROM BOOKING_TABLE 
#             WHERE START_DATE <= ? AND END_DATE >= ?
#         )
#     """, (end_date, start_date))  # Preventing overlap
#     fully_available = cursor.fetchall()

#     if not fully_available:
#         print("No fully available rooms.\n")
#     else:
#         for room in fully_available:
#             print(f"Room ID: {room[1]}  Floor ID: {room[2]}  Room Type: {room[3]}  Rent: {room[4]}")
#         print()
#         return

#     #print("Case 2: Partially Available Rooms\n")
#     # Get all rooms not fully booked for the entire period
#     cursor.execute("""
#         SELECT DISTINCT ROOM_TABLE.* FROM ROOM_TABLE
#         LEFT JOIN BOOKING_TABLE ON ROOM_TABLE.ROOM_ID = BOOKING_TABLE.ROOM_ID
#         WHERE ROOM_TABLE.ROOM_ID NOT IN (
#             SELECT ROOM_ID FROM BOOKING_TABLE 
#             WHERE START_DATE <= ? AND END_DATE >= ?
#         )
#     """, (start_date, end_date))

#     partially_available = cursor.fetchall()

#     # Remove fully available rooms from partials to avoid duplication
#     fully_ids = set(room[0] for room in fully_available)
#     partially_available = [room for room in partially_available if room[0] not in fully_ids]

#     if not partially_available:
#         print("No partially available rooms.")
#     else:
#         for room in partially_available:
#             print(f"Room ID: {room[1]}  Floor ID: {room[2]}  Room Type: {room[3]}  Rent: {room[4]}")

# from datetime import datetime, timedelta

# def print_available_rooms(start_date, end_date):
#     s_date = datetime.strptime(start_date, "%Y-%m-%d")
#     e_date = datetime.strptime(end_date, "%Y-%m-%d")
#     total_days = (e_date - s_date).days + 1  # Inclusive

#     total_rent = 0

#     # Case 1: Fully Available Rooms
#     cursor.execute("""
#         SELECT * FROM ROOM_TABLE 
#         WHERE ROOM_ID NOT IN (
#             SELECT ROOM_ID FROM BOOKING_TABLE 
#             WHERE START_DATE <= ? AND END_DATE >= ?
#         )
#     """, (end_date, start_date))
#     fully_available = cursor.fetchall()

#     for room in fully_available:
#         room_id = room[1]
#         monthly_rent = room[4]
#         daily_rent = monthly_rent / 30
#         rent = daily_rent * total_days
#         total_rent += rent

#         print(f"[FULL] Room ID: {room[1]}  Floor ID: {room[2]}  Type: {room[3]}  Rent/Month: ₹{room[4]}")
#         print(f"Available Days: {total_days} | Rent: ₹{rent:.2f}\n")

#     fully_ids = set(room[0] for room in fully_available)

#     # Case 2: Partially Available Rooms (excluding already fully available)
#     cursor.execute("""
#         SELECT DISTINCT ROOM_TABLE.* FROM ROOM_TABLE
#         LEFT JOIN BOOKING_TABLE ON ROOM_TABLE.ROOM_ID = BOOKING_TABLE.ROOM_ID
#         WHERE ROOM_TABLE.ROOM_ID NOT IN (
#             SELECT ROOM_ID FROM BOOKING_TABLE 
#             WHERE START_DATE <= ? AND END_DATE >= ?
#         )
#     """, (start_date, end_date))
#     all_possible_rooms = cursor.fetchall()

#     partially_available = [room for room in all_possible_rooms if room[0] not in fully_ids]

#     for room in partially_available:
#         room_id = room[1]
#         monthly_rent = room[4]
#         daily_rent = monthly_rent / 30

#         cursor.execute("""
#             SELECT START_DATE, END_DATE FROM BOOKING_TABLE
#             WHERE ROOM_ID = ? AND NOT (END_DATE < ? OR START_DATE > ?)
#         """, (room_id, start_date, end_date))
#         bookings = cursor.fetchall()

#         booked_days = set()
#         for b_start, b_end in bookings:
#             b_start_date = datetime.strptime(b_start, "%Y-%m-%d")
#             b_end_date = datetime.strptime(b_end, "%Y-%m-%d")
#             for d in range((b_end_date - b_start_date).days + 1):
#                 booked_days.add(b_start_date + timedelta(days=d))

#         all_days = set(s_date + timedelta(days=i) for i in range(total_days))
#         available_days = sorted(all_days - booked_days)
#         num_available_days = len(available_days)

#         room_rent = daily_rent * num_available_days
#         total_rent += room_rent

#         print(f"[PARTIAL] Room ID: {room[1]}  Floor ID: {room[2]}  Type: {room[3]}  Rent/Month: ₹{room[4]}")
#         print(f"Available Days: {num_available_days} | Rent: ₹{room_rent:.2f}\n")

#     print(f"✅ Total Rent for All Available Rooms (Full + Partial): ₹{total_rent:.2f}")

# from datetime import datetime, timedelta

# def print_available_rooms(start_date, end_date):
#     s_date = datetime.strptime(start_date, "%Y-%m-%d")
#     e_date = datetime.strptime(end_date, "%Y-%m-%d")
#     total_days = (e_date - s_date).days + 1  # Inclusive

#     total_rent = 0

#     # Case 1: Fully Available Rooms
#     cursor.execute("""
#         SELECT * FROM ROOM_TABLE 
#         WHERE ROOM_ID NOT IN (
#             SELECT ROOM_ID FROM BOOKING_TABLE 
#             WHERE START_DATE <= ? AND END_DATE >= ?
#         )
#     """, (end_date, start_date))
#     fully_available = cursor.fetchall()

#     for room in fully_available:
#         room_id = room[1]
#         daily_rent = room[4]
#         rent = daily_rent * total_days
#         total_rent += rent

#         print(f"[FULL] Room ID: {room[1]}  Floor ID: {room[2]}  Type: {room[3]}  Rent/Day: ₹{room[4]}")
#         print(f"Available Days: {total_days} | Rent: ₹{rent:.2f}\n")

#     fully_ids = set(room[0] for room in fully_available)

#     # Case 2: Partially Available Rooms
#     cursor.execute("""
#         SELECT DISTINCT ROOM_TABLE.* FROM ROOM_TABLE
#         LEFT JOIN BOOKING_TABLE ON ROOM_TABLE.ROOM_ID = BOOKING_TABLE.ROOM_ID
#         WHERE ROOM_TABLE.ROOM_ID NOT IN (
#             SELECT ROOM_ID FROM BOOKING_TABLE 
#             WHERE START_DATE <= ? AND END_DATE >= ?
#         )
#     """, (start_date, end_date))
#     all_possible_rooms = cursor.fetchall()

#     partially_available = [room for room in all_possible_rooms if room[0] not in fully_ids]

#     for room in partially_available:
#         room_id = room[1]
#         daily_rent = room[4]

#         cursor.execute("""
#             SELECT START_DATE, END_DATE FROM BOOKING_TABLE
#             WHERE ROOM_ID = ? AND NOT (END_DATE < ? OR START_DATE > ?)
#         """, (room_id, start_date, end_date))
#         bookings = cursor.fetchall()

#         booked_days = set()
#         for b_start, b_end in bookings:
#             b_start_date = datetime.strptime(b_start, "%Y-%m-%d")
#             b_end_date = datetime.strptime(b_end, "%Y-%m-%d")
#             for d in range((b_end_date - b_start_date).days + 1):
#                 booked_days.add(b_start_date + timedelta(days=d))

#         all_days = set(s_date + timedelta(days=i) for i in range(total_days))
#         available_days = sorted(all_days - booked_days)
#         num_available_days = len(available_days)

#         room_rent = daily_rent * num_available_days
#         total_rent += room_rent

#         print(f"[PARTIAL] Room ID: {room[1]}  Floor ID: {room[2]}  Type: {room[3]}  Rent/Day: ₹{room[4]}")
#         print(f"Available Days: {num_available_days} | Rent: ₹{room_rent:.2f}\n")

#     print(f"✅ Total Rent for All Available Rooms (Full + Partial): ₹{total_rent:.2f}")

# from datetime import datetime, timedelta

# def print_available_rooms(start_date, end_date):
#     # Generate full date range as strings
#     date_range = [
#         (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)).strftime("%Y-%m-%d")
#         for i in range((datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days + 1)
#     ]
#     total_rent = 0

#     # --- CASE 1: Fully Available Rooms ---
#     cursor.execute("""
#         SELECT * FROM ROOM_TABLE 
#         WHERE ROOM_ID NOT IN (
#             SELECT ROOM_ID FROM BOOKING_TABLE 
#             WHERE START_DATE <= ? AND END_DATE >= ?
#         )
#     """, (end_date, start_date))
#     fully_available = cursor.fetchall()

#     if fully_available:
#         print("✅ Case 1: Fully Available Rooms\n")
#         for room in fully_available:
#             rent = room[4] * len(date_range)
#             total_rent += rent
#             print(f"Room ID: {room[1]} | Start Date: {start_date} | End Date: {end_date} | Total Rent: ₹{rent}")
#         print(f"\n💰 Total Rent (Fully Available Rooms): ₹{total_rent}")
#         return

#     # --- CASE 2: Partially Available Rooms ---
#     print("❌ Case 1 Failed. Checking Case 2: Partially Available Rooms\n")

#     cursor.execute("""
#         SELECT DISTINCT ROOM_TABLE.* FROM ROOM_TABLE
#         LEFT JOIN BOOKING_TABLE ON ROOM_TABLE.ROOM_ID = BOOKING_TABLE.ROOM_ID
#         WHERE ROOM_TABLE.ROOM_ID NOT IN (
#             SELECT ROOM_ID FROM BOOKING_TABLE 
#             WHERE START_DATE <= ? AND END_DATE >= ?
#         )
#     """, (start_date, end_date))
#     rooms = cursor.fetchall()

#     for room in rooms:
#         room_id = room[1]
#         rent_per_day = room[4]

#         # Fetch bookings that overlap
#         cursor.execute("""
#             SELECT START_DATE, END_DATE FROM BOOKING_TABLE
#             WHERE ROOM_ID = ? AND NOT (END_DATE < ? OR START_DATE > ?)
#         """, (room_id, start_date, end_date))
#         bookings = cursor.fetchall()

#         booked_dates = set()
#         for b_start, b_end in bookings:
#             b_range = [
#                 (datetime.strptime(b_start, "%Y-%m-%d") + timedelta(days=i)).strftime("%Y-%m-%d")
#                 for i in range((datetime.strptime(b_end, "%Y-%m-%d") - datetime.strptime(b_start, "%Y-%m-%d")).days + 1)
#             ]
#             booked_dates.update(b_range)

#         available_dates = [d for d in date_range if d not in booked_dates]
#         if available_dates:
#             rent = rent_per_day * len(available_dates)
#             total_rent += rent
#             print(f"Room ID: {room_id} | Start Date: {available_dates[0]} | End Date: {available_dates[-1]} | Total Rent: ₹{rent}")

#     print(f"\n💰 Total Rent (Partially Available Rooms): ₹{total_rent}")

# from datetime import datetime, timedelta

# def print_available_rooms(start_date, end_date):
#     # Generate full date range as strings
#     date_range = [
#         (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)).strftime("%Y-%m-%d")
#         for i in range((datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days + 1)
#     ]
#     total_rent = 0

#     # --- CASE 1: Fully Available Rooms ---
#     cursor.execute("""
#         SELECT * FROM ROOM_TABLE 
#         WHERE ROOM_ID NOT IN (
#             SELECT ROOM_ID FROM BOOKING_TABLE 
#             WHERE START_DATE <= ? AND END_DATE >= ?
#         )
#     """, (end_date, start_date))
#     fully_available = cursor.fetchall()

#     if fully_available:
#         print("✅ Case 1: Fully Available Rooms\n")
#         for room in fully_available:
#             rent = room[4] * len(date_range)
#             total_rent += rent
#             print(f"Room ID: {room[1]} | Start Date: {start_date} | End Date: {end_date} | Total Rent: ₹{rent}")
#         print(f"\n💰 Total Rent (Fully Available Rooms): ₹{total_rent}")
#         return

#     # --- CASE 2: Partially Available Rooms ---
#     print("❌ Case 1 Failed. Checking Case 2: Partially Available Rooms\n")

#     cursor.execute("""
#         SELECT DISTINCT ROOM_TABLE.* FROM ROOM_TABLE
#         LEFT JOIN BOOKING_TABLE ON ROOM_TABLE.ROOM_ID = BOOKING_TABLE.ROOM_ID
#         WHERE ROOM_TABLE.ROOM_ID NOT IN (
#             SELECT ROOM_ID FROM BOOKING_TABLE 
#             WHERE START_DATE <= ? AND END_DATE >= ?
#         )
#     """, (start_date, end_date))
#     rooms = cursor.fetchall()

#     partial_results = []

#     for room in rooms:
#         room_id = room[1]
#         rent_per_day = room[4]

#         # Fetch bookings that overlap
#         cursor.execute("""
#             SELECT START_DATE, END_DATE FROM BOOKING_TABLE
#             WHERE ROOM_ID = ? AND NOT (END_DATE < ? OR START_DATE > ?)
#         """, (room_id, start_date, end_date))
#         bookings = cursor.fetchall()

#         booked_dates = set()
#         for b_start, b_end in bookings:
#             b_range = [
#                 (datetime.strptime(b_start, "%Y-%m-%d") + timedelta(days=i)).strftime("%Y-%m-%d")
#                 for i in range((datetime.strptime(b_end, "%Y-%m-%d") - datetime.strptime(b_start, "%Y-%m-%d")).days + 1)
#             ]
#             booked_dates.update(b_range)

#         available_dates = [d for d in date_range if d not in booked_dates]
#         if available_dates:
#             rent = rent_per_day * len(available_dates)
#             total_rent += rent
#             partial_results.append((available_dates[0], room_id, available_dates[-1], rent))

#     # Sort by available start date
#     partial_results.sort()

#     for start, room_id, end, rent in partial_results:
#         print(f"Room ID: {room_id} | Start Date: {start} | End Date: {end} | Total Rent: ₹{rent}")

#     print(f"\n💰 Total Rent (Partially Available Rooms): ₹{total_rent}")

'''
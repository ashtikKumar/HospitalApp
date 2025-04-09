import sqlite3
import BookingLogic
from BookingLogic import generate_date_range, get_fully_available_rooms, get_partial_availability

conn = sqlite3.connect('new_test12.db')
cursor = conn.cursor()

def prompt_user_for_booking(start_date, end_date, available_rooms):
  print("\nAvailable Rooms from", start_date, "to", end_date)
  for room in available_rooms:
      print(f"Room ID: {room['room_id']} | Start Date: {room['start_date']} | End Date: {room['end_date']} | Rent: ₹{room['rent']}")

  confirm = input("\nWould you like to proceed with booking these room(s)? (yes/no): ").strip().lower()
  return confirm == 'yes'

def get_next_booking_id(cursor):
  cursor.execute("SELECT MAX(ID) FROM BOOKING_TABLE")
  max_id = cursor.fetchone()[0]
  return (max_id or 0) + 1

def book_rooms(conn, available_rooms):
  cursor = conn.cursor()
  for room in available_rooms:
      booking_id = get_next_booking_id(cursor)
      cursor.execute("""
          INSERT INTO BOOKING_TABLE (ID, ROOM_ID, START_DATE, END_DATE) VALUES (?, ?, ?, ?)
      """, (booking_id, room['room_id'], room['start_date'], room['end_date']))
  conn.commit()
  print("\nBooking successful!")

# def handle_booking():
#     start_date = input("Enter Start Date (YYYY-MM-DD): ").strip()
#     end_date = input("Enter End Date (YYYY-MM-DD): ").strip()
#     date_range = generate_date_range(start_date, end_date)

#     full_rooms = get_fully_available_rooms(start_date, end_date)

#     available_rooms = []
#     if full_rooms:
#         for room in full_rooms:
#             rent = room[4] * len(date_range)
#             available_rooms.append({
#                 'room_id': room[1],
#                 'start_date': start_date,
#                 'end_date': end_date,
#                 'rent': rent
#             })
#     else:
#         partials = get_partial_availability(start_date, end_date, date_range)
#         if not partials:
#             print("No rooms are available in the given date range.")
#             return
#         for start, room_id, end, rent in partials:
#             available_rooms.append({
#                 'room_id': room_id,
#                 'start_date': start,
#                 'end_date': end,
#                 'rent': rent
#             })

#     if available_rooms and prompt_user_for_booking(start_date, end_date, available_rooms):
#         conn = sqlite3.connect('new_test12.db')
#         book_rooms(conn, available_rooms)
#         conn.close()


def handle_booking():
  start_date = input("Enter Start Date (YYYY-MM-DD): ").strip()
  end_date = input("Enter End Date (YYYY-MM-DD): ").strip()
  date_range = generate_date_range(start_date, end_date)

  full_rooms = get_fully_available_rooms(start_date, end_date)

  available_rooms = []
  total_rent = 0  # <-- Track total rent

  if full_rooms:
      for room in full_rooms:
          rent = room[4] * len(date_range)
          total_rent += rent
          available_rooms.append({
              'room_id': room[1],
              'start_date': start_date,
              'end_date': end_date,
              'rent': rent
          })
  else:
      partials = get_partial_availability(start_date, end_date, date_range)
      if not partials:
          print("No rooms are available in the given date range.")
          return
      for start, room_id, end, rent in partials:
          total_rent += rent
          available_rooms.append({
              'room_id': room_id,
              'start_date': start,
              'end_date': end,
              'rent': rent
          })

  print(f"\nTotal Rent: ₹{total_rent}")  # <-- ✅ Print total before booking

  if available_rooms and prompt_user_for_booking(start_date, end_date, available_rooms):
      conn = sqlite3.connect('new_test12.db')
      book_rooms(conn, available_rooms)
      conn.close()

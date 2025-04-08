import DB_Init
import BookingLogic

DB_Init.BookingTable_Init()
DB_Init.RoomTable_Init()

while True:
  print("\n-- JnJ Hospitals --")
  print("-- MENU --")
  print("1. Book a Room")
  print("2. Check Occupancy Percentage")
  print("3. Show Room Table")
  print("4. Show Booking Table")
  print("5. Exit")

  choice = input("Enter your choice: ").strip()

  if choice == '1':
    BookingLogic.handle_booking()
  elif choice == '2':
    date = input("Enter date (YYYY-MM-DD): ").strip()
    BookingLogic.occupancy_report(date)
  elif choice == '3':
    BookingLogic.print_room_table()
  elif choice == '4':
    BookingLogic.print_booking_table()
  elif choice == '5':
    print("Thank you for using JnJ Hospital System.")
    break
  else:
    print("Invalid choice. Please try again.")

#DB_Init.drop_tables()
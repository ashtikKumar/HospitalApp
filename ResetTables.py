import sqlite3

def reset_tables():
    conn = sqlite3.connect('new_test12.db')
    cursor = conn.cursor()

    # Optional: Enable foreign key constraints if you're using them
    cursor.execute("PRAGMA foreign_keys = ON")

    # Clear data from tables
    cursor.execute("DELETE FROM BOOKING_TABLE")
    cursor.execute("DELETE FROM ROOM_TABLE")

    conn.commit()
    conn.close()
    print("ROOM_TABLE and BOOKING_TABLE have been cleared.")

# Uncomment below if you want it to run directly
# if __name__ == "__main__":
#     reset_tables()

def drop_tables():
    conn = sqlite3.connect('new_test12.db')
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS BOOKING_TABLE")
    cursor.execute("DROP TABLE IF EXISTS ROOM_TABLE")

    conn.commit()
    conn.close()
    print("Tables dropped successfully.")
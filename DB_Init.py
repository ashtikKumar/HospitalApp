import sqlite3

DB_NAME = 'JnJ_Hospitals.db'


def RoomTable_Init():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ROOM_TABLE (
            ID INT PRIMARY KEY NOT NULL, 
            ROOM_ID INT NOT NULL, 
            FLOOR_ID INT NOT NULL, 
            ROOM_TYPE TEXT, 
            RENT INTEGER)''')

    rooms = [(1, 201, 2, 'T1', 3500), (2, 202, 2, 'T2', 3500),
             (3, 203, 2, 'T2', 6000)]
    cursor.executemany(
        "INSERT OR IGNORE INTO ROOM_TABLE VALUES (?, ?, ?, ?, ?)", rooms)
    conn.commit()
    conn.close()


def BookingTable_Init():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS BOOKING_TABLE (
            ID INT PRIMARY KEY NOT NULL, 
            ROOM_ID INT NOT NULL, 
            START_DATE DATE NOT NULL, 
            END_DATE DATE NOT NULL,
            FOREIGN KEY(ROOM_ID) REFERENCES ROOM_TABLE(ROOM_ID))''')
    bookings = [(1, 201, '2025-03-03', '2025-03-29'),
                (2, 202, '2025-03-28', '2025-03-30'),
                (3, 203, '2025-03-22', '2025-03-27'),
                (4, 203, '2025-03-30', '2025-04-01'),
                (5, 203, '2025-03-01', '2025-03-21')]
    cursor.executemany(
        "INSERT OR IGNORE INTO BOOKING_TABLE VALUES (?, ?, ?, ?)", bookings)
    conn.commit()
    conn.close()


def reset_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM BOOKING_TABLE")
    cursor.execute("DELETE FROM ROOM_TABLE")
    conn.commit()
    conn.close()
    print("Tables cleared.")


def drop_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS BOOKING_TABLE")
    cursor.execute("DROP TABLE IF EXISTS ROOM_TABLE")
    conn.commit()
    conn.close()
    print("Tables dropped.")

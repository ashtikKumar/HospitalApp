import sqlite3

conn = sqlite3.connect('new_test12.db')
cursor = conn.cursor()

def RoomTable_Init():
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS ROOM_TABLE (ID INT(1) PRIMARY KEY NOT NULL, ROOM_ID INT(3) NOT NULL, FLOOR_ID INT(1) NOT NULL, ROOM_TYPE VARCHAR2(2), RENT NUMBER)'''
    )

    cursor.execute(
        """INSERT OR IGNORE INTO ROOM_TABLE VALUES(1,201,2,'T1',3500)""")
    cursor.execute(
        """INSERT OR IGNORE INTO ROOM_TABLE VALUES(2,202,2,'T2',3500)""")
    cursor.execute(
        """INSERT OR IGNORE INTO ROOM_TABLE VALUES(3,203,2,'T2',6000)""")

    conn.commit()

def BookingTable_Init():
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS BOOKING_TABLE (ID INT(1) PRIMARY KEY NOT NULL, ROOM_ID INT(3)  NOT NULL, START_DATE DATE NOT NULL, END_DATE DATE NOT NULL, FOREIGN KEY(ROOM_ID) REFERENCES ROOM_TABLE(ROOM_ID))'''
    )

    cursor.execute(
        """INSERT OR IGNORE INTO BOOKING_TABLE VALUES(1,201,'2025-03-03', '2025-03-29')"""
    )
    cursor.execute(
        """INSERT OR IGNORE INTO BOOKING_TABLE VALUES(2,202,'2025-03-28', '2025-03-30')"""
    )
    cursor.execute(
        """INSERT OR IGNORE INTO BOOKING_TABLE VALUES(3,203,'2025-03-22', '2025-03-27')"""
    )
    cursor.execute(
        """INSERT OR IGNORE INTO BOOKING_TABLE VALUES(4,203,'2025-03-30', '2025-04-01')"""
    )
    cursor.execute(
        """INSERT OR IGNORE INTO BOOKING_TABLE VALUES(5,203,'2025-03-01', '2025-03-21')"""
    )

    conn.commit()

#!/usr/bin/env python
# parses through the info.txt file, extracts (session, mac address, hits) and updates the sqlite database
import os
import sqlite3
from typing import List, TextIO, Tuple

LIB_DIR: str = os.environ['WIPI_LIB_DIR']  # exported by `wipi`

DB_NAME: str = f'{LIB_DIR}/rpi.db'
connection: sqlite3.Connection = sqlite3.connect(DB_NAME)
cursor: sqlite3.Cursor = connection.cursor()

SESSION_FILE: str = f'{LIB_DIR}/session_start_time.txt'

search_query: str = "SELECT DISTINCT mac_address FROM ATTENDANCE_DATA WHERE session==?"
insert_attendance_query: str = "INSERT OR IGNORE INTO ATTENDANCE_DATA (session, mac_address, hits) VALUES (?, ?, ?)"
insert_student_info: str = "INSERT OR REPLACE INTO STUDENT_INFO (mac_address, name, bits_id, device_make) " \
                           "VALUES (?, (SELECT name FROM STUDENT_INFO WHERE mac_address==?), " \
                           "(SELECT bits_id FROM STUDENT_INFO WHERE mac_address==?), ?)"
update_query: str = "UPDATE ATTENDANCE_DATA SET hits = hits+1 WHERE mac_address==? AND session==?"

# get start time of the session
sess_file: List[bytearray] = list(open(SESSION_FILE, "r"))
start_time: bytearray = sess_file[0]
if start_time[len(start_time) - 1] == "\n":
    start_time = start_time[:len(start_time) - 1]

# get month number from month name
# monthNumber: Dict[str, str] = {
#     "Jan": "01",
#     "Feb": "02",
#     "Mar": "03",
#     "Apr": "04",
#     "May": "05",
#     "Jun": "06",
#     "Jul": "07",
#     "Aug": "08",
#     "Sep": "09",
#     "Oct": "10",
#     "Nov": "11",
#     "Dec": "12"
# }

if __name__ == '__main__':

    cursor.execute(search_query, (start_time,))
    # connection.commit()

    rows = cursor.fetchall()

    macs = {}
    for r in rows:
        m = str(r[0])
        if m in macs:
            continue
        macs[m] = 1

    fp: TextIO = open("info.txt", "r")
    line: bytearray
    for line in fp:
        var: List[bytearray] = line.split()
        # print tuple(var[8])
        if var[8] in macs:
            cursor.execute(update_query, (var[8], start_time))
            connection.commit()
            continue

        macs[var[8]] = 1

        connection.commit()

        # get date and time in sql compatible format
        # var[1] = var[1][:(len(var[1])-1)]
        # if (len(var[1]) == 1):
        # 	var[1] = "0"+var[1]

        # ts = ""
        # ts += (var[2] + '-')
        # if (var[0] not in monthNumber):
        # 	print("invalid month")
        # 	continue

        # ts += (monthNumber[var[0]] + '-')
        # ts += (var[1] + ' ')
        # ts += ((var[3].split('.'))[0])

        # device_manufacturer = (var[9].split('_'))[0]

        # val = (ts, var[5], var[8], device_manufacturer)

        attendance_val: Tuple[bytearray, bytearray, str] = (start_time, var[8], "1")
        cursor.execute(insert_attendance_query, attendance_val)
        connection.commit()

        device = (var[9].split('_'))[0]
        cursor.execute(insert_student_info, (var[8], var[8], var[8], device))
        connection.commit()

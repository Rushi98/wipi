# parses through the info.txt file, extracts (session, mac address, hits) and updates the sqlite database

import sqlite3

DB_NAME = "rpi.db"
search_query = "SELECT DISTINCT mac_address FROM ATTENDANCE_DATA"
insert_query = "INSERT OR IGNORE INTO ATTENDANCE_DATA (session, mac_address, hits) VALUES (?, ?, ?)"
update_query = "UPDATE ATTENDANCE_DATA SET hits = hits+1 WHERE mac_address==?"

# get start time of the session
sess_file = list(open("session_start_time.txt", "r"))
start_time = sess_file[0]
if start_time[len(start_time) - 1] == "\n":
    start_time = start_time[:len(start_time) - 1]

# get month number from month name
monthNumber = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
}

if __name__ == '__main__':

    # attempt connection to the database
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
    except Exception as e:
        print("cannot connect to SQLite")
        raise e

    cursor.execute(search_query)
    connection.commit()

    rows = cursor.fetchall()

    macs = {}
    for r in rows:
        m = str(r[0])
        if m in macs:
            continue
        macs[m] = 1

    fp = open("info.txt", "r")
    for line in fp:
        var = line.split()
        # print tuple(var[8])
        if var[8] in macs:
            cursor.execute(update_query, (var[8],))
            connection.commit()
            continue

        macs[var[8]] = 1
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

        val = (start_time, var[8], "1")

        cursor.execute(insert_query, val)
        connection.commit()

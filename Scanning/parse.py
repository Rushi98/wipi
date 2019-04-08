# parses through the info.txt file, extracts (timestamp, ip address, mac address) and updates the MySql database

import sqlite3
import sys

DB_NAME = "rpi.db"
query = "INSERT OR IGNORE INTO SCAN_DATA VALUES (?, ?, ?, ?)"

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
	except Exception as e:
		raise e
		print("cannot connect to SQLite")
		sys.exit()
	 
	
	fp = open("info.txt", "r")
	for line in fp:
		var = line.split()

		# get date and time in sql compatible format
		var[1] = var[1][:(len(var[1])-1)]
		if (len(var[1]) == 1):
			var[1] = "0"+var[1]

		ts = ""
		ts += (var[2] + '-')
		if (var[0] not in monthNumber):
			print("invalid month")
			continue

		ts += (monthNumber[var[0]] + '-')
		ts += (var[1] + ' ')
		ts += ((var[3].split('.'))[0])

		device_manufacturer = (var[9].split('_'))[0]

		cursor = connection.cursor()

		val = (ts, var[5], var[8], device_manufacturer)
		cursor.execute(query, val)
		connection.commit()

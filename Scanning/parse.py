# parses through the info.txt file, extracts (timestamp, ip address, mac address) and updates the MySql database

import mysql.connector

DB_NAME = "DEVICES"
query = "INSERT IGNORE INTO SCAN_DATA (ts, ip_address, mac_address, device_manufacturer) VALUES (%s, %s, %s, %s)"

# get month number from month name
monthNumber = {
	"Jan": 1,
	"Feb": 2,
	"Mar": 3,
	"Apr": 4,
	"May": 5,
	"Jun": 6,
	"Jul": 7,
	"Aug": 8,
	"Sep": 9,
	"Oct": 10,
	"Nov": 11,
	"Dec": 12
}

if __name__ == '__main__':

	# attempt connection to the database
	try:
		mydb = mysql.connector.connect(
	    host="localhost",
	    user="root",
	    passwd="qwerty",
	    database=DB_NAME,
	    auth_plugin="mysql_native_password")
		
	except Exception as e:
		raise e
		print "cannot connect to mysql server"
		return -1;

	
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
			print "invalid month"
			continue

		ts += (monthNumber[var[0]] + '-')
		ts += (var[1] + ' ')
		ts += ((var[3].split('.'))[0])

		device_manufacturer = (var[9].split('_'))[0]

		myCursor = mydb.cursor()

		val = (ts, var[5], var[8], device_manufacturer)
		myCursor.execute(query, val)
		mydb.commit()

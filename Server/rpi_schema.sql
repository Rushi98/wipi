CREATE TABLE ATTENDANCE_DATA (session DATETIME, mac_address char(17) NOT NULL, hits INTEGER, PRIMARY KEY (session, mac_address));
CREATE TABLE "STUDENT_INFO"
(
	mac_address char(17) not null
		primary key,
	name varchar(100),
	bits_id varchar(15),
	device_make varchar(100)
);

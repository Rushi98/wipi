CREATE TABLE `SCAN_DATA` (
  `ts` datetime NOT NULL
,  `ip_address` varchar(15) NOT NULL
,  `mac_address` char(17) NOT NULL
,  `device_manufacturer` varchar(100) DEFAULT NULL
,  UNIQUE (`ts`)
);
CREATE TABLE `STUDENT_INFO` (
  `mac_address` char(17) NOT NULL
,  `name` varchar(100) NOT NULL
,  `bits_id` varchar(15) NOT NULL
, device_make varchar(100),  PRIMARY KEY (`mac_address`)
);
CREATE TABLE ATTENDANCE_DATA (session DATETIME, mac_address char(17) NOT NULL, hits INTEGER, PRIMARY KEY (session, mac_address));

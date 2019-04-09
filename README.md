# wipi

## Hardware Requirements
1. Raspberry Pi 3 Model B

## Software Requirements
1. SQLite Database System
2. tshark Packet Analyzer
3. python 
4. Arch Linux ARM Port (alarm)
5. All packages listed in `docs/packages`

## Setup
1. Follow `docs/Raspberry Pi 3 _ Arch Linux ARM.pdf` to for installing Arch
   on Pi.
2. `cd /home/alarm/wipi-master`
3. `cp wipi.service /etc/systemd/system/wipi.service`
4. `systemctl enable wipi.service`

## Assumptions About System
1. All packages listed in `/docs/packages` are installed on raspi.
2. There is a user with username = `alarm`, password = `alarm`, home directory = `alarm`
3. The software is installed in directory `/home/alarm/wipi-master/`

#!/bin/bash
# following is the working of the script:
# 1) capture tcp packets for 60 seconds and store in packets.pcap
# 2) use tshark to analyze the captured packets and update the database
# 3) delete the packets.pcap file
# 4) go to step 1)

root_pwd="alarm"

session_start=`date "+%Y-%m-%d %H:%M:%S"`
echo ${session_start} > session_start_time.txt
PARSE_PY_PATH=/home/alarm/wipi-master/parse.py
WIRELESS_INTERFACE=wlan0
SELF_IP=192.168.12.1

for i in {1..50} 
do
	# wlo1 is the wireless interface which captures the packets
	echo $root_pwd | sudo -S tcpdump -i $WIRELESS_INTERFACE -w packets.pcap &
	echo "starting capture #$i"

	# scan for 60 seconds
	sleep 60s
	echo "stopping capture #$i"
	printf "\n"

	# stop the current capture
	pid=$!
	sudo kill -2 $pid

	# analyze the captured packets using tshark
	#tshark -r packets.pcap -Y "arp.opcode==2 && arp contains b8:27:eb:76:35:d6 && arp.src.proto_ipv4!=$SELF_IP"\
	tshark -r packets.pcap -Y "arp.opcode==2  && arp.src.proto_ipv4!=$SELF_IP" \
	 -T fields -E separator=" " -e frame.time -e _ws.col.Info -e _ws.col.Source > info.txt
	
	# use the filtered packets to update the database
	python ${PARSE_PY_PATH}

	# delete the packets captured in this
	sudo rm packets.pcap
done	

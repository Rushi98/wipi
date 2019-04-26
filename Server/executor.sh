#!/bin/bash
# following is the working of the script:
# 1) capture tcp packets for 60 seconds and store in packets.pcap
# 2) use tshark to analyze the captured packets and update the database
# 3) delete the packets.pcap file
# 4) go to step 1)

LIB_DIR='/usr/lib/wipi'
PARSE_PY_PATH=${LIB_DIR}/parse.py
SCAN_DURATION=50    # minutes TODO: get this from argument

# w_interface_name state(UP/DOWN) ip/netmask
function get_w_interface_info() {
# line starting with `w`
local r1="^w"
ip -4 -br address show          \
    | grep ${r1} -m1              \
    | tr -s ' '
}

function get_w_interface_name() {
echo $(get_w_interface_info)    \
    | cut -f1 -d' '
}

function get_w_ip() {
echo $(get_w_interface_info)    \
    | cut -f3 -d' '             \
    | grep -o '[0-9.]*/'        \
    | grep -o '[0-9.]*'
}

session_start=`date "+%Y-%m-%d %H:%M:%S"`
echo ${session_start} > ${LIB_DIR}/session_start_time.txt

WIRELESS_INTERFACE=`get_w_interface_name`
echo "wireless interface is ${WIRELESS_INTERFACE}"

SELF_IP=`get_w_ip`
echo "ip address for wireless interface is ${SELF_IP}"

for i in $(seq 1 ${SCAN_DURATION})
do
	tcpdump -i ${WIRELESS_INTERFACE} -w packets.pcap &
	echo "starting capture #$i"

	# scan for 60 seconds
	sleep 60s
	echo "stopping capture #$i"
	printf "\n"

	# stop the current capture
	pid=$!
	echo "killing ${pid}"
	kill -2 ${pid}

	# analyze the captured packets using tshark
	#tshark -r packets.pcap -Y "arp.opcode==2 && arp contains b8:27:eb:76:35:d6 && arp.src.proto_ipv4!=$SELF_IP"\
	tshark -r packets.pcap -Y "arp.opcode==2  && arp.src.proto_ipv4!=$SELF_IP" \
	 -T fields -E separator=" " -e frame.time -e _ws.col.Info -e _ws.col.Source > info.txt
	
	# use the filtered packets to update the database
	${PARSE_PY_PATH}

	# delete the packets captured in this
	rm packets.pcap
done	

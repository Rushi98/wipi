# following is the working of the script:
# 1) capture tcp packets for 60 seconds and store in packets.pcap
# 2) use tshark to analyze the captured packets and update the database
# 3) delete the packets.pcap file
# 4) go to step 1)

root_pwd="rpi_pwd"

for i in {1..50} 
do
	# wlo1 is the wireless interface which captures the packets
	echo $root_pwd | sudo -S tcpdump -i wlo1 -w packets.pcap &
	echo "starting capture #$i"

	# scan for 60 seconds
	sleep 60s
	echo "stopping capture #$i"
	printf "\n"

	# stop the current capture
	pid=$!
	sudo kill -2 $pid

	# analyze the captured packets using tshark
	tshark -r packets.pcap -Y "arp.opcode==2 && arp contains ac:2b:6e:22:e4:c6 && arp.src.proto_ipv4!=10.42.0.1"\
	 -T fields -E separator=" " -e frame.time -e _ws.col.Info -e _ws.col.Source > info.txt
	
	# use the filtered packets to update the database
	python parse.py

	# delete the packets captured in this
	sudo rm packets.pcap
done	
[https://raspberrypi.stackexchange.com/questions/7987/wifi-configuration-on-arch-linux-arm]

# WiFi configuration on Arch Linux ARM
## Question
I have bought a Model A Pi, and I successfully configured it with a USB Wifi dongle on Raspbian. I recently prepared an SD card with the latest version of Arch Linux ARM and I am trying to get it set up with WiFi. I was trying to follow a Raspbian WiFi tutorial (thinking it could be the same as Arch Linux ARM) which said that there is a directory /etc/network/ and you could set up WiFi from the interface file, but no directory /etc/network/ exists. I heard about netctl but I have no Idea how to use it! I do have a supported USB WiFi dongle. Could someone please show me how I can setup WiFi on Arch Linux ARM? Thanks!

## Answer [https://raspberrypi.stackexchange.com/a/7992]
The deprecated `netcfg` used `/etc/network.d/` to store profiles. The successor of `netcfg` is `netctl`.

In order to setup a wireless network, install `netctl` using `sudo pacman -S netctl` (was installed by default). Next, you have to create a network profile. `/etc/netctl/examples/` contains some examples. Let's assume you want to setup a WPA2-PSK network. Simply copy over the example file and start editing:
```
/etc/netctl# install -m640 examples/wireless-wpa wireless-home
/etc/netctl# cat wireless-home
Description='A simple WPA encrypted wireless connection'
Interface=wlan0
Connection=wireless
Security=wpa

IP=dhcp

ESSID='MyNetwork'
# Prepend hexadecimal keys with \"
# If your key starts with ", write it as '""<key>"'
# See also: the section on special quoting rules in netctl.profile(5)
Key='WirelessKey'
# Uncomment this if your ssid is hidden
#Hidden=yes
```
Edit `MyNetwork` and `WirelessKey` as needed. Note the `640` permissions, you do not want to leak your wireless passphrase to the world!

Proceed with testing:

# netctl start wireless-home
If you do not get an error, you should be connected. Let's test this:
```sh
$ ping 8.8.8.8
```
To make this network start on boot:
```sh
netctl enable wireless-home
# the enable can be done by creating symlink
# /etc/systemd/system/multi-user.target.wants/netctl@asteroid.service' -> '/usr/lib/systemd/system/netctl@.service'
ln -s usr/lib/systemd/system/netctl@.service etc/systemd/system/multi-user.target.wants/netctl@asteroid.service
# and create file `/etc/systemd/system/netctl@asteroid.service.d/profile.conf`
# with content
##############################
# [Unit]
# Description=A simple WPA encrypted wireless connection
# BindsTo=sys-subsystem-net-devices-wlan0.device
# After=sys-subsystem-net-devices-wlan0.device
#############################
```



arp -s 10.0.1.2 00:00:00:00:01:02
sudo tc qdisc add dev h1-eth0 root netem rate 10Mbit limit 100 delay 5ms loss 0.5%
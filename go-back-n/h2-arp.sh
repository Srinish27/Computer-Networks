arp -s 10.0.1.1 00:00:00:00:01:01
sudo tc qdisc add dev h2-eth0 root netem rate 10Mbit limit 100 delay 5ms loss 0.5%
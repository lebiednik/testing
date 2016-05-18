#!bin/sh
sudo pip install dpkt
sudo pip install pytest
sudo pip install ipaddress
git clone https://blebiednik3@scm.ctisl.gtri.gatech.edu/git/scm/av/pcap2har.git
git checkout testing
sudo python setup.py install

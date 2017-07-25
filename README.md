# beaconRelay
This project is destinated to activate relays connected to a Raspberry Pi 3 Model B when an iBeacon is detected. More specificly, it is actually used to open a house gate automatically when a car with an iBeacon is approaching.

# Dependencies
BluePy: https://github.com/IanHarvey/bluepy

# Use
After install all dependencies, you will need to create a file named "beaconList.txt" in the same folder that you have the test.py file. In this new file you should put a list of the iBeacons you want to use as "<MAC ADDRESS>, <NAME OF BEACON>". For example:

```sh
a6:8c:aa:fc:d2:2b, Blue Beacon
06:d7:95:b9:5c:5a, Red Beacon
c2:bd:d7:d6:25:76, White Beacon
```

After this just run the script like:

```sh
$ sudo python test.py
```

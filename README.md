# ThingSpeak Publish and Subscribe

A GUI tool made with *Python Tkinter* for publishing and subscribing to your **ThinksSpeak** cloud channel for pushing and fetching sensors data. And also a local solution to save sensor data with **LAMPP** stack in Raspberry Pi.


## ThingSpeak
---
### Dependencies
- For DHT sensor (humidity and temperature sensors) follow the steps from there : [Adafruit_Python_DHT](https://github.com/adafruit/Adafruit_Python_DHT.git).
- For MQTT Client install `paho-mqtt`
```bash
$ sudo apt install python3-paho-mqtt
```

### Execute
- Clone the repository and change the directory.
- Execute `thingspeak_pubsub.py`
```bash
$ git clone https://github.com/suvambasak/thingspeak-pub-sub.git
$ cd thingspeak-pub-sub/thingspeak/
$ python3 thingspeak_pubsub.py
```
<br>
<p align="center">
  <img src="https://github.com/suvambasak/thingspeak-pub-sub/blob/main/doc/ts.jpg?raw=true">
</p>

<br><br>

## LAMPP Stack
---
### Dependencies
- For DHT sensor (humidity and temperature sensors) follow the steps from there : [Adafruit_Python_DHT](https://github.com/adafruit/Adafruit_Python_DHT.git).
- Install LAMPP stack on Raspberry Pi. Follow this: [LAMP Web Server](https://projects.raspberrypi.org/en/projects/lamp-web-server-with-wordpress#:~:text=Install%20software%20on%20your%20Raspberry,devices%20on%20your%20local%20network).
- Install `pymysql`, `matplotlib`
```bash
$ sudo apt install python3-pymysql python3-matplotlib
```

### Execute
- Clone the repository and change the directory.
```bash
$ git clone https://github.com/suvambasak/thingspeak-pub-sub.git
$ cd thingspeak-pub-sub/lampp/
```
#### Create Table
- Start LAMPP server.
```bash
$ sudo opt/lampp/lampp start
```
- Goto: http://localhost/phpmyadmin/
- From the import tab, import `dht.sql`

#### Run
- Execute `dht_mysql_db.py`
```bash
$ python3 dht_mysql_db.py
```
<br>

<p align="center">
  <img src="https://github.com/suvambasak/thingspeak-pub-sub/blob/main/doc/lamp1.jpg?raw=true">
</p>

---
<br>
<p align="center">
  <img src="https://github.com/suvambasak/thingspeak-pub-sub/blob/main/doc/lamp2.jpg?raw=true">
</p>

---
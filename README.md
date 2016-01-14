# Temperature and humidity Arduino monitor

This is the source code for a very simple temperature and humidity logger based
on an Arduino and the DHT22 sensor.

## Hardware

You will need:

* Arduino board (with an USB cable)
* DHT22 sensor

## Arduino source code

The Arduino source code is in the `src` directory, and can be compiled using
the Arduino IDE.

You also need to install the [DHT11/DHT22
library](https://github.com/adafruit/DHT-sensor-library) into your `libraries`
folder.

## Monitor script

You will need the `pyserial` module to use the monitoring script in the
`monitoring` directory:

    pip install pyserial

You can then read temperature and humidity data from the Arduino connected by
an USB cable, by running:

    python monitor/arduino_monitor.py

## Zabbix template

You must first install the template found in the `zabbix` directory, and add it
to the host the Arduino board is attached to.

To send temperature and humidity data to Zabbix, you will also need the
`py-zabbix` package:

    pip install py-zabbix

Copy the script somewhere:

    mkdir -pv /var/lib/zabbix/scripts
    cp monitor/arduino_monitor.py /var/lib/zabbix/scripts

Copy the systemd service:

    cp systemd/arduino-sensors.service /etc/systemd/system

You can optionally edit the `--host`, `--temperature-item` and
`--humidity-item` arguments to match the names of the host and items you use on
your Zabbix installation.

Reload, enable and start:

    systemctl daemon-reload
    systemctl enable arduino-sensors.service
    systemctl start arduino-sensors.service

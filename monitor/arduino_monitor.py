#!/usr/bin/python
# coding=utf-8

# Base Python File (arduino_monitor.py)
# Created: Sat 24 Oct 2015 12:53:17 PM CEST
# Version: 1.0
#
# This Python script was developped by François-Xavier Thomas.
# You are free to copy, adapt or modify it.
# If you do so, however, leave my name somewhere in the credits, I'd appreciate it ;)
#
# (ɔ) François-Xavier Thomas <fx.thomas@gmail.com>

"""Zabbix monitor for temperature and humidity on an Arduino DHT11/DHT22 sensor"""

import argparse
import logging
import sys
import os

from serial import Serial

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--device", "-d", default="/dev/ttyACM0",
                    help="TTY device on which the Arduino is connected")
parser.add_argument("--host", "-s", default=None,
                    help="Send to Zabbix host on which the trap metric is defined")
parser.add_argument("--temperature-item", "-t", default="arduino.temperature",
                    help="Temperature item name")
parser.add_argument("--humidity-item", "-m", default="arduino.humidity",
                    help="Humidity item name")
parser.add_argument("--verbose", "-v", action="store_true")
args = parser.parse_args()


# Setup logging
class NamedLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        if args.host:
            return '%s: %s' % (args.host, msg), kwargs
        else:
            return msg, kwargs
logging_level = logging.DEBUG if args.verbose else logging.INFO
logging.basicConfig(stream=sys.stderr, level=logging_level)
log = NamedLoggerAdapter(logging.getLogger(), {})

# Connect to the serial device
if not os.path.exists(args.device):
    log.error("Device %s does not exist, exiting.", args.device)
    sys.exit(1)
serial = Serial(args.device, 9600)

# Try to setup Zabbix
if args.host:
    try:
        from zabbix.sender import ZabbixMetric, ZabbixSender
        sender = ZabbixSender(use_config=True)
        log.info("Zabbix support enabled for host: %s", args.host)
    except ImportError:
        log.error("Zabbix support not enabled: py-zabbix not found.")
        sys.exit(2)

# Read from serial forever
while True:

    # Try and parse a line
    data = serial.readline()
    try:
        hum, temp = map(float, data.strip().split(b","))

    # If the output cannot be parsed, print it as is
    except:
        log.info(data.decode("ascii").strip())

    # Otherwise, assume we got temp/humidity values
    else:

        # Write temperature/humidity data to stderr
        log.info("Read %s: %s%%", args.humidity_item, hum)
        log.info("Read %s: %s°C", args.temperature_item, temp)

        # Send to Zabbix, if --host is present
        if args.host:
            try:
                sender.send([
                    ZabbixMetric(args.host, args.humidity_item, str(hum)),
                    ZabbixMetric(args.host, args.temperature_item, str(temp)),
                ])
            except:
                log.exception("Cannot send metric to Zabbix")

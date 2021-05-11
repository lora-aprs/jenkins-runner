#!/bin/python3 -u

import subprocess
import time
import serial
import datetime

class dut:
	def __init__(self, port):
		self.pio_package_path = "$HOME/.platformio/packages"
		self.port = port

	def mkspiffs(self, fs_path, fs_bin):
		print("---------------------------------------------------------------------------------")
		print(f" make spiffs with files from {fs_path}")
		print("---------------------------------------------------------------------------------")
		subprocess.run(f"{self.pio_package_path}/tool-mkspiffs/mkspiffs_espressif32_arduino -c {fs_path} -p 256 -b 4096 -s 1507328 {fs_bin}", shell=True)

	def erase_flash(self):
		print("---------------------------------------------------------------------------------")
		print(f" erase flash")
		print("---------------------------------------------------------------------------------")
		subprocess.run(f"/usr/bin/python3 {self.pio_package_path}/tool-esptoolpy/esptool.py --chip esp32 --port {self.port} erase_flash", shell=True)

	def write_flash(self, addr, bin_file):
		print("---------------------------------------------------------------------------------")
		print(f" write flash with file {bin_file}")
		print("---------------------------------------------------------------------------------")
		subprocess.run(f"/usr/bin/python3 {self.pio_package_path}/tool-esptoolpy/esptool.py --chip esp32 --port {self.port} --baud 460800 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_size detect {addr} {bin_file}", shell=True)

	def monitor(self, timeout_min):
		delta = datetime.timedelta(minutes=timeout_min)
		stop_time = datetime.datetime.now() + delta
		print("---------------------------------------------------------------------------------")
		print(f" will stop monitoring at {stop_time}")
		print("---------------------------------------------------------------------------------")
		ser = serial.Serial(self.port, 115200, timeout=0)
		while datetime.datetime.now() < stop_time:
			line = ser.readline()
			if line:
				print(line.decode(), end='')
		ser.close()
		time.sleep(1)

	def send_nmea(self, nmea_file):
		print("---------------------------------------------------------------------------------")
		print(f" start sending nmea data to {self.port}")
		print("---------------------------------------------------------------------------------")
		f = open(nmea_file, "r")
		ser = serial.Serial(self.port, 115200, timeout=0)
		sleep_count = 0
		for x in f:
			s = ser.read(500)
			if s:
				print(s.decode(), end='')
			sleep_count = sleep_count + 1
			ser.write(x.encode())
			if sleep_count > 2:
				time.sleep(1)
				sleep_count = 0
		ser.close()
		f.close()
		time.sleep(1)

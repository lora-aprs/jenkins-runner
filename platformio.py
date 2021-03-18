#!/bin/python3

import subprocess

pio_package_path = "$HOME/.platformio/packages"

def clear_flash(port):
	subprocess.run(f"/usr/bin/python3 {pio_package_path}/tool-esptoolpy/esptool.py --chip esp32 --port {port} erase_flash", shell=True)

def upload_firmware(port, bin_dir):
	subprocess.run(f"/usr/bin/python3 {pio_package_path}/tool-esptoolpy/esptool.py --chip esp32 --port {port} --baud 460800 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size detect 0x1000 {bin_dir}/bootloader_dio_40m.bin 0x8000 {bin_dir}/partitions.bin 0xe000 {bin_dir}/boot_app0.bin 0x10000 {bin_dir}/firmware.bin", shell=True)

def compile_filesystem(fs_path, fs_bin):
	subprocess.run(f"{pio_package_path}/tool-mkspiffs/mkspiffs_espressif32_arduino -c {fs_path} -p 256 -b 4096 -s 1507328 {fs_bin}", shell=True)

def upload_filesystem(port, fs_bin):
	subprocess.run(f"/usr/bin/python3 {pio_package_path}/tool-esptoolpy/esptool.py --chip esp32 --port {port} --baud 460800 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_size detect 2686976 {fs_bin}", shell=True)

	pass



import sys, os

pathname = os.path.dirname(sys.argv[0])
full_path = os.path.abspath(pathname)

port = "/dev/ttyUSB1"
bin_dir = f"{full_path}/binaries"
fs_path = f"{full_path}/fs"
fs_bin = f"{full_path}/spiffs.bin"

clear_flash(port)
compile_filesystem(fs_path, fs_bin)
upload_filesystem(port, fs_bin)
upload_firmware(port, bin_dir)

import time, serial
import datetime

delta = datetime.timedelta(minutes=1)
stop_time = datetime.datetime.now() + delta
print(stop_time)
ser = serial.Serial(port, 115200, timeout=0)
while datetime.datetime.now() < stop_time:
    s = ser.read(100)
    if s:
        print(s.decode(), end='')
print(datetime.datetime.now())

ser.close()
time.sleep(1)

clear_flash(port)


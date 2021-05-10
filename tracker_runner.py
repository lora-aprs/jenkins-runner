#!/bin/python3 -u

import sys
import os
import time
import platformio

pathname = os.path.dirname(sys.argv[0])
full_path = os.path.abspath(pathname)

bin_dir = f"{full_path}/binaries/ttgo-t-beam-v1"
#fs_path = f"{full_path}/fs"
#fs_bin = f"{full_path}/spiffs.bin"
port = sys.argv[1]
#timeout_min = int(sys.argv[2])
nmea_file = "nmea/cumberland_01.nmea"

print("---------------------------------------------------------------------------------")
print(f"full_path:   {full_path}")
print(f"bin_dir:     {bin_dir}")
#print(f"fs_path:     {fs_path}")
#print(f"fs_bin:      {fs_bin}")
print(f"port:        {port}")
#print(f"timeout_min: {timeout_min}")
print(f"nmea_file:   {nmea_file}")
print("---------------------------------------------------------------------------------")

dut = platformio.dut(port)

dut.erase_flash()
#dut.mkspiffs(fs_path, fs_bin)
#dut.write_flash("2686976", fs_bin)
dut.write_flash("0x1000",  f"{bin_dir}/bootloader_dio_40m.bin")
dut.write_flash("0x8000",  f"{bin_dir}/partitions.bin")
dut.write_flash("0xe000",  f"{bin_dir}/boot_app0.bin")
dut.write_flash("0x10000", f"{bin_dir}/firmware.bin")

dut.send_nmea(nmea_file)

dut.write_flash("0x10000", f"{full_path}/DisplayCleaner.bin")
time.sleep(1)
dut.erase_flash()

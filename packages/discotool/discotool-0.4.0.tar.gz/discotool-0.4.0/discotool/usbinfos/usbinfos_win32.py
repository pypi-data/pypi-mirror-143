#!/usr/bin/env python3

import os
import re
import wmi
from .pyserial_list_ports_windows import comports
from .usbinfos_common import *
from . import usb_descriptor_win32

def filter_port_description(description):
	m = re.match(".*%(.+)%.*", description)
	if m:
		name = m.group(1)
	else:
		name = description
	return name.replace("_"," ").title()

def get_devices_list(drive_info=False):
	remainingPorts = [x for x in comports() if x.vid is not None]
	deviceList = []

	serialNumbers = [{"serial_number": x.serial_number} for x in remainingPorts]

	descriptors = {
		# f"USB\\VID_{dev.vid:04X}&PID_{dev.pid:04X}\\{dev.serial_number}"
		(dev.vid, dev.pid, dev.serial_number): dev
		for dev in usb_descriptor_win32.get_all_devices()
	}

	allMounts = []
	wmi_info = wmi.WMI()
	for physical_disk in wmi_info.Win32_DiskDrive ():
		if physical_disk.InterfaceType != "USB": continue
		volumes = []
		manufacturer, product = "", ""
		pnp_id = physical_disk.PNPDeviceID.replace("\\","#")
		for partition in physical_disk.associators ("Win32_DiskDriveToDiskPartition"):
			for logical_disk in partition.associators ("Win32_LogicalDiskToPartition"):
				if logical_disk.DriveType == 2: # removable
					volumes.append(logical_disk)
					# try to find info from related "windows portable drive" entity
					for ppi in wmi_info.Win32_PnPEntity(pnpclass="WPD"):
						if pnp_id in ppi.PNPDeviceID:
							manufacturer = ppi.manufacturer or manufacturer
							product = ppi.description or product
		# default information from the caption
		if physical_disk.caption:
			# guessing the Manufacturer is the first word
			manufacturer = manufacturer or physical_disk.caption.split(" ")[0]
			# guessing it ends with "USB Device"
			product = product or " ".join(physical_disk.caption.split(" ")[1:-2])
		allMounts.append({
			"manufacturer": manufacturer.strip(),
			"product": product.strip(),
			"disk": physical_disk,
			"volumes": volumes,
		})
		serialNumbers.append({"serial_number":physical_disk.SerialNumber})
	
	# how to get the actual list of USB connected devices in a useful way ?
	# for now we take anything with a serial number: serial ports and disk drives
	devices = serialNumbers

	for device in devices:
		curDevice = {}
		deviceVolumes = []
		name = ""
		SN = device['serial_number']

		ttys = []
		vid = "0"
		pid = "0"
		manufacturer = ""
		for port in list(remainingPorts):
			if port.serial_number == SN:
				vid = port.vid
				pid = port.pid
				name = filter_port_description(port.description)
				manufacturer = port.manufacturer
				iface = port.interface or ""
				ttys.append({'dev':port.device,'iface':iface})
				remainingPorts.remove(port)

		if vid == "0": continue

		version = ""
		mains = []
		deviceVolumes = []
		for mount in allMounts:
			if mount["disk"].SerialNumber == device['serial_number']:
				if mount["manufacturer"]:
					manufacturer = mount["manufacturer"]
				if mount["product"]:
					name = mount["product"]
				for disk in mount["volumes"]:
					if disk.VolumeName is None:
						# disk unmounted or something
						continue
					volume = disk.DeviceID
					if drive_info:
						mains,version = get_cp_drive_info(volume)
					deviceVolumes.append({
						'name': disk.VolumeName,
						'mount_point': volume+"\\",
						'mains': mains,
					})

		uid = (vid,pid,SN)
		if uid in descriptors:
			desc = descriptors[uid]
			manufacturer = desc.manufacturer or manufacturer
			name = desc.product or name

		curDevice['version'] = version
		curDevice['volumes'] = deviceVolumes
		curDevice['name'] = name
		curDevice['vendor_id'] = int(vid)
		curDevice['product_id'] = int(pid)
		curDevice['serial_num'] = SN
		curDevice['ports'] = ttys
		curDevice['manufacturer'] = manufacturer
		deviceList.append(curDevice)

	rp = [port.device for port in remainingPorts]
	return (deviceList,rp)

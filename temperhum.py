#!/usr/bin/env python3

import usb.core
import usb.util
import sys

VERSION = "1.2"

Temperhum_Vendor = 0x413d
Temperhum_Product = 0x2107
Temperhum_Interface = 1
Temperhum_ID = hex(Temperhum_Vendor) + ':' + hex(Temperhum_Product)
Temperhum_ID = Temperhum_ID.replace( '0x', '')

params = [x.lower() for x in sys.argv]

# Check the parameters passed

if "--help" in params:
    print ("")
    print ("Usage: temperhum.py [OPTION]")
    print ("Reads the temperature and humidity from a PCSensor, TEMPerHum, USB sensor")
    print ("")
    print ("--help          shows this :-)")
    print ("--version       displays version information and exits")
    print ("--f             output temperature in Fahrenheit, default is Celsius")
    print ("--nosymbols     do not show C, F or %")
    print ("--debug         turn on debugging output")
    print ("--reattach      if the usb device is attached to a kernel driver, default is to detach it, and leave it that way")
    print ("                this option forces a reattach to the kernel driver on exit")
    print ("")
    exit(0)

if "--version" in params:
    print ("")
    print ("temperhum.py  version", VERSION)
    print ("")
    exit(0)

if "--debug" in params:
    DEBUG = True
else:
    DEBUG = False

if "--f" in params:
    CELSIUS = False
else:
    CELSIUS = True

if "--nosymbols" in params:
    NOSYMBOLS = True
else:
    NOSYMBOLS = False

if "--reattach" in params:
    REATTACH = True
else:
    REATTACH = False


# If debug is true tell the user

if DEBUG == True:
    print ("--debug =", DEBUG, "  --f =", not CELSIUS, "  --nosymbols =", NOSYMBOLS, "  --reattach =", REATTACH)

# Try to find the Temperhum usb device

device = usb.core.find(idVendor = Temperhum_Vendor, idProduct = Temperhum_Product)

# If it was not found report the error and exit

if device is None:
    print ("Error: Device", Temperhum_ID, "not found")
    exit(1)
else:
    if DEBUG == True:
        print ("Found Device ID", Temperhum_ID)
        print ("-" * 20, "Device Information", "-" * 20)
        print (device)
        print ("-" * 20, "Device Information", "-" * 20)
        
# check if it has a kernal driver, if so set a reattach flag and detach it

reattach = False
if device.is_kernel_driver_active(1):
    reattach = True
    if DEBUG == True:
        print ("Warning: kernal driver attached to this device, will try to detach it", end='')
        if REATTACH:
            print (" and reattach at the end")
        else:
            print (" and leave it detached") 

    result = device.detach_kernel_driver(1)

    if result != None:
        print ("Error: unable to detach kernal driver from device")
        exit(2)
    else:
        if DEBUG == True:
            print ("Kernal driver detached ok")

# Extract the correct interface information from the device information

cfg = device[0]
inf = cfg[Temperhum_Interface,0]

if DEBUG == True:
    print ("Claiming the device interface", Temperhum_Interface, "for use")
    
result = usb.util.claim_interface(device, Temperhum_Interface)
if result != None:
    print ("Error: unable to claim the interface")
    exit(3)
else:
    if DEBUG == True:
        print ("Claimed interface ok")

# Extract the read and write endpoint information 

ep_read = inf[0]
ep_write = inf[1]
if DEBUG == True:
    print ("-" * 20, "Read Endpoint Information", "-" * 20)
    print (ep_read)
    print ("-" * 20, "Read Endpoint Information", "-" * 20)
    print ("-" * 20, "Write Endpoint Information", "-" * 20)
    print (ep_write)
    print ("-" * 20, "Write Endpoint Information", "-" * 20)

# Extract the addresses to read from and write to

ep_read_addr = ep_read.bEndpointAddress
ep_write_addr = ep_write.bEndpointAddress

if DEBUG == True:
    print ("Read endpoint address =", hex(ep_read_addr))
    print ("Write endpoint address =", hex(ep_write_addr))
    print ("Sending request for temperature/humidity data to device")

try:
    msg = b'\x01\x80\x33\x01\0\0\0\0'
    sendit = device.write(ep_write_addr, msg)
except:
    print ("Error: sending request to device")
    exit(4)

if DEBUG == True:
    print ("Sending request went ok")
    print ("Reading data from device")

try:
    data = device.read(ep_read_addr, 0x8)
except:
    print ("Error: reading data from device")
    exit(5)
else:
    if DEBUG == True:
        print ("Data returned from device =", data)
    
# Decode the temperature and humidity

if CELSIUS == True:
    temperature = round( ( (data[2] * 256) + data[3] ) / 100, 1 )
else:
    temperature =  round( ( (data[2] * 256) + data[3] ) / 100 * 9/5 + 32, 1 )
    
humidity = int( ( (data[4] * 256) + data[5] ) / 100 )

# Add symbols unless turned off by --nosymbols parameter

if NOSYMBOLS == False:
    if CELSIUS == True:
        temperature = str(temperature) + "C"
    else:
        temperature = str(temperature) + "F"

    humidity = str(humidity) + "%"

# Output the temperature and humidity

if DEBUG == True:
    print ("")
    print ("------------")
    print (temperature, humidity)
    print ("------------")
    print ("")
else:    
    print (temperature, humidity)

# Release the usb resources

if DEBUG == True:
    print ("Releasing USB resources")

result = usb.util.dispose_resources(device)

if result != None:
    print ("Error: releasing USB resources")
else:
    if DEBUG == True:
        print ("Resources released ok")

# Reattach device to the kernel driver if requested by parameter

if REATTACH:
    if DEBUG == True:
        print ("Reattaching the kernel driver to device")
    result = device.attach_kernel_driver(1)
    if result != None:
        print ("Error: reattaching the kernel driver to device")
        exit(6)

exit(0)

# temperhum.py
Python 3 program to read temperature and humidity from a TEMPerHUM USB sensor on a Raspberry Pi

## Installation
In a Raspberry Pi, terminal or ssh session, run the following commands, you can ignore the first one,
if you already have git installed.
```bash
  sudo apt-get install git
  git clone https://github.com/cjmair/temperhum.git
  cd temperhum
  ./install.sh
  ```
## Usage
At a command prompt enter
```bash
  temperhum.py
```
This should return the temperature, in Celsius and the humidity, in the format below
```bash
  23.9C 38%
```
## Optons
Various options can be given on the command line, see the --help option listing below
```
  temperhum.py --help

  Usage: temperhum.py [OPTION]
  Reads the temperature and humidity from a PCSensor, TEMPerHum, USB sensor, USB ID 413d:2107

  --help          shows this :-)
  --version       displays version information and exits
  --f             output temperature in Fahrenheit, default is Celsius
  --nosymbols     do not show C, F or %
  --raw           include the raw data from the sensor in the output, as hex bytes
  --debug         turn on debugging output
  --reattach      if the usb device is attached to a kernel driver, default is to detach it,
                  and leave it that way, this option forces a reattach to the kernel driver on exit
```
example
```
  temperhum.py --f --nosymbols
```
will return the temperature in Fahrenheit and the humidity, without any symbols, as below
```
  75.2 38
```
  

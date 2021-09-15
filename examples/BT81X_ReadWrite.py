
"""
This example initializes Eve Chip and reads the Chip ID.
"""

import sys
import time

from telemetrix_rpi_pico import telemetrix_rpi_pico

# Instantiate the TelemetrixRpiPico class accepting all default parameters.
pico = telemetrix_rpi_pico.TelemetrixRpiPico()

"""
 CALLBACKS
 
 These functions process the data returned from the Eve
"""


def the_device_callback(report):
    """
    Verify the device ID
    """
    print("report=",report)




# Convenience values for the pins.
# Note that the CS value is within a list
SPI_PORT = 0
MISO = 4
MOSI = 3
CLK = 2
CS = [5]
CS_PIN = 5

HIGH = 1
LOW  = 0

REG_ID     = [0x30,0x20,0x00]
REG_CHIPID = [0x0C,0x00,0x00]

DUMMY_BYTE_LENGTH = 1  #2 for QSPI(Unsupported yet)

FREQ = 500000

def write_host_cmd(cmd):
    pico.spi_cs_control(CS_PIN,  LOW)
    pico.spi_write_blocking(cmd, SPI_PORT)
    pico.spi_cs_control(CS_PIN,  HIGH)


#The addr shall be exact 3 bytes 
def read_eve(addr, number_of_bytes):    
    pico.spi_cs_control(CS_PIN,  LOW)
    pico.spi_write_blocking(addr, SPI_PORT) 
    pico.spi_read_blocking(number_of_bytes + DUMMY_BYTE_LENGTH, SPI_PORT, the_device_callback)  
    pico.spi_cs_control(CS_PIN,  HIGH)    
    
def write_eve(addr, buff):  
    bytes_to_write = addr + buff
    bytes_to_write[0] = addr[0] | 0x80
    pico.spi_cs_control(CS_PIN,  LOW)
    pico.spi_write_blocking(bytes_to_write, SPI_PORT) 
    pico.spi_cs_control(CS_PIN,  HIGH)  

# initialize the device
# These are "non-standard" pin-numbers, and therefore
# the qualify_pins parameter is set to FALSE
pico.set_pin_mode_spi(SPI_PORT, MISO, MOSI, CLK, FREQ, CS, qualify_pins=False)

write_host_cmd([0x44,0,0])
write_host_cmd([0,0,0])
time.sleep(.5)


RAM_G = [0x00,0x00,0x00]  # Has to be 3 bytes address
write_eve(RAM_G, [0xDE,0xAD,0xBE,0xBF])


while True:
    try:
        # Read Chip ID of Eve
        read_eve(REG_ID, 1)
        read_eve(REG_CHIPID, 4)
        read_eve(RAM_G,4)
        time.sleep(.1)
        
    except KeyboardInterrupt:
        pico.shutdown()
        sys.exit(0)

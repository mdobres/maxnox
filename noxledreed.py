# Test Module for NOX : Noughts and crosses / Tic Tac Toe Game
# lights LED when reed switch closes

import smbus
import time
import math
import board
import busio
from adafruit_ht16k33 import matrix

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# creates a 8x8 matrix:
matrix = matrix.Matrix8x8(i2c)

# edges of an 3x3 matrix
col_max = 3
row_max = 3

# Clear the matrix.
matrix.fill(0)
col = 0
row = 0

#LED setup
# Create display instance on default I2C address (0x70) and bus number.
#display = Matrix8x8.Matrix8x8(address=0x70, busnum=1)
# check using I2cdetect -y 1  to make sure the address is 70, if not edit the line above to change it
# the correct address

# Initialize the display. Must be called once before using the display.
#display.begin()
#display.clear()
#display.write_display()
# MCP23017  setup
# this program scans both registers one device, giving 2 x 8 = 16 inputs, only 9 of these are used in the NOX program 
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1
# this program scans both the A and B registers of one MCP23017 port exapander and returns changes 
mbrd = [0xFF,0xFF]   # mbrd is the noughts and crosses board  this sets them to 11111111 : open w
chcol =["A","B","C"]  # column labels
i2cadd=0x21 # the I2c Device address of the MCP23017s (A0-A2)
GPIOn = [0x12, 0x13]
IODIRA = 0x00 # APin direction register for first 8 ie 1 = input or 2= output
IODIRB = 0x01 # B Pin direction register
GPIOA  = 0x12 # Register for inputs
GPIOB  = 0x13 # B Register for inputs
GPPUA= 0x0C  # Register for Pull ups A
GPPUB= 0x0D  # Register for Pull ups B

# Set all A 8 GPA pins as  input. ie set them to 1 oXFF = 11111111
bus.write_byte_data(i2cadd,IODIRA,0xFF)
# Set pull up on GPA pins .ie from default of 0 to 11111111
bus.write_byte_data(i2cadd,GPPUA,0xFF)
# Set all B 8 GPB pins as  input. ie set them to 1 oXFF = 11111111
bus.write_byte_data(i2cadd,IODIRB,0xFF)
# Set pull up on GPB pins .ie from default of 0 to 11111111
bus.write_byte_data(i2cadd,GPPUB,0xFF)

print ("starting")
# now look for a change

# Loop until user presses CTRL-C
while True:
  # read the 8 registers

  for l in range(2):  #loops round both registers of MCP23017
    a = bus.read_byte_data(i2cadd,GPIOn[l])
    if a != mbrd[l]: # there has been a change
      c = a ^ mbrd[l]  # bitwise operation copies the bit if it is set in one operand but not both.
      dirx = "Close"
      if a > mbrd[l] : dirx = "Open"  # if the number gets bigger a 0 has changed to a 1
      y = math.frexp(c)[1]  # calculates integer part of log base 2, which is binary bit position
      w=y+l*8
      x =int((w-1)/3)+1   # anodes numbers starts 1
      y =  (2+w)%3   # cathodes number start 0
      
      if dirx == "Close":   matrix[x, y]=2 # switch on the LED
      if dirx == "Open":   matrix[x, y]=0 # switch off the LED
        
      #display.write_display()
      print ("square", w, " Reed Switch " , dirx )   # chcol[(w+2)%3], (int((w-1)/3))+1
      
      mbrd[l]=a  # update the current state of the board
      time.sleep(0.1)


# Clear the display buffer.

matrix.fill(0)


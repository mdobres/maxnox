# Test Module for NOX : Noughts and crosses / Tic Tac Toe Game
# lights LED when reed switch closes

import smbus
import time
import math
import board
import busio
from adafruit_ht16k33 import matrix
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

# Modify this if you have a different sized Character LCD
lcd_columns = 16
lcd_rows = 2

# Initialise I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Initialise the LCD class
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

lcd.clear()

# Set LCD color to blue
lcd.color = [0, 100, 0]
time.sleep(1)

# create some custom characters
lcd.create_char(1, [2, 3, 2, 2, 14, 30, 12, 0])
lcd.create_char(2, [0, 1, 3, 22, 28, 8, 0, 0])
lcd.create_char(3, [0, 14, 21, 23, 17, 14, 0, 0])
lcd.create_char(4, [31, 17, 10, 4, 10, 17, 31, 0])
lcd.create_char(5, [8, 12, 10, 9, 10, 12, 8, 0])
lcd.create_char(6, [2, 6, 10, 18, 10, 6, 2, 0])
lcd.create_char(7, [31, 17, 21, 21, 21, 21, 17, 31])
lcd.clear()
lcd.message = "RPI NOX game\nWelcome"



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
      
      if dirx == "Close":
        matrix[x, y]=2 # switch on the LED
        lcd.clear()
        #lcd.message('Hello\nworld!')
        lcd.message = "Square: \n" + str(w)
        #lcd.message = str(w)
      if dirx == "Open":
        matrix[x, y]=0 # switch off the LED
        lcd.clear()
        
      #display.write_display()
      print ("square", w, " Reed Switch " , dirx )   # chcol[(w+2)%3], (int((w-1)/3))+1
      
      mbrd[l]=a  # update the current state of the board
      time.sleep(1)
      
      # Turn off LCD backlights and clear text
      lcd.color = [0, 0, 0]
      
# Clear the display buffer.
lcd.clear()

#Clear Matrix
matrix.fill(0)



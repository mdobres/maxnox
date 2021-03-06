# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time
import board
import busio
from adafruit_ht16k33 import matrix

#  from PIL import Image
#  from PIL import ImageDraw

#from Adafruit_LED_Backpack import Matrix8x8
# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create display instance on default I2C address (0x70) and bus number.

#matrix = matrix.Matrix8x8(address=0x72, busnum=1)


# check using I2cdetect -y 1  to make sure the address is 70, if not edit the line above to change it
# the correct address
# Alternatively, create a display with a specific I2C address and/or bus.
# display = Matrix8x8.Matrix8x8(address=0x74, busnum=1)

# Initialize the display. Must be called once before using the display.
#display.begin()
#display.clear()

# creates a 8x8 matrix:
matrix = matrix.Matrix8x8(i2c, address=0x70)

# edges of an 3x3 matrix
col_max = 3
row_max = 3

# Clear the matrix.
matrix.fill(0)
col = 0
row = 0

q = True

while q:
        # Run through each pixel individually and turn it on.
        for xled in range(1,10):   # anodes numbers starts 1
                
            x =int((xled-1)/3)+1   # anodes numbers starts 1
            y =  (2+xled)%3   # cathodes number start 0
            
            matrix[x, y] = 2
            col += 1
            time.sleep(1)
            
            # Print Square Location
            print ("Square " ,xled)
            
            # Delay for half a second.
            time.sleep(1)
            
            if xled == row_max:
                
                q = False 
                

# Clear the display buffer.

matrix.fill(0)

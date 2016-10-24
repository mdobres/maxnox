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

#  from PIL import Image
#  from PIL import ImageDraw

from Adafruit_LED_Backpack import Matrix8x8


# Create display instance on default I2C address (0x70) and bus number.
display = Matrix8x8.Matrix8x8(address=0x70, busnum=1)
# check using I2cdetect -y 1  to make sure the address is 70, if not edit the line above to change it
# the correct address
# Alternatively, create a display with a specific I2C address and/or bus.
# display = Matrix8x8.Matrix8x8(address=0x74, busnum=1)

# Initialize the display. Must be called once before using the display.
display.begin()
display.clear()

while True:
        # Run through each pixel individually and turn it on.
        for xled in range(1,10):   # anodes numbers starts 1
                x =int((xled-1)/3)+1   # anodes numbers starts 1
                y =  (2+xled)%3   # cathodes number start 0
                # Clear the display buffer.
                display.clear()
                # Set pixel at position i, j to on.  To turn off a pixel set
                # the last parameter to 0.
                display.set_pixel(x, y, 1)
                # Write the display buffer to the hardware.  This must be called to
                # update the actual display LEDs
                print "Square " ,xled
                display.write_display()
                # Delay for half a second.
                time.sleep(3)



# Clear the display buffer.


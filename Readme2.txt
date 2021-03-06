Code revised by Fernando:

March 2021:

 the python_led_backpack and adafruit_python_charLCD libraries are no longer valid and the new ones do not work on python2 which is no longer supported. Therefore, I had to modify your code slightly to accommodate the new libraries and update the code for python3.
Here are the steps I followed for installing the new libraries from command screen (using linux commands).
1. Raspberry PI Preparation
>sudo apt-get update -y
>sudo apt-get upgrade -y

2. Enable the I2C Interface
>sudo raspi-config

a new screen will pop up. Here you will need to select I2C Enable

3. Install adafruit-blinka (to allow the adafruit libraries to work)
>pip3 install adafruit-blinka

4. Test the I2C Bus
>lsmod | grep -i i2c

here you should see:
i2c_bcm2835
i2c_dev

This indicates that the I2C module is working

5. Search for all peripheral address to make sure there are communicating with the I2C
>sudo i2cdetect -y 1

here you should see a matrix table similar to the one shown above by Max with 3 addressed (LCD is OX20, HT16K33 is OX70 and MCP23017 is OX21

6. Install the new HT16K33 library
>pip3 install adafruit-circuitpython-ht16k33

7. Install the new CharLCD library
>sudo pip3 install adafruit-circuitpython-charlcd

8. Test the LCD 16X2 using the adafruit file
charlcd_i2c_rgb_simpletest.py

The LCD test file is stored in your raspberry directory where the LCD library is installed. In my raspberry it is located as follows
/usr/local/lib/python3.7/dist-packages(6.2.2)

Once you have installed the proper libraries and run the updated test files the NOX game will work.

The main issues I had was with the reed switches that broke very easily and the sainmart LCD which has a very poor brightness. Apparently a resistor is not working properly. I also had the issue reported by Max with the HT16K33 address changing form OX70 to OX72. If you keep trying it will reset by itself or you can try the procedure mentioned by Max above. 
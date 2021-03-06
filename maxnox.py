# Tic-Tac-Toe
# Plays the game of tic-tac-toe against a human opponent
# Michael Dawson - 2/21/03

import smbus
import time
import math
import board
import busio
import os
import random

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

# Set LCD color Red on
lcd.color = [100, 0, 0]
time.sleep(1)

# Set LCD color Blue on
lcd.color = [0, 100, 0]
time.sleep(1)

# Set LCD color Green on
lcd.color = [0, 0, 100]
time.sleep(1)

# Set LCD color off
lcd.color = [0, 0, 0]
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
print (lcd.message)



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

 
# global constants
X = "X"
O = "O"
EMPTY = " "
TIE = "TIE"
NUM_SQUARES = 9

# Global variables for LCD Keypad
# Make list of button value, text, and backlight color.
buttons = ( (lcd.select_button, 'Shutdown', (1,1,1)),  # Select
            (lcd.left_button,   'No'  , (1,0,0)),    # Left
            (lcd.up_button,     'Yes'    , (0,0,1)),  # Up
            (lcd.down_button,   'No'  , (0,1,0)),   # Down
            (lcd.right_button,  'No' , (1,0,1)) )  # Right
level= 2 # expert
def ledon(sq):
        w=sq+1 # different numbering system
        x =int((w-1)/3)+1   # anodes numbers starts 1
        y =  (2+w)%3   # cathodes number start 0
        matrix[x, y]=2 # switch on the LED
        #display.set_pixel(x, y, 1)  # switch on the LED
        #display.write_display()

def ledoff(sq):
        w=sq+1 # different numbering system
        x =int((w-1)/3)+1   # anodes numbers starts 1
        y =  (2+w)%3   # cathodes number start 0
        matrix[x, y]=0 # switch off the LED
        #display.set_pixel(x, y, 0)  # switch on the LED
        #display.write_display()

def display_instruct():

    """Display game instructions."""
    lcd.clear()
    lcd.message = (' Noughts &\n Crosses')
    print (lcd.message)
    time.sleep(1)  #give time to read message
    for l in range(9):
        ledon(l)
        time.sleep(0.25)
        ledoff(l)
    return
    
def get_LCD_button(question):
    lcd.clear()
    lcd.message = (question)
    pressed = False
    print ("In " + str(question))
    time.sleep(1)  #give time to read message
    while pressed == False:
        # Loop through each button and check if it is pressed.
        if lcd.right_button:
            lcd.clear()
            lcd.message = "No"
            but= "No"
            time.sleep(1)  #give time to read message
            pressed = True
        
        if lcd.left_button:
            lcd.clear()
            lcd.message = "No"
            but= "No"
            time.sleep(1)  #give time to read message
            pressed = True
                
        if lcd.up_button:
            lcd.clear()
            lcd.message = "Yes"
            but= "Yes"
            time.sleep(1)  #give time to read message
            pressed = True
            
        if lcd.down_button:
            lcd.clear()
            lcd.message = "No"
            but= "No"
            time.sleep(1)  #give time to read message
            pressed = True
            
        if lcd.select_button:
            lcd.clear()
            lcd.message = "Shutdown"
            but= "Shutdown"
            time.sleep(1)  #give time to read message
            pressed = True
        
    print (but)
    return but # sends name back 

#def get_LCD_button(question):
#   lcd.clear()
#   lcd.message = (question)
#   pressed = False
#    print ("in Question")
#    time.sleep(1)  #give time to read message
#    while pressed == False:
        # Loop through each button and check if it is pressed.
#        for button in buttons:
#            if lcd.is_pressed(button[0]):
#                # Button is pressed, change the message and backlight.
#                lcd.clear()
#                lcd.message(button[1]) # prints button name
#                but=button[1]
#                time.sleep(1)  #give time to read message
#                pressed = True 
#    print (but)
#    return but # sends name back

def get_level():
    global level
    lcd.clear()  
    print ("In Level: " + str(level))
    chlev =["Beginner","Good","Expert"]  # level labels   
    while True:
            mess=" Level = "+str(chlev[level]) +"\n Yes or No?"
            getl = get_LCD_button(mess)
            if getl == "Shutdown": os.system("sudo shutdown -h now")
            if getl == "Yes": return
            level=(level+1)%3



    time.sleep(1)  #give time to read message
    while pressed == False:
        # Loop through each button and check if it is pressed.
        for button in buttons:
            if lcd.is_pressed(button[0]):
                # Button is pressed, change the message and backlight.
                lcd.clear()
                lcd.message(button[1]) # prints button name
                print (lcd.message)
                but=button[1]
                time.sleep(1)  #give time to read message
                pressed = True 
    print (but)
    return but # sends name back


    

def pieces():
    global mbrd 
    print ("pieces")
    # mbrd = [0xFF,0xFF] 
    """Determine if player or computer goes first."""
    go_first = get_LCD_button(" Yes to go 1st\n any other I go ")
    print (" go_first", go_first)
    if go_first == "Yes":
        lcd.clear()
        lcd.message = (' Yes\n')
        print (lcd.message)
        time.sleep(1) 
        human = X
        computer = O

    elif go_first == "Shutdown": os.system("sudo shutdown -h now")

    else:
        lcd.clear()
        lcd.message = (' Me to go first')
        print (lcd.message)
        time.sleep(1) 
        computer = X
        human = O
    return computer, human


def new_board():
    """Create new game board."""
    board = []
    for square in range(NUM_SQUARES):
        board.append(EMPTY)
    return board

def check_clear():
        global mbrd
        # checks that the board is clear before starting a game
        mbrd = [255, 255]   # mbrd is the noughts and crosses board  this sets them to 11111111 : open w
        clrboard = False
        while clrboard != True :
                clrboard = True 
                for l in range(2):  #loops round both registers of MCP23017
                    a = bus.read_byte_data(i2cadd,GPIOn[l])
                    if a != mbrd[l]: # there is a piece on the board
                                clrboard =False
                                lcd.clear()
                                lcd.message = ('  Please clear\n  The board')
                                print (lcd.message)
                                time.sleep(1)         
        lcd.clear()
        return

def legal_moves(board):
    """Create list of legal moves."""
    moves = []
    for square in range(NUM_SQUARES):
        if board[square] == EMPTY:
            moves.append(square)
    return moves

def make(move):
#Flash LED on square move +1 until registers
# light LED
            global mbrd           
            w2=10
            print ("led on move ", move)
            ledon(move)
           # time.sleep(1)
# Check to see if piece placed
            movecomp = False
            while movecomp != True :
                for l in range(2):  #loops round both registers of MCP23017
                    a = bus.read_byte_data(i2cadd,GPIOn[l])
                    if a != mbrd[l]: # there has been a change
                      c = a ^ mbrd[l]  # bitwise operation copies the bit if it is set in one operand but not both.
                      dirx = "Close"
                      if a > mbrd[l] : dirx = "Open"  # if the number gets bigger a 0 has changed to a 1
                      k = math.frexp(c)[1]  # calculates integer part of log base 2, which is binary bit position
                      w2=k-1+l*8          
                      if dirx == "Close" and w2 == move :
                              movecomp = True  # if the square is closed in the right place we're done
                              mbrd[l]=a  # update the current state of the board

            ledoff(move) # switch off the LED
            lcd.clear()
            lcd.message = ('    Thanks\n')
            print (lcd.message)
           
            
            return 

def winner(board):
    """Determine the game winner."""
    WAYS_TO_WIN = ((0, 1, 2),
                   (3, 4, 5),
                   (6, 7, 8),
                   (0, 3, 6),
                   (1, 4, 7),
                   (2, 5, 8),
                   (0, 4, 8),
                   (2, 4, 6))
    
    for row in WAYS_TO_WIN:
        if board[row[0]] == board[row[1]] == board[row[2]] != EMPTY:
            winner = board[row[0]]
            return winner

    if EMPTY not in board:
        return TIE

    return None

def human_move(board, human):
    global mbrd
    chcol =["A","B","C"]  # column labels
    print ("in Human Move")
    lcd.clear()
    lcd.message = (' Make Your Move')
    print (lcd.message)
    #time.sleep(1)  #give time to read message
    legal = legal_moves(board)
    move = None
    print ("start H " ,mbrd)
    while move not in legal:
      # read the 8 registers
      #lcd.clear()
      #lcd.message(' Make Your Move')
      #time.sleep(1)
      
      for l in range(2):  #loops round both registers of MCP23017
        a = bus.read_byte_data(i2cadd,GPIOn[l])
        if a != mbrd[l]: # there has been a change
            c = a ^ mbrd[l]  # bitwise operation copies the bit if it is set in one operand but not both.
            dirx = "Close"

            if a > mbrd[l] :
                dirx = "Open"  # if the number gets bigger a 0 has changed to a 1 a piece has been lifted
                lcd.clear()
                lcd.message = ('\nNo!, put it back')
                print (lcd.message)
                time.sleep(1)  #give time to read message
                lcd.clear()
                lcd.message = (' Make Your Move')
                print (lcd.message)
            else:
                y = math.frexp(c)[1]  # calculates integer part of log base 2, which is binary bit position
                move=y-1+l*8 # different from test prog as need numbers 0-8
                mbrd[l]=a  # update the current state of the board
   
    print ("Hmove " , move)
    ledon(move)
    time.sleep(1)
    ledoff(move)
    lcd.clear()
    
    lcd.message = (' Your move\n ')
    print (lcd.message)
    mess = chcol[move%3] + str(int(move/3)+1) 
    lcd.message = (mess)
    print (lcd.message)
    
    time.sleep(1)  #give time to read message
    return move

def ranmove():
        rmove=random.randint(0,8)
        return rmove


def computer_move(board, computer, human):
    global mbrd,level
    print ("in computer move.")
    # make a copy to work with since function will be changing list
    board = board[:]
    # the best positions to have, in order
    BEST_MOVES = (4, 0, 2, 6, 8, 1, 3, 5, 7)


    lcd.clear()
    lcd.message = (' Making my Move\n Place piece')
    print (lcd.message)
    time.sleep(1)  #give time to read message

    # Idiot level moves randomly ignores win
    if level==0:
            while True:
                    move= random.randint(0,8)
                    if move in legal_moves(board):
                            print (move)
                            make(move)
                            return move
   
    # if computer can win, take that move
    for move in legal_moves(board):
        board[move] = computer
        if winner(board) == computer:
            print (move)
            make(move)
            return move
        # done checking this move, undo it
        board[move] = EMPTY

    # if human can win, block that move
    for move in legal_moves(board):
        board[move] = human
        if winner(board) == human:
            print (move)
            make(move)
            return move
        # done checkin this move, undo it
        board[move] = EMPTY

# good level, blocks your winning move, but then moves randomly
    if level==1:
            while True:
                    move= random.randint(0,8)
                    if move in legal_moves(board):
                            print (move)
                            make(move)
                            return move

    # since no one can win on next move, pick best open square
    for move in BEST_MOVES:
        if move in legal_moves(board):
            print (move)
            make(move)
            return move
def next_turn(turn):
    """Switch turns."""
    if turn == X:
        return O
    else:
        return X

    
def congrat_winner(the_winner, computer, human):
    """Congratulate the winner."""
    lcd.clear()
    if the_winner != TIE:       
        lcd.message = ("won!\n")
        print (lcd.message)
        
    else:
           lcd.message = ("It's a tie!\n")
           print (lcd.message)

    if the_winner == computer:
        
           lcd.message = ("I Win!!!!")
           print (lcd.message)

    elif the_winner == human:
        
       lcd.message = ("No, no! You won!")
       print (lcd.message)
       
    elif the_winner == TIE:
        
        lcd.message = ("Its a Tie!")
        print (lcd.message)
        
    time.sleep(1)  #give time to read message       

def main():
        global mbrd
        while True:
            display_instruct()
        
            check_clear()
            print ("Start After Clear " ,mbrd)
            get_level()
            computer, human = pieces()
            turn = X
            board = new_board()
            

            while not winner(board):
                if turn == human:
                    move = human_move(board, human)
                    board[move] = human
                else:
                    move = computer_move(board, computer, human)
                    board[move] = computer
            
                turn = next_turn(turn)

            the_winner = winner(board)
            congrat_winner(the_winner, computer, human)


# start the program
main()
# raw_input("\n\nPress the enter key to quit.")


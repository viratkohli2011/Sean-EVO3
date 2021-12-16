## Imports
from ev3dev2 import *
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sound import Sound
from time import sleep
import os

os.system('setfont Lat15-TerminusBold14')

motorLeft = LargeMotor('outB'); motorLeft.stop_action = 'hold'
motorRight = LargeMotor('outC'); motorRight.stop_action = 'hold'

leftSensor = ColorSensor(INPUT_3)
rightSensor = ColorSensor(INPUT_2)

sound = Sound()

## Functions

# This function takes inputs of LOCATION and BOARD and returns a list of potential new spaces
def get_nei(board, cur_loc, last_loc, gold, gold_loc,all_loc,found):
    neighbors = []
    xloc = cur_loc[0]
    yloc = cur_loc[1]
    new = (0,0)


    for val in board.keys():
        if board[val] == (0,0,0) and new == (0,0):
            new = val
        if all_loc.count(val) > 3 and all_loc.count(cur_loc)>0:
            loop = True
        else: 
            loop = False

    # Regular movement before Gold is found

    if not gold:
        if yloc < 3:
            neighbors.append((xloc,(yloc+1)))
        if xloc < 3:
            neighbors.append(((xloc+1),yloc))
        if yloc > 0:
            neighbors.append((xloc,(yloc-1)))
        if xloc > 0:
            neighbors.append(((xloc-1),yloc))
        
        if last_loc in neighbors:
            neighbors.remove(last_loc)
            neighbors.append(last_loc)

        if all_loc.count(cur_loc)>3:
            for nei in neighbors:
                if all_loc.count(nei) < 1:
                    neighbors.remove(nei)
                    neighbors.insert(0,nei)

        return neighbors

    
    # When Gold is found pathfind back home
    elif found:
        if xloc > 0:
                neighbors.append((xloc-1,yloc))
        if yloc > 0:
                neighbors.append((xloc,yloc-1))
        if gold_loc[0] == xloc:
            if (xloc-1,yloc) in neighbors and (xloc-1,yloc) in neighbors:
                neighbors.remove((xloc-1,yloc))
                neighbors.append((xloc-1,yloc))
        if yloc < 3:        
            neighbors.append((xloc,yloc+1))
        if xloc < 3:
            neighbors.append((xloc+1,yloc))

        if last_loc in neighbors:
            neighbors.remove(last_loc)
            neighbors.append(last_loc)

        return neighbors
    
    # If detects looping, find new place to pathfind to
    elif loop and not gold:
        print("looping")
        if new[0]<=xloc and new[1]<=yloc:
            print(1)
            if xloc > 0:
                neighbors.append((xloc-1,yloc))
            if yloc > 0:
                neighbors.append((xloc,yloc-1))
            if new[0] == xloc:
                if (xloc-1,yloc) in neighbors and (xloc-1,yloc) in neighbors:
                    neighbors.remove((xloc-1,yloc))
                    neighbors.append((xloc-1,yloc))
            if yloc < 3:        
                neighbors.append((xloc,yloc+1))
            if xloc < 3:
                neighbors.append((xloc+1,yloc))
                
        elif new[0]>=xloc and new[1]>=yloc:
            print(2)
            if xloc < 3:
                neighbors.append((xloc+1,yloc))
            if yloc < 3: 
                neighbors.append((xloc,yloc+1))
            if new[0] == xloc:
                if new[0] == xloc and (xloc+1,yloc) in neighbors:
                    neighbors.remove((xloc+1,yloc))
                    neighbors.append((xloc+1,yloc))
            if yloc > 0:    
                neighbors.append((xloc,yloc-1))
            if xloc > 0:
                neighbors.append((xloc-1,yloc))
            
        

        elif new[0]<=xloc and new[1]>=yloc:
            print(3)
            if xloc > 0:
                neighbors.append((xloc-1,yloc))
            if yloc < 3:
                neighbors.append((xloc,yloc+1))
            if new[0] == xloc:
                if (xloc-1,yloc) in neighbors and (xloc-1,yloc) in neighbors:
                    neighbors.remove((xloc-1,yloc))
                    neighbors.append((xloc-1,yloc))
            if yloc < 3:
                neighbors.append((xloc,yloc+1))
            if xloc < 3:
                neighbors.append((xloc+1,yloc))

        elif new[0]>=xloc and new[1]<=yloc:
            print(4)
            if xloc < 3:
                neighbors.append((xloc+1,yloc))
            if yloc > 0:
                neighbors.append((xloc,yloc-1))
            if new[0] == xloc and (xloc+1,yloc) in neighbors:
                if (xloc+1,yloc) in neighbors:
                    neighbors.remove((xloc+1,yloc))
                    neighbors.append((xloc+1,yloc))
            if yloc < 3:
                neighbors.append((xloc,yloc+1))
            if xloc < 3:
                neighbors.append((xloc+1,yloc))
        return neighbors




    # When Gold is found: Gold pathfinding
    else:
        #print("board:{} cur_loc:{} all_loc:{} gold:{} gold_loc:{}".format(board,cur_loc,last_loc,gold,gold_loc))
        if gold_loc[0]<=xloc and gold_loc[1]<=yloc:
            print(1)
            if xloc > 0:
                neighbors.append((xloc-1,yloc))
            if yloc > 0:
                neighbors.append((xloc,yloc-1))
            if gold_loc[0] == xloc:
                if (xloc-1,yloc) in neighbors and (xloc-1,yloc) in neighbors:
                    neighbors.remove((xloc-1,yloc))
                    neighbors.append((xloc-1,yloc))
            if yloc < 3:        
                neighbors.append((xloc,yloc+1))
            if xloc < 3:
                neighbors.append((xloc+1,yloc))
                
        elif gold_loc[0]>=xloc and gold_loc[1]>=yloc:
            print(2)
            if xloc < 3:
                neighbors.append((xloc+1,yloc))
            if yloc < 3: 
                neighbors.append((xloc,yloc+1))
            if gold_loc[0] == xloc:
                if gold_loc[0] == xloc and (xloc+1,yloc) in neighbors:
                    neighbors.remove((xloc+1,yloc))
                    neighbors.append((xloc+1,yloc))
            if yloc > 0:    
                neighbors.append((xloc,yloc-1))
            if xloc > 0:
                neighbors.append((xloc-1,yloc))
            
        
        elif gold_loc[0]<=xloc and gold_loc[1]>=yloc:
            print(3)
            if xloc > 0:
                neighbors.append((xloc-1,yloc))
            if yloc < 3:
                neighbors.append((xloc,yloc+1))
            if gold_loc[0] == xloc:
                if (xloc-1,yloc) in neighbors and (xloc-1,yloc) in neighbors:
                    neighbors.remove((xloc-1,yloc))
                    neighbors.append((xloc-1,yloc))
            if yloc < 3:
                neighbors.append((xloc,yloc+1))
            if xloc < 3:
                neighbors.append((xloc+1,yloc))

        elif gold_loc[0]>=xloc and gold_loc[1]<=yloc:
            print(4)
            if xloc < 3:
                neighbors.append((xloc+1,yloc))
            if yloc > 0:
                neighbors.append((xloc,yloc-1))
            if gold_loc[0] == xloc and (xloc+1,yloc) in neighbors:
                if (xloc+1,yloc) in neighbors:
                    neighbors.remove((xloc+1,yloc))
                    neighbors.append((xloc+1,yloc))
            if yloc < 3:
                neighbors.append((xloc,yloc+1))
            if xloc < 3:
                neighbors.append((xloc+1,yloc))
        return neighbors


# This function updates a location with new values for breeze
def update_breeze(board, loc, breeze):
    if board[loc][0] == -1:
        pass

    elif board[loc][0] == 2:
        board[loc][1] = -1
        board[loc][2] = -1

    elif board[loc][0] == 1 and breeze == 1:
        board[loc][0] = 2
        board[loc][1] = -1
        board[loc][2] = -1
              
    else:
        board[loc][0] = breeze

# This function updates a location with new values for stench
def update_stench(board, loc, stench):  
    if board[loc][1] == -1:
        pass
    
    elif board[loc][1] == 2:
        board[loc][0] = -1
        board[loc][2] = -1

    elif board[loc][1] == 1 and stench == 1:
        board[loc][1] = 2
        board[loc][0] = -1
        board[loc][2] = -1
    else:
        board[loc][1] = stench
        
# This function updates a location with new values for glitter
def update_glitter(board, loc, glitter):
    if board[loc][2] == -1:
        pass

    elif board[loc][2] == 2:
        board[loc][0] = -1
        board[loc][1] = -1

    elif board[loc][2] == 1 and glitter == 1:
        board[loc][2] = 2
        board[loc][1] = -1
        board[loc][0] = -1
    else:
        board[loc][2] = glitter



## MOVE FUNCTIONS

def correction() :
    offset = True

    while offset :

        leftLV = leftSensor.reflected_light_intensity
        rightLV = rightSensor.reflected_light_intensity
        threshold = abs(leftLV - rightLV)

        #print(leftLV, rightLV, threshold)
        if (leftSensor.reflected_light_intensity > 22 or rightSensor.reflected_light_intensity > 22) and \
        abs(leftSensor.reflected_light_intensity - rightSensor.reflected_light_intensity) < 10:
            motorLeft.off()
            motorRight.off()
            offset = False

        elif leftSensor.reflected_light_intensity > rightSensor.reflected_light_intensity and\
            abs(leftSensor.reflected_light_intensity - rightSensor.reflected_light_intensity) > 10 :
            motorLeft.off()
            motorRight.off()

            while abs(leftSensor.reflected_light_intensity - rightSensor.reflected_light_intensity) > 10 :
                motorRight.on(18)

            motorRight.off()
            #print("left white, first fix")

            motorLeft.on(5)
            motorRight.on(5)

            while (leftSensor.reflected_light_intensity < 22 or rightSensor.reflected_light_intensity < 22) and \
            abs(leftSensor.reflected_light_intensity - rightSensor.reflected_light_intensity) < 10 :
                #print(leftSensor.reflected_light_intensity, rightSensor.reflected_light_intensity)
                continue
            motorLeft.off()
            motorRight.off()

            while leftSensor.reflected_light_intensity < rightSensor.reflected_light_intensity and\
            abs(leftSensor.reflected_light_intensity - rightSensor.reflected_light_intensity) > 10 :
                motorRight.on(18)
             
            motorRight.off()
            #print("left now black, second fix")

            offset = False

        elif rightSensor.reflected_light_intensity > leftSensor.reflected_light_intensity and\
            abs(leftSensor.reflected_light_intensity - rightSensor.reflected_light_intensity) > 10 :
            motorLeft.off()
            motorRight.off()

            while abs(leftSensor.reflected_light_intensity - rightSensor.reflected_light_intensity) > 10 :
                motorLeft.on(18)
                
            motorLeft.off()
            #print("right white, first fix")

            motorLeft.on(5)
            motorRight.on(5)

            
                
            while (leftSensor.reflected_light_intensity < 22 or rightSensor.reflected_light_intensity < 22) and \
            abs(leftSensor.reflected_light_intensity - rightSensor.reflected_light_intensity) < 10 :
                #print(leftSensor.reflected_light_intensity, rightSensor.reflected_light_intensity)
                continue
            motorLeft.off()
            motorRight.off()

            while rightSensor.reflected_light_intensity < leftSensor.reflected_light_intensity and\
            abs(leftSensor.reflected_light_intensity - rightSensor.reflected_light_intensity) > 10 :
                motorLeft.on(18)

            motorLeft.off()
            #print("right now black, second fix")

            offset = False

def forwards() :
    motorLeft.on(28)
    motorRight.on(28)
    correction()
    motorLeft.run_to_rel_pos(position_sp= 600, speed_sp = 280)
    motorRight.run_to_rel_pos(position_sp= 600, speed_sp = 280)
    motorLeft.wait_while('running')
    motorRight.wait_while('running')

def rotate90(direction) :
    motorLeft.on(-35 * direction)
    motorRight.on(35 * direction)
    sleep(.47) #time for 90
    motorLeft.off()
    motorRight.off()

def rotate180(direction) :
    motorLeft.on(-35 * direction)
    motorRight.on(35 * direction)
    sleep(1) #time for 180
    motorLeft.off()
    motorRight.off()

# This function finds the next direction the robot needs to face based on the current one
def getNextDir(cur_loc, next_loc):
    if cur_loc[0] < next_loc[0]:
        return 1
    elif cur_loc[0] > next_loc[0]:
        return 3
    elif cur_loc[1] > next_loc[1]:
        return 2
    elif cur_loc[1] < next_loc[1]:
        return 0


def Move(cur_loc,next_loc,dire):
    next_dir = getNextDir(cur_loc, next_loc)
    if dire == next_dir:
        pass
    elif dire-next_dir == -1 or (dire-next_dir == 3 and dire == 3) :
        # Rotate one to right
        rotate90(-1)
    elif abs(dire -next_dir) == 2:
        # Do 180
        rotate180(-1)
    elif abs(dire-next_dir) == 1 or abs(dire-next_dir) == 3:
        # Rotate one to left
        rotate90(1)

    # MOVE FORWARD 1
    forwards()

    return next_dir

def Rot(cur_loc, next_loc, dire) :
    next_dir = getNextDir(cur_loc, next_loc)
    if dire == next_dir:
        pass
    elif dire-next_dir == -1 or (dire-next_dir == 3 and dire == 3):
        # Rotate one to right
        rotate90(-1)
    elif abs(dire-next_dir) == 2:
        # Do 180
        rotate180(-1)
    elif abs(dire-next_dir) == 1 or abs(dire-next_dir) == 3:
        # Rotate one to left
        rotate90(1)
        
    return next_dir

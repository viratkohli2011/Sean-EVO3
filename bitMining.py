#!/usr/bin/env python3
## main.py contains the main loop for our Wumpus Robotics program

from funcs import *




# Definitions
board = {(0,0): [-1,-1,-1], (0,1): [-1,-1,-1], (0,2): [0,0,0], (0,3): [0,0,0], \
    (1,0): [-1,-1,-1], (1,1): [0,0,0], (1,2): [0,0,0], (1,3): [0,0,0], \
    (2,0): [0,0,0],(2,1): [0,0,0],(2,2): [0,0,0],(2,3): [0,0,0],\
    (3,0): [0,0,0],(3,1): [0,0,0],(3,2): [0,0,0],(3,3): [0,0,0]}
    
# Current Location
cur_loc = (0,0)

# Current Direction 
cur_dir = 0

# List of all past locations
all_loc = [(0,0)]

# checks if gold has been located
gold = False
found = False
wumpus = False
spoken = False
wump_finished = False
just_murdered = False
gold_loc = (0,0)

# Signal meanings
Bsig = [1, 3, 5, 7, 9, 11]
Ssig = [2, 3, 6, 7, 10, 11]
Gsig = [4, 5, 6, 7]



# MOVE FORWARD 1

# Gold Finding Loop
print("My name is SEAN; I'm here to kick ass and find gold, and I'm all out of gold.")
sound.speak("My name is SEAN")
sleep(.5)
while True:
    if gold and gold_loc == cur_loc:
        found = True

    if found and cur_loc == (0,0):
        break    
    
    if len(get_nei(board,cur_loc,all_loc[-1],gold,gold_loc,all_loc,found)) == 0:
        print("No More Valid Spaces to Move")
        #print("board:{} cur_loc:{} all_loc:{} gold:{} gold_loc:{}".format(board,cur_loc,all_loc[-1],gold,gold_loc))

    for nei in get_nei(board,cur_loc,all_loc[-1],gold,gold_loc,all_loc,found):
        if board[nei][0]<1 and board[nei][1]<1:
            all_loc.append(cur_loc)
            cur_loc = nei
            print(cur_loc)
            cur_dir = Move(all_loc[-1],cur_loc,cur_dir)
            if wumpus:
                if wump_loc in get_nei(board,cur_loc,(0,0),False,gold_loc,all_loc,False):
                    # Turn toward wumpus
                    cur_dir=Rot(cur_loc, wump_loc,cur_dir)
                    print("Fire at {}!".format(wump_loc))
                    sound.speak("Fire! DIE WUMPUS")
                    for val in board:
                        board[val][1] = -1
                        board[wump_loc] = [-1,-1,-1]
                    wump_finished = True
                    wumpus = False
                    just_murdered = True

            #print(board)
            #print("Gold_loc: {}".format(gold_loc))
            break
    
    

    
    if not found and cur_loc not in all_loc:
        signal = int(input("What is the Input? ==> "))
        if signal == 999:
            print(board)
            signal = int(input("What is the Input? ==> "))
    
    elif not found and cur_loc in all_loc:
        signal = -20

    elif just_murdered:
        signal = -20
        just_murdered = False
    
    else:
        for val in board:
            if board[val][0] == 0:
                board[val][0] = 2
        print(board)
        signal = 1



    # Set all neighbors to hazard or glitter values
    if cur_loc not in all_loc:
        for nei in get_nei(board,cur_loc,(0,0),False,gold_loc,all_loc,False):
            if signal >= 8:
                found = True

            if signal == 0:
                update_breeze(board,nei,-1)
                update_stench(board,nei,-1)
                update_glitter(board,nei,-1)

            if signal in Ssig:
                update_stench(board,nei,1)
            elif signal == -20:
                pass
                
            else: 
                update_stench(board,nei,-1)

            if signal in Gsig:
                update_glitter(board,nei,1)
            elif signal == -20:
                pass

            else:
                update_glitter(board,nei,-1)
                
            if signal in Bsig:
                update_breeze(board,nei,1)
            elif signal == -20:
                pass
            else: 
                update_breeze(board,nei,-1)


            if board[nei][0] ==2:
                update_stench(board,nei,-1)
                update_glitter(board,nei,-1)

            if board[nei][1] ==2:
                update_breeze(board,nei,-1)
                update_glitter(board,nei,-1)

            if board[nei][2] ==2:
                update_breeze(board,nei,-1)
                update_stench(board,nei,-1)

    if found and not spoken:
        print("GOLD FOUND {}".format(gold_loc))
        sound.speak("GOT THE GOLD! WOOOOOOOOOO HOOOOOOOOOO! LETS GET THIS BREAD!")
        spoken = True

    if found:
        for val in board:
            if board[val][0] != -1:
                board[val][0] = 2
            
    if wump_finished:
        board[wump_loc] = [-1,-1,-1]


    #print("1: (0,2):{} (1,3):{}".format(board[(0,2)],board[(1,3)]))

    scount = 0
    sval = (0,0)
    gval = (0,0)
    gcount = 0    
    for val in board:
        if board[val][1] == 1:
            sval = val
            scount += 1
            
        if board[val][2] == 1:
            gval = val
            gcount += 1

    #print("2: (0,2):{} (1,3):{}".format(board[(0,2)],board[(1,3)]))
            
    for val in board:
        if board[val][1] == 2:
            sval = val
            scount = 1
        if board[val][2] == 2:
            gval = val
            gcount = 1
    
    # If there is only one potential Wumpus or gold location, then that location is absolute

    #print("3: (0,2):{} (1,3):{}".format(board[(0,2)],board[(1,3)]))

    if scount == 1:
        for val in board:
            board[val][1]=-1
        board[sval][1] = 2
        board[gval][0] = -1
        board[gval][1] = -1

        wumpus = True
        wump_loc = sval


    if gcount == 1:
        for val in board:
            board[val][2]=-1
        board[gval][2] = 2
        board[gval][0] = -1
        board[gval][1] = -1

        gold = True
        gold_loc = gval
    
    #print("4: (0,2):{} (1,3):{}".format(board[(0,2)],board[(1,3)]))

print("WE ARE HOME!")
sound.speak("Hurrah! WE ARE HOME!")
                
    
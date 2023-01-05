from machine import Pin
import utime
import _thread
import ledMatrix
import random
import sys
import math

fall_wait = 1
w,h = 8,8
h_offset = 3
mtx = [[0]*w for _ in range(h+h_offset)]
sumMtx = []

lock = _thread.allocate_lock()

buttonR = Pin(16,Pin.IN,Pin.PULL_DOWN)
buttonL = Pin(17,Pin.IN,Pin.PULL_DOWN)
buttonU = Pin(18,Pin.IN,Pin.PULL_DOWN)

shapes = [
        [
            [0,1,0],
            [1,1,1]
        ],
        [
            [1,0,0],
            [1,1,1]
        ],
        [
            [0,0,1],
            [1,1,1]
        ],
        [
            [1,1,1,1]
        ],
        [
            [1,1],
            [1,1]
        ]
    ]

def Copy(matrix):
    mtxOut = []
    for row in matrix:
        newrow = []
        for el in row:
            newrow.append(el)
        mtxOut.append(newrow)
    return mtxOut

mtx_screenshot = Copy(mtx)

def gameOver():
    print("Game Over")

def printMtx(matrix):
    for i in range(h_offset):
        for j in matrix[i]:
            if j:
                print(j,end="")
            else:
                print('.',end="")
        print()
    for i in range(h):
        for j in matrix[i+h_offset]:
            print(j,end="")
        print()
    print()
    
def displayMtx(matrix):
    ledMatrix.Input([matrix[i] for i in range(h_offset,h+h_offset)])

def Place():
    shape = shapes[random.randint(0,len(shapes)-1)]
    x = random.randint(0,w - len(shape[0]))
    y = h_offset-len(shape)
    for i, row in enumerate(shape):
        for j,el in enumerate(row):
            if el:
                mtx[i+y][j+x] = 1
    return [y,x],shape

def Forge(mtx1,mtx2):
    forgedMtx = [[0]*w for _ in range(h+h_offset)]
    for i,row in enumerate(forgedMtx):
        for j,_ in enumerate(row):
            if mtx1[i][j] == 1 or mtx2[i][j] == 1:
                forgedMtx[i][j] = 1
            else:
                forgedMtx[i][j] = 0
    return forgedMtx

def Validate(mtx,tempMtx):
    global mtx_screenshot
    mcount = 0 #number of 1's in the real matrix
    tcount = 0 #number of 1's in the temp matrix 
    for i in mtx:
        mcount += i.count(1)
    for j in tempMtx:
        tcount += j.count(1)
    if mcount < tcount:   # we lost 1's ==> we clipped into something
       return False
    return True

def main():
    global mtx
    global mtx_screenshot
    global sumMtx
    print('tetris time')
    pos,shape = Place()
    rot_state = 0
    
    urelease = True
    
    sumMtx = Forge(mtx,mtx_screenshot)
    displayMtx(sumMtx)
    printMtx(sumMtx)
    
    last_interrupt = utime.ticks_ms()
    
    _thread.start_new_thread(ledMatrix.main,())
    while True:
        #-----------//rotate//-----------
        if buttonU.value() and urelease:
            urelease = False
            tempMtx = Copy(mtx)     #saving matrix state
            
            shape_center = [len(shape)/2,len(shape[0])/2] # y,x
            actual_center = [pos[0]+shape_center[0],pos[1]+shape_center[1]] # y,x
            rotated_shape = [[0]*len(shape) for _ in range(len(shape[0]))]
            
            print(pos, shape_center, actual_center)
            square_pos = []
            for i,row in enumerate(shape):
                for j,square in enumerate(row):
                    if square == 1:
                        #finding the position of the 1's
                        square_pos.append([i+0.5-shape_center[0],j+0.5-shape_center[1]])    #y-distance, x-distance
            new_square_pos = []
            for el in square_pos:
                new_square_pos.append([el[1] + 0.5,el[0]*-1+0.5]) # this is the rotated matrix(basically flipping the positions: y --> x and x --> y, after that multipliing the second element with -1))
            #making the changes
            for square in square_pos:
                print(actual_center,square)
                #print(int(actual_center[0]+square[0]-0.5),int(actual_center[1]+square[1]-0.5))
                try:
                    mtx[int(actual_center[0]+square[0]-0.5)][int(actual_center[1]+square[1]-0.5)] = 0
                except:
                    pass
            print()
            for i,square in enumerate(new_square_pos):
                try:
                    mtx[int(actual_center[0]+square[0]-0.5)][int(actual_center[1]+square[1]-0.5)] = 1
                    rotated_shape[int(shape_center[1]+square[0]-0.5)][int(shape_center[0]+square[1]-0.5)] = 1   #preparing shape for next rotation
                except:
                    pass
                print(actual_center,square)
                
            if Validate(Forge(mtx, mtx_screenshot),sumMtx) == False: # validating move, if INVALID then dont make that move
                mtx = Copy(tempMtx) #reloading matrix previous state
            else:    
                pos = [int(actual_center[0]+((0+0.5-shape_center[1]) + 0.5)-0.5),int(actual_center[1]+((len(shape)-1+0.5-shape_center[0])*-1+0.5)-0.5)] # fixing position
                shape = Copy(rotated_shape)
                #print()
                #print(((0+0.5-shape_center[1]) + 0.5))
                #print(((len(rotated_shape)-1+0.5-shape_center[0])*-1+0.5))
                #print(pos)
            #print(shape)
            #while buttonU.value():pass
            #while buttonU.value() == 0:pass
            
            sumMtx = Forge(mtx,mtx_screenshot)
            printMtx(sumMtx)
            displayMtx(sumMtx)
        elif buttonU.value() == 0 and urelease == False:
            print('a')
            urelease = True
            
        #-----------//left//-----------
        if buttonL.value():
            tempMtx = Copy(mtx)     #saving matrix state
            pos[1] -= 1
            for i in range(len(mtx)):
                mtx[i].pop(0)
                mtx[i].append([0]*w)
            if Validate(Forge(mtx, mtx_screenshot),sumMtx) == False: # validating move, if INVALID then dont make that move
                mtx = Copy(tempMtx) #reloading matrix previous state
                pos[1] += 1
            sumMtx = Forge(mtx,mtx_screenshot)
            printMtx(sumMtx)
            displayMtx(sumMtx)
            while buttonL.value():pass

        #-----------//right//-----------
        if buttonR.value():
            tempMtx = Copy(mtx)     #saving matrix state
            pos[1] += 1 
            for i in range(len(mtx)):
                mtx[i].pop(len(mtx[i])-1)
                mtx[i].insert(0,[0]*w)
            if Validate(Forge(mtx,mtx_screenshot),sumMtx) == False: # validating move, if INVALID then dont make that move
                mtx = Copy(tempMtx) #reloading matrix previous state
                pos[1] -= 1
            sumMtx = Forge(mtx,mtx_screenshot)
            printMtx(sumMtx)
            displayMtx(sumMtx)
            while buttonR.value():pass
        #-----------//falling//-----------
        if utime.ticks_diff(utime.ticks_ms(),last_interrupt) > fall_wait * 1000:
            pos[0] += 1
            tempMtx = Copy(mtx)     #saving matrix state
            mtx.pop(len(mtx)-1) #take the last element out
            mtx.insert(0,[0]*w) #put an empty row in the front of the matrix
            if Validate(Forge(mtx,mtx_screenshot),sumMtx) == False :
                mtx = Copy(tempMtx) #reloading matrix previous state
                mtx_screenshot = Forge(mtx,mtx_screenshot)
                pos[0] -= 1
                #print("invalid fall")
                if 1 in mtx_screenshot[h_offset]:
                    gameOver()
                    ledMatrix.Input([])
                    utime.sleep(1)
                    return
                for i in range(len(mtx)):
                    mtx[i] = [0]*w
                for i,row in enumerate(mtx_screenshot): #enumerating mtx_screenshot rows
                    if 0 not in row: #row is full
                        mtx_screenshot.pop(i) #take the full row out
                        mtx_screenshot.insert(0,[0]*w) #put an empty row in the front of the matrix
                pos,shape = Place()

            sumMtx = Forge(mtx,mtx_screenshot)
            printMtx(sumMtx)
            displayMtx(sumMtx)
            last_interrupt = utime.ticks_ms()

if __name__ == "__main__":
    main()
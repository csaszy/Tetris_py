import time
import copy
import keyboard

w,h = 5,10
h_offset = 2
mtx = [[0]*w for _ in range(h+h_offset)]
sumMtx = copy.deepcopy(mtx)

def printMtx():
    for i in range(h):
        print(sumMtx[i+h_offset])
    print()    

def Place(x,y):
    mtx[y][x] = 1

def Validate(mtx,tempMtx):
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
    mtx_screenshot = copy.deepcopy(mtx)
    Place(1,2)
    while True:
        #-----------//left//-----------
        if keyboard.is_pressed("a"): 
            for i in range(len(mtx)):
                tempMtx = copy.deepcopy(mtx)     #saving matrix state
                mtx[i].pop(0)
                mtx[i].append([0]*w)
                if Validate(mtx,tempMtx) == False: # validating move, if INVALID then dont make that move
                    mtx = copy.deepcopy(tempMtx) #reloading matrix previous state

        #-----------//right//-----------
        if keyboard.is_pressed("d"): 
            for i in range(len(mtx)):
                tempMtx = copy.deepcopy(mtx)     #saving matrix state
                mtx[i].pop(len(mtx[i])-1)
                mtx[i].insert(0,[0]*w)
                if Validate(mtx,tempMtx) == False: # validating move, if INVALID then dont make that move
                    mtx = copy.deepcopy(tempMtx) #reloading matrix previous state

        #-----------//falling//-----------
        tempMtx = copy.deepcopy(mtx)     #saving matrix state
        mtx.pop(len(mtx)-1) #take the last element out
        mtx.insert(0,[0]*w) #put an empty row in the front of the matrix
        if Validate(mtx,tempMtx) == False: # validating move, if INVALID then dont make that move
            mtx = copy.deepcopy(tempMtx) #reloading matrix previous state
            mtx_screenshot = copy.deepcopy(mtx)
            print("invalid fall")
            for i in range(len(mtx)):
                mtx[i] = [0]*w
            Place(1,2)

        for i,row in enumerate(sumMtx):
            for j,_ in enumerate(row):
                if mtx[i][j] == 1 or mtx_screenshot[i][j] == 1:
                    sumMtx[i][j] = 1
                else:
                    sumMtx[i][j] = 0
        printMtx()
        time.sleep(0.5)

if __name__ == "__main__":
    main()
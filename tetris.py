import time
import copy
import keyboard

w,h = 5,10
h_offset = 3
mtx = [[0]*w for _ in range(h+h_offset)]
mtx_screenshot = copy.deepcopy(mtx)

def gameOver():
    print("Game Over")
    while True: 
        pass

def printMtx(matrix):
    for i in range(h):
        print(matrix[i+h_offset])
    print()    

def Place(x,y):
    mtx[y][x] = 1

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
    Place(1,2)
    sumMtx = Forge(mtx,mtx_screenshot)

    while True:
        #-----------//left//-----------
        if keyboard.is_pressed("a"): 
            for i in range(len(mtx)):
                tempMtx = copy.deepcopy(mtx)     #saving matrix state
                mtx[i].pop(0)
                mtx[i].append([0]*w)
                if Validate(Forge(mtx, mtx_screenshot),sumMtx) == False: # validating move, if INVALID then dont make that move
                    mtx = copy.deepcopy(tempMtx) #reloading matrix previous state

        #-----------//right//-----------
        if keyboard.is_pressed("d"): 
            for i in range(len(mtx)):
                tempMtx = copy.deepcopy(mtx)     #saving matrix state
                mtx[i].pop(len(mtx[i])-1)
                mtx[i].insert(0,[0]*w)
                if Validate(Forge(mtx,mtx_screenshot),sumMtx) == False: # validating move, if INVALID then dont make that move
                    mtx = copy.deepcopy(tempMtx) #reloading matrix previous state

        #-----------//falling//-----------
        tempMtx = copy.deepcopy(mtx)     #saving matrix state
        mtx.pop(len(mtx)-1) #take the last element out
        mtx.insert(0,[0]*w) #put an empty row in the front of the matrix
        if Validate(Forge(mtx,mtx_screenshot),sumMtx) == False :
            mtx = copy.deepcopy(tempMtx) #reloading matrix previous state
            mtx_screenshot = Forge(mtx,mtx_screenshot)
            #print("invalid fall")
            if 1 in mtx_screenshot[h_offset]:
                gameOver()
            for i in range(len(mtx)):
                mtx[i] = [0]*w
            while 0 not in mtx_screenshot[len(mtx_screenshot)-1]: #last row is full
                mtx_screenshot.pop(len(mtx)-1) #take the last element out
                mtx_screenshot.insert(0,[0]*w) #put an empty row in the front of the matrix
            Place(1,2)

        sumMtx = Forge(mtx,mtx_screenshot)

        printMtx(sumMtx)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
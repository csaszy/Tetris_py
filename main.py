import time
mtx = []
cols = 10
rows = 20

bg=" "
cube="#"
#----------------------------------------------------------------
def main():
    gen()
    while True:
        Update()
        time.sleep(1)
#----------------------------------------------------------------
def gen():
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(bg)
        mtx.append(row)
#----------------------------------------------------------------
def Update():
    for row in mtx:
        for col in row:
            print(bg,end="")
        print("")
    print("")
#----------------------------------------------------------------
if __name__ == "__main__":
    main()
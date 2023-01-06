from machine import Pin
import machine
import utime
import ledMatrix
import tetris
import sys

buttonR = Pin(16,Pin.IN,Pin.PULL_DOWN)
buttonL = Pin(17,Pin.IN,Pin.PULL_DOWN)
buttonU = Pin(18,Pin.IN,Pin.PULL_DOWN)

led = Pin(25,Pin.OUT)

if __name__ == '__main__':
    led.value(1)
    while buttonR.value() == 0 and buttonL.value() == 0 and buttonU.value() == 0:pass
    led.value(0)
    if buttonR.value():
        sys.exit()
    if buttonL.value():
        ledMatrix.Write("tetris")
    score = tetris.main()
    print(score)
    ledMatrix.Write(score)
    #machine.reset()

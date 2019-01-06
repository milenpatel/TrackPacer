import time
import threading
import RPi.GPIO as GPIO
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
from neopixel import *

LED_PIN = 18
LED_FREQ_HZ= 800000
LED_DMA = 10
LED_INVERT = False
LED_CHANNEL = 0
LIT_PART = 4 #Change this to be how long you want the led to be lit for
LED_COUNT = 76 #Change this to be how many LED's end up being on the track 
LED_BRIGHTNESS = 200 #Change this to be how bright you want the LED's to be [0,255]

def beginPacing(numMinutesPerLap, numSecondsPerLap, getOutMode, numLaps, preferredColor):
    totalSecondsPerLap = 60*numMinutesPerLap + numSecondsPerLap #Used for calculating position change of LED's between each loop
    totalSeconds = totalSecondsPerLap * numLaps #Used to control how long the for loop runs for
    pixelList = list(range(0,LIT_PART)) #List that contains the individual positions of each LED in the LIT range
    lastValuePixelList = [-1]     #make a list that is equal to pixelList in length, but has -1 for each value
    for R in pixelList:
        lastValuePixelList.append(-1)
    lastValuePixelList.pop()
    for i in range(totalSeconds): #Make a for loop that runs one time each second
        for x in lastValuePixelList:#Turn off the LED's from last Loop
            if(x != -1):
                strip.setPixelColor(x,0)
        for x in pixelList:  #Light up the correct part of the strip
            strip.setPixelColor(x, preferredColor)
        strip.show()
        for x in range(len(lastValuePixelList)): #Update the list of pixels that needs to be cleared on the next iteration
            lastValuePixelList[x]=pixelList[x]
        for x in range(len(pixelList)):  #Update the values of pixelList for the next loop
            pixelList[x]+=LED_COUNT/totalSecondsPerLap
            if pixelList[x]>LED_COUNT-1:
                pixelList[x]-=LED_COUNT
        if getOutMode and i<10: #Currently, get out mode just makes the first 10 iterations go at double speed, this means that it finishes faster than pace, see if this is noticeable on track
            time.sleep(0.5)
        else:
            time.sleep(1) #If there is a big delay upon implementation, then update this to be 1-runTime to improve accuracy
        print("Loop " + str(i) + " / " + str(totalSeconds-1)+" has ended: ")
        print("Pixel Values: " + str(pixelList))
        print("-----------")
    for x in range(len(lastValuePixelList)):    #After the entire loop, clear the stuff from the last iteration
        strip.setPixelColor(lastValuePixelList[x], 0)
    strip.show()

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

x= threading.Thread(target = beginPacing, name = 'thread1', args = (0,19,False,2,Color(255,0,0)))
y= threading.Thread(target = beginPacing, name = 'thread2', args = (0,14,False,2,Color(0,255,0)))
x.start()
y.start()
#Try if getOutMode and i>10 time.sleep(1+10/totalSeconds)
#Try get rid of popline and just do pixellist-1 so it iterates one less time

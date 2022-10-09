import cv2
import math
import time

from matplotlib import image

def estimateSpeed(location1, location2):
    PTime=0
    d_pixels = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
    ppm = 8.8
    d_meters = d_pixels / ppm
    while True:
        CTime=time.time()
        fps=1/(CTime-PTime)
        PTime=CTime
    speed = d_meters * fps * 3.6
    return speed

def process_in_while(img,carId,car_bbox):
    frameCounter=0
    CurrentCarId=0
    fps=0

    carTracker={}
    carNumber={}
    carLoc1={}
    carLoc2={}

    speed=[None]*1000

    while True:
        start_time=time.time()
        
        if type(img)==type(None):
            break

        frameCounter+=1
        carIdToDel=[]

        for carID in carTracker.keys():
            trackingQuality = carTracker[carID].update(img)

            if trackingQuality < 7:
                carIdToDel.append(carID)

        
        for carID in carIdToDel:
            print("Removing carID " + str(carID) + ' from list of trackers. ')
            print("Removing carID " + str(carID) + ' previous location. ')
            print("Removing carID " + str(carID) + ' current location. ')
            carTracker.pop(carID, None)
            carLoc1.pop(carID, None)
            carLoc2.pop(carID, None)

        
        if not (frameCounter % 10):
            for (_x, _y, _w, _h) in car_bbox:
                x = int(_x)
                y = int(_y)
                w = int(_w)
                h = int(_h)
            x_bar = x + 0.5 * w
            y_bar = y + 0.5 * h

            matchCarID = None

            for carID in carTracker.keys():
                trackedPosition = carTracker[carID].get_position()



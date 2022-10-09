from FunctionLibrary import *
import cv2
import time

tracker=EuclideanDistTracker()
PTime=0
obj_det=cv2.createBackgroundSubtractorMOG2(history=100,varThreshold=40)

WebcamIsUsing=False
if WebcamIsUsing: 
    cap=cv2.VideoCapture(0)
else:
    cap=cv2.VideoCapture("highway.mp4")

while True:
    _,img=cap.read()

    h,w,_,=img.shape
    roi=img[340: 720,500: 800]
    mask=obj_det.apply(roi)
    _,mask=cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
    cont,_=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    det=[]
    for cnt in cont:
        area=cv2.contourArea(cnt)
        if area>100:
            #cv2.drawContours(roi,[cnt],-1,(0,255,0),2)
            x,y,w,h=cv2.boundingRect(cnt)
            det.append([x,y,w,h])
    
    CTime=time.time()
    fps=1/(CTime-PTime)
    PTime=CTime
    
    boxes_ids=tracker.update(det)
    for box in boxes_ids:
        x,y,w,h,id=box
        SpeedEstimatorTool=SpeedEstimator([x,y],fps)
        speed=SpeedEstimatorTool.estimateSpeed()
        cv2.putText(roi,str(id)+": "+str(speed)+"Km/h",(x,y-15),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
        cv2.rectangle(roi,(x,y),(x+w,y+h),(0,0,255),3)

    cv2.imshow("mask",mask)
    cv2.imshow("roi",roi)
    cv2.imshow("img",img)

    key=cv2.waitKey(30)
    if key==113: #113=Q
        break

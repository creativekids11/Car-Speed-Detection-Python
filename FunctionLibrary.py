import math
import numpy as np

class EuclideanDistTracker:
    def __init__(self):
        self.center_points={}
        self.id_count=0
    def update(self,obj_rect):
        obj_bbx_ids=[]
        for rect in obj_rect:
            x,y,w,h=rect
            cx=(x+x+w)//2
            cy=(y+y+h)//2
            same_obj=False
            for id,pt in self.center_points.items():
                dist=math.hypot(cx-pt[0],cy-pt[1])
                if dist<25:
                    self.center_points[id]=(cx,cy)
                    obj_bbx_ids.append([x,y,w,h,id])
                    same_obj=True
                    break
            if same_obj is False:
                self.center_points[self.id_count]=(cx,cy)
                obj_bbx_ids.append([x,y,w,h,self.id_count])
                self.id_count+=1
        new_cnt_point={}
        for bb_id in obj_bbx_ids:
            _,_,_,_,obj_id=bb_id
            center=self.center_points[obj_id]
            new_cnt_point[obj_id]=center
        self.center_points=new_cnt_point.copy()

        return obj_bbx_ids

class SpeedEstimator:
    def __init__(self,posList,fps):
        self.x=posList[0]
        self.y=posList[1]
        self.fps=fps
        
    def estimateSpeed(self):
        # Distance / Time -> Speed
        d_pixels=math.sqrt(self.x+self.y)
        ppm=8.8
        d_meters=int(d_pixels*ppm)
        speed=d_meters/self.fps*3.6
        speedInKM=np.average(speed)
        return int(speedInKM)
    
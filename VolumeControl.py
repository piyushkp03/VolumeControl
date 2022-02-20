import math

import cv2
import time
import numpy
import numpy as np

import HandsTracking as ht


from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume



videocap=cv2.VideoCapture(0)

prevtime=0

detector=ht.HandDetection()


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volrange=volume.GetVolumeRange()  #-65 to 0

minvol=volrange[0]
maxvol=volrange[1]


while True:
    test, imgframe=videocap.read()
    img=imgframe
    #img=detector.Hands(imgframe)
    lmlist=detector.Location(img,draw=False)
    if len(lmlist)>0:
        #print(lmlist[4],lmlist[8])
        x1,y1=lmlist[4][0],lmlist[4][1]
        x2, y2 = lmlist[8][0], lmlist[8][1]
        cv2.rectangle(img,(x1-5,y1-5),(x1+5,y1+5),cv2.COLOR_YUV420sp2GRAY,10)
        cv2.rectangle(img, (x2 - 5, y2 - 5), (x2 + 5, y2 + 5), cv2.COLOR_YUV420sp2GRAY, 10)
        cv2.line(img,(x1,y1),(x2,y2),(202,122,0),3)
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img, (cx, cy), 10, (33, 112, 234), cv2.FILLED)

        l=math.hypot(x1-x2,y1-y2)
        #print(l)

        # Length range 40-290
        vol=np.interp(l,[30,270],[minvol,maxvol])
        volume.SetMasterVolumeLevel(vol, None)
        print(vol)

        if l<50:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)






    img=cv2.resize(img,(800,500))
    cv2.imshow("Img", img)
    cv2.waitKey(1)


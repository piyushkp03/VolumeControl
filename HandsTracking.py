import cv2
import mediapipe as mdp
import time


class HandDetection:
    def __init__(self,mode=False,mxhands=3
                 ,detcon=0.5,trcon=0.5):
        self.mode = mode
        self.mxhands = mxhands
        self.detcon = detcon
        self.trcon=trcon
        self.mdpHands = mdp.solutions.hands
        self.hands = self.mdpHands.Hands(self.mode,self.mxhands,1,self.detcon,self.trcon)
        self.mdpDraw = mdp.solutions.drawing_utils

    def Location(self,img,handno=0,draw=False):

        lmlist=[]

        self.results = self.hands.process(img)
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handno]
            for idd, lm in enumerate(myHand.landmark):
                print(lm)
                h, w, c = img.shape
                # print("Image dimension",h,w,c)
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(type(idd), idd, cx, cy)
                lmlist.append((cx,cy))
                #if idd == 0:
                if draw:
                    #print("Inside if", idd)
                    cv2.circle(img, (cx, cy), 20, (255, 0, 255), cv2.FILLED)

        return lmlist

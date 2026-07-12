import cv2
# pyrefly: ignore [missing-import]
import mediapipe as mp 
import os , time 
from Hand_Tracking_Model.utils import handDetector

from utils import EffectManager , get_fps, detect_thumbs_up , detect_thumbs_down
from utils import detect_heart ,  detect_rock_on , detect_peace , detect_middle

##################
""" Arguments """
##################
Wcam, Hcam = 1280 , 720 

cap = cv2.VideoCapture(0)
cap.set(3,Wcam)
cap.set(4,Hcam)

detector = handDetector(model_path = "Hand_Tracking_Model/hand_landmarker.task",
                        num_hands = 2,
                        confidence = 0.6
                        )

effect_mgr = EffectManager()

frame_count = 0
pTime = time.time()

Alert = "Hand is not completly DETECTED ! Try to move it !"

while True:

    # Reading
    test , img = cap.read()
    if not test or img is None:
        break

    # fps and time
    fps , pTime = get_fps(cap, pTime)

    timestamp_ms = int((frame_count / get_fps(cap,0,type='cap')[0]) * 1000)
    frame_count += 1

    # flipping the image Y-AXIS : 
    img = cv2.flip(img,1)

    # preprocessing
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)

    res = detector.landmarker.detect_for_video(mp_img,timestamp_ms) 

    lmList = detector.findHands(img,res, draw =True )
    
    if lmList and len(lmList) > 0:
        
        # Center of screen for 2-handed effects
        cx, cy = int(img.shape[1]/2) - 100, int(img.shape[0]/2)

        # 1. Heart (2 hands)
        if detect_heart(lmList):
            effect_mgr.trigger("[ ❤️ HEARTS ]", cx, cy)
            
        else:
            # 2. Rock On
            rocks = detect_rock_on(lmList)
            if rocks == 1 or rocks ==2:
                effect_mgr.trigger("[ 🪩 LASERS ]", cx, cy)
                
            # 3. Peace
            peaces = detect_peace(lmList)
            if peaces == 2:
                effect_mgr.trigger("[ 🎉 CONFETTI ]", cx, cy)
            elif peaces == 1:
                effect_mgr.trigger("[ 🎈 BALLOONS ]", cx, cy)
                
            # 4. Thumbs Up
            thumbs_ups = detect_thumbs_up(lmList)
            if thumbs_ups == 2:
                effect_mgr.trigger("[ 🎆 FIREWORKS ]", cx, cy)
            elif thumbs_ups == 1:
                effect_mgr.trigger("[ 👍 THUMBS UP ]", cx, cy)
                
            # 5. Thumbs Down
            thumbs_downs = detect_thumbs_down(lmList)
            if thumbs_downs == 2:
                effect_mgr.trigger("[ 🌧️ RAINSTORM ]", cx, cy)
            elif thumbs_downs == 1:
                effect_mgr.trigger("[ 👎 THUMBS DOWN ]", cx, cy)
            
            # 6. middle finger
            middle_finger = detect_middle(lmList)
            if middle_finger in [1,2]:
                effect_mgr.trigger("[ 🖕 MIDDLE FINGER ]", cx, cy)

        # Draw active effects
        effect_mgr.draw(img)

    else :
        cv2.putText(img,Alert, (40,120), cv2.FONT_HERSHEY_COMPLEX,
                    1, (183,81,93) , 1
                    )
        print(Alert)
    

    # display 
    cv2.putText(img,f'FPS : {str(int(fps))}',(40,80), cv2.FONT_HERSHEY_COMPLEX,
                3, (183,81,93) , 1
                )
    cv2.imshow('Live',cv2.cvtColor(img,cv2.COLOR_RGB2BGR))

    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

cap.release()
cv2.destroyAllWindows()
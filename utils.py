import time , math
import cv2
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
from PIL import Image, ImageDraw, ImageFont


# init " pTime = time.time() " before the While loop
def get_fps(cap, pTime,type='default'):
    if type == "default":
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        return fps, pTime

    elif type =="cap":
        fps= cap.get(cv2.CAP_PROP_FPS)
        if fps<= 0:
            return 30, pTime
        return fps, pTime
    else:
        return 30, pTime


try:
    EMOJI_FONT = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 40)
except IOError:
    EMOJI_FONT = ImageFont.load_default()

class EffectManager:
    def __init__(self):
        self.active_effects = []

    def trigger(self, text, x, y):
        for eff in self.active_effects:
            if eff['text'] == text and eff['life'] > 15:
                return
        
        self.active_effects.append({
            'text': text,
            'x': x,
            'y': y,
            'life': 30  
        })

    def draw(self, img):
        if not self.active_effects:
            return img

        # 1. Convert the current OpenCV image matrix (RGB) to a PIL Image (RGB)
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)

        for eff in self.active_effects[:]:
            # 2. Draw the emoji strings directly onto the PIL canvas layout
            # PIL text uses (X, Y) layout configurations seamlessly
            draw.text((eff['x'], eff['y']), eff['text'], font=EMOJI_FONT, embedded_color=True)
            
            # Animate positions
            eff['y'] -= 4
            eff['life'] -= 1
            
            if eff['life'] <= 0:
                self.active_effects.remove(eff)
        
        # 3. Convert the PIL canvas tracking map back into your active OpenCV image reference
        img_rgb = np.array(img_pil)
        np.copyto(img, img_rgb)
        

# ==========================================
# 2. CORE FINGER STATE LOGIC
# ==========================================
def get_fingers_up(hand):
    """Returns a list of 5 booleans: [Thumb, Index, Middle, Ring, Pinky]"""
    fingers = []
    
    # Thumb
    thumb_tip_dist = math.hypot(hand[4][1] - hand[17][1], hand[4][2] - hand[17][2])
    thumb_ip_dist = math.hypot(hand[3][1] - hand[17][1], hand[3][2] - hand[17][2])
    fingers.append(thumb_tip_dist > thumb_ip_dist)

    # 4 Fingers
    for i in range(8, 21, 4):
        tip_dist = math.hypot(hand[i][1] - hand[0][1], hand[i][2] - hand[0][2])
        pip_dist = math.hypot(hand[i-2][1] - hand[0][1], hand[i-2][2] - hand[0][2])
        fingers.append(tip_dist > pip_dist)
        
    return fingers

def is_pointing_up(hand):
    return hand[4][2] < hand[2][2]  # Thumb tip is higher than Thumb base

def is_pointing_down(hand):
    return hand[4][2] > hand[2][2]  # Thumb tip is lower than Thumb base

# ==========================================
# 3. GESTURE DETECTION FUNCTIONS
# ==========================================
def detect_thumbs_up(hands):
    count = sum(1 for hand in hands if get_fingers_up(hand) == [True, False, False, False, False] and is_pointing_up(hand))
    return count

def detect_thumbs_down(hands):
    count = sum(1 for hand in hands if get_fingers_up(hand) == [True, False, False, False, False] and is_pointing_down(hand))
    return count

def detect_peace(hands):
    # Index and Middle up, others down. Thumb can optionally be out.
    count = 0
    for hand in hands:
        f = get_fingers_up(hand)
        if f[1] and f[2] and not f[3] and not f[4]:
            count += 1
    return count

def detect_rock_on(hands):
    # Index and Pinky up. Thumb can optionally be out.
    count = 0
    for hand in hands:
        f = get_fingers_up(hand)
        if f[1] and not f[2] and not f[3] and f[4]:
            count += 1
    return count

def detect_heart(hands):
    if len(hands) != 2:
        return False
    
    h1, h2 = hands[0], hands[1]
    
    # Check if index tips (8) are close together
    index_dist = math.hypot(h1[8][1] - h2[8][1], h1[8][2] - h2[8][2])
    # Check if thumb tips (4) are close together
    thumb_dist = math.hypot(h1[4][1] - h2[4][1], h1[4][2] - h2[4][2])
    
    # Check if all other fingers are folded (roughly)
    f1, f2 = get_fingers_up(h1), get_fingers_up(h2)
    
    if index_dist < 60 and thumb_dist < 60 and not f1[2] and not f2[2]:
        count = 0
        for hand in hands :

            index_tip_thumb_dist = math.hypot(hand[8][1]-hand[4][1], hand[8][2]-hand[4][2])
            index_pip_thumb_dist = math.hypot(hand[4][1]-hand[6][1], hand[4][2]-hand[6][2])

            if index_tip_thumb_dist < index_pip_thumb_dist :
                count += 1

        if count == 2 :
            return True
    return False
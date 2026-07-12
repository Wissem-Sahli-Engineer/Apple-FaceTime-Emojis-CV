# 🚀 Apple FaceTime Emojis CV

A playful computer-vision project that brings the energy of Apple FaceTime reactions to your webcam. Using OpenCV and MediaPipe, the app detects hand gestures in real time and overlays animated emoji effects such as hearts, confetti, fireworks, lasers, and rainstorms directly on the live video feed.

---

## ✨ Project Overview

This project combines real-time hand tracking with gesture recognition to create an interactive, camera-driven experience. It is designed for fun experimentation, live demos, and creative visual effects driven by simple hand poses.

### What it does
- Captures video from your webcam
- Detects hand landmarks with MediaPipe
- Classifies common gestures such as heart, peace, rock-on, thumbs up, and thumbs down
- Renders animated emoji-based effects in the video window
- Lets you exit the app by pressing the space bar

---

## 🏗️ Architecture & Flow Scheme

```mermaid
flowchart LR
    A[Start Webcam] --> B[Read Frame]
    B --> C[Flip & Convert to RGB]
    C --> D[Send Frame to MediaPipe HandLandmarker]
    D --> E[Extract Hand Landmarks]
    E --> F[Classify Gesture]
    F --> G[Trigger Effect]
    G --> H[Draw Emoji Overlay]
    H --> I[Display Live Stream]
    I --> B
```

### Pipeline Summary
1. The webcam captures each frame.
2. The frame is flipped horizontally and converted to RGB for MediaPipe.
3. Hand landmarks are extracted for one or two hands.
4. Gesture logic checks finger positions and distances.
5. Matching effects are triggered and drawn as animated overlays.
6. The updated frame is shown in a live OpenCV window.

---

## 📂 Directory Structure

```text
Apple FaceTime Emojis CV/
├── Emojis.py
├── readme.md
├── requirements.txt
├── utils.py
└── Hand_Tracking_Model/
    ├── hand_landmarker.task
    └── utils.py
```

---

## 📄 File Details

- [Emojis.py](file:///Users/wess/Desktop%20computer%20vision/Apple%20FaceTime%20Emojis%20CV/Emojis.py)  
  The main application entry point. It opens the webcam, runs the detection loop, handles the live frame display, and calls the gesture/effect logic.

- [utils.py](file:///Users/wess/Desktop%20computer%20vision/Apple%20FaceTime%20Emojis%20CV/utils.py)  
  Contains the effect engine and gesture recognition helpers. It manages active overlays, animation timing, and the coordinate-based logic for identifying hand poses.

- [Hand_Tracking_Model/utils.py](file:///Users/wess/Desktop%20computer%20vision/Apple%20FaceTime%20Emojis%20CV/Hand_Tracking_Model/utils.py)  
  Wraps the MediaPipe hand landmark detector and converts raw landmark results into usable hand coordinate lists.

- [Hand_Tracking_Model/hand_landmarker.task](file:///Users/wess/Desktop%20computer%20vision/Apple%20FaceTime%20Emojis%20CV/Hand_Tracking_Model/hand_landmarker.task)  
  The trained MediaPipe hand landmark model used to detect hand joints and finger positions from webcam frames.

- [requirements.txt](file:///Users/wess/Desktop%20computer%20vision/Apple%20FaceTime%20Emojis%20CV/requirements.txt)  
  Lists the required Python packages for running the project.

- [readme.md](file:///Users/wess/Desktop%20computer%20vision/Apple%20FaceTime%20Emojis%20CV/readme.md)  
  Project documentation and usage guide.

---

## 🧮 How It Works (Core Logic)

The app uses a lightweight gesture pipeline built around hand landmark geometry:

### 1. Frame acquisition
Each video frame is read from the webcam and normalized for processing.

### 2. Landmark extraction
The MediaPipe hand detector produces 21 hand landmarks per detected hand. These points include finger tips, knuckles, and palm base positions.

### 3. Gesture detection
The project classifies gestures using simple geometric checks:

- Thumbs up / thumbs down  
  The thumb tip is compared against the thumb base and the hand orientation is checked to distinguish up vs. down.

- Peace sign  
  The index and middle fingers must be raised while the ring and pinky remain folded.

- Rock-on  
  The index and pinky must be raised while the middle and ring remain folded.

- Heart gesture  
  Two hands are required. The index finger tips and thumb tips must be positioned close together, and the remaining fingers should be folded into a heart-like shape.

### 4. Effect rendering
Once a gesture is recognized, the app stores a temporary effect entry with:
- a label such as "HEARTS" or "FIREWORKS"
- a screen position near the center of the frame
- a short lifespan and upward movement animation

The effect is drawn on top of the live image using emoji text and a short-lived animation loop.

---

## 🛠️ Setup & Requirements

### Requirements
- Python 3.9 or newer
- A working webcam
- macOS camera permission enabled
- Internet access for the initial package install if needed

### Required packages
Install the following dependencies:
- opencv-python
- mediapipe
- numpy
- pillow

### Setup instructions

1. Open a terminal in the project folder.

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python Emojis.py
```

### Notes
- The project uses the Apple Color Emoji font on macOS for emoji rendering, which improves the visual quality of effect overlays.
- If the camera does not open, verify that your webcam is available and that your system allows camera access.

---

## 🎮 Controls / Usage

### Running the app
- Launch the program with the command above.
- A live window titled "Live" will open.
- Your webcam feed will appear with the detected hands and animated effects.

### Interaction
- Show one or two hands in front of the camera.
- Try the following gestures to trigger effects:
  - ❤️ Heart gesture: triggers hearts
  - 🤘 Rock-on: triggers lasers
  - ✌️ Peace sign: triggers confetti or balloons
  - 👍 Thumbs up: triggers fireworks or thumbs-up text
  - 👎 Thumbs down: triggers a rainstorm or thumbs-down text

### Exit
- Press the space bar to close the application.

---

## 💡 Quick Summary

This project is a compact, real-time hand-gesture visualizer that turns ordinary webcam input into a lively emoji reaction system. It is simple to run, easy to extend, and a great example of combining computer vision, gesture recognition, and live visual effects.

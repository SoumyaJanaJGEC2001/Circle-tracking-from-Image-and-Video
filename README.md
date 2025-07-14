
# 🟢 Circle Detection & Tracking in Industrial Grayscale Videos

This project performs **robust circle detection and tracking** in black-and-white (B&W) industrial video streams using a **hybrid method** combining:

- 🌀 **Hough Circle Transform** – detects circular shapes
- 🔑 **ORB Descriptors** – ensures frame-to-frame matching
- 🧠 **Object Tracking** – tracks unique circle IDs
- 📊 **CSV Logging** – exports per-frame circle counts

Also includes **static image circle detection with diameter extraction** (`main.py`).

---

## 📽️ Demo Output

![Tracked Output Animation](tracked_output.gif)

---

## 📂 Project Structure

```
.
├── test_video.mp4                 # Input video (grayscale)
├── pic1.jpg                       # Input image for static detection
├── tracker.py                     # Real-time video circle tracking
├── main.py                        # Static image detection + logging
├── refined_tracked_output.mp4     # Tracked video output
├── circle_data.csv                # Output for static image (main.py)
├── circle_count_per_frame.csv     # Per-frame circle count (tracker.py)
└── README.md
```

---

## ✅ Features

### `tracker.py` – Real-Time Video Circle Tracking
- Assigns **unique IDs** to persistent circles across frames
- Uses **ORB descriptors + spatial proximity** for robustness
- Ignores **noisy or short-lived detections**
- Saves:
  - 🟢 `refined_tracked_output.mp4` – Annotated video
  - 📊 `circle_count_per_frame.csv` – Circle count per frame

### `main.py` – Static Image Detection
- Detects all circles in an input image
- Logs **center, radius, diameter**
- Saves:
  - 🟢 Annotated window
  - 📊 `circle_data.csv` – Circle metadata table

---

## 🧠 How It Works

1. 🔍 **Hough Transform** detects circular shapes.
2. 🔑 **ORB Descriptors** are extracted from circle regions.
3. 🧬 **BFMatcher** finds frame-to-frame descriptor similarity.
4. 🧠 Tracks are updated only if:
   - Spatial distance < `SPATIAL_THRESH`
   - Descriptor distance < `DESCRIPTOR_THRESH`
5. ⏳ Tracks seen for ≥ `MIN_PERSISTENCE` frames are retained.

---

## 🛠️ Setup

### Requirements
- Python 3.7+
- OpenCV
- NumPy
- Pandas

### Install
```bash
pip install opencv-python numpy pandas
```

---

## 🚀 Usage

### ▶ Real-Time Video Tracking
```bash
python tracker.py
```
- 🔸 Input: `test_video.mp4`
- 🔸 Output:
  - `refined_tracked_output.mp4` – Video with circle IDs
  - `circle_count_per_frame.csv` – Circle count per frame

### 🖼 Static Image Circle Detection
```bash
python main.py
```
- 🔸 Input: `pic1.jpg`
- 🔸 Output:
  - Annotated circle display
  - `circle_data.csv`

---

## 🏭 Real-World Industrial Applications

✅ **Automated Quality Control**  
🔹 Detect flaws in gaskets, O-rings, bearings

✅ **Production Line Monitoring**  
🔹 Track circular items on conveyor belts

✅ **Microscopic Inspection**  
🔹 Identify circular cells, bubbles, or beads

✅ **Packaging & Label Validation**  
🔹 Check cap alignment, bottle tops, printed logos

✅ **Tool Marking & Alignment Check**  
🔹 Detect hole positions, tool paths, surface markings

---

## ⚙️ Configuration Parameters

You can tune these constants in `tracker.py`:

```python
SPATIAL_THRESH = 23
DESCRIPTOR_THRESH = 35
MIN_PERSISTENCE = 16
MAX_IDLE = 4
POSITION_AVG_WINDOW = 5
UPDATE_DESCRIPTOR_THRESHOLD = 18
MIN_MATCH_COUNT = 6
MIN_RADIUS = 10
```

---

## ⚠️ License

This project is under a **non-commercial use only license**.  
**Commercial, industrial, or revenue-generating use is strictly prohibited.**

For academic or personal use only.  
See `LICENSE` for full terms or contact the author for commercial licensing.

---

## 📧 Author

**Soumya Kanti Jana**  
Dept. of Computer Science & Engineering  
Jalpaiguri Government Engineering College  
Email: [soumyajana2001@gmail.com](mailto:soumyajana2001@gmail.com)

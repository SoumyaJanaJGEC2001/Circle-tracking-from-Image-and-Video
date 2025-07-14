🟢 Circle Detection & Tracking in Industrial Grayscale Videos
This project performs robust circle detection and tracking in industrial black-and-white (B&W) video streams using a hybrid approach combining:

🌀 Hough Circle Transform for shape-based detection

🔑 ORB Feature Descriptors for matching between frames

🧠 Object Tracking with spatial & appearance-based consistency

📊 Exports per-frame circle counts and visualization

It also supports static image detection with diameter extraction using main.py.

📽️ Demo Output

![Tracked Output Animation](tracked_output.gif)

📂 Project Structure
bash
Copy
Edit
.
├── test_video.mp4                 # (your input video)
├── pic1.jpg                       # (your input image for static detection)
├── tracker.py                     # real-time video tracking
├── main.py                        # static image detection & logging
├── refined_tracked_output.mp4     # annotated video output
├── circle_data.csv                # output for main.py (image)
├── circle_count_per_frame.csv     # output for tracker.py (video)
└── README.md
✅ Features
tracker.py – Real-Time Circle Tracking
Assigns unique IDs to persistent circles across frames

Filters noise using ORB descriptors + spatial constraints

Ignores short-lived or inconsistent detections

Tracks only real, stable circle objects

Saves annotated video + per-frame circle count CSV

main.py – Static Image Detection
Detects all circles from an input image

Calculates and logs radius and diameter

Saves annotated image and outputs data to CSV

🧠 How It Works
🔍 Hough Circle Detection for finding circular shapes

🔑 ORB descriptors are extracted from each circle region

🧬 BFMatcher checks descriptor similarity between frames

🧠 Tracks are updated only if spatial distance and descriptor distance are within threshold

⏳ Only circles seen for ≥ MIN_PERSISTENCE frames are counted

🛠️ Setup
Requirements:
Python 3.7+

OpenCV

NumPy

Pandas

Install them:

bash
Copy
Edit
pip install opencv-python numpy pandas
🚀 Usage
▶ Video Circle Tracker (tracker.py)
bash
Copy
Edit
python tracker.py
Outputs:

refined_tracked_output.mp4: Video with tracked circle IDs

circle_count_per_frame.csv: Count of unique circles per frame

🖼 Static Image Circle Detector (main.py)
bash
Copy
Edit
python main.py
Ensure the image path (pic1.jpg) is valid.

Outputs:

Annotated display window with detected circles

circle_data.csv: Per-circle data including radius and diameter

🏭 Real-World Industrial Applications
✅ Automated Quality Control
Detect defects in circular components (e.g., bearings, gaskets, pipe ends)

✅ Production Line Monitoring
Count and inspect round items moving through conveyor belts

✅ Microscopic Inspection
Detect bubbles, cell boundaries, or circular particles under microscopes

✅ Packaging & Labeling Validation
Ensure printed or physical circles (bottle caps, can labels) are present and aligned

✅ Mechanical Process Verification
Detect tool marks or hole placements on metallic surfaces

⚙️ Configuration Parameters
Inside tracker.py, you can tune:

python
Copy
Edit
SPATIAL_THRESH = 23           # max distance for spatial matching
DESCRIPTOR_THRESH = 35        # feature similarity tolerance
MIN_PERSISTENCE = 16          # minimum frames a circle must persist
MAX_IDLE = 4                  # drop circle after N missed frames
MIN_RADIUS = 10               # remove very small noisy detections
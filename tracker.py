import cv2
import numpy as np
import pandas as pd
from collections import defaultdict, deque

# === Configuration ===
VIDEO_PATH = "test_video.mp4"
OUTPUT_VIDEO = "refined_tracked_output.mp4"
OUTPUT_CSV = "circle_count_per_frame.csv"

SPATIAL_THRESH = 23            # Slightly tighter spatial threshold
DESCRIPTOR_THRESH = 35         # Stricter matching threshold
MIN_PERSISTENCE = 16           # Circle must persist ≥ 16 frames
MAX_IDLE = 4                   # Forget if unseen for 4 frames
POSITION_AVG_WINDOW = 5        # Averaging for stability
UPDATE_DESCRIPTOR_THRESHOLD = 18  # Only update descriptor if match is strong
MIN_MATCH_COUNT = 6            # Require minimum number of matches to consider valid
MIN_RADIUS = 10                # Filter very small noisy detections

# === Setup ===
cap = cv2.VideoCapture(VIDEO_PATH)
fps = cap.get(cv2.CAP_PROP_FPS)
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, fps, (W, H))

orb = cv2.ORB_create(nfeatures=1000)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# === Tracking state ===
tracked_circles = {}
appearance_count = defaultdict(int)
framewise_counts = []
circle_id_counter = 1
frame_idx = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_idx += 1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                               param1=50, param2=30,
                               minRadius=MIN_RADIUS, maxRadius=100)

    matched_ids_this_frame = set()

    if circles is not None:
        circles = np.round(circles[0, :]).astype(int)

        for (x, y, r) in circles:
            x1, x2 = max(x - r, 0), min(x + r, W)
            y1, y2 = max(y - r, 0), min(y + r, H)
            crop = gray[y1:y2, x1:x2]
            kp, des = orb.detectAndCompute(crop, None)
            if des is None:
                continue

            matched_id = None
            min_avg_dist = float('inf')

            for cid, data in tracked_circles.items():
                avg_pos = np.mean(data['positions'], axis=0)
                dx, dy = x - avg_pos[0], y - avg_pos[1]
                spatial_dist = np.hypot(dx, dy)
                if spatial_dist > SPATIAL_THRESH:
                    continue

                if data['desc'] is None:
                    continue

                matches = bf.match(des, data['desc'])
                if len(matches) < MIN_MATCH_COUNT:
                    continue

                avg_desc_dist = np.mean([m.distance for m in matches])
                if avg_desc_dist < DESCRIPTOR_THRESH and avg_desc_dist < min_avg_dist:
                    matched_id = cid
                    min_avg_dist = avg_desc_dist

            if matched_id:
                tracked = tracked_circles[matched_id]
                tracked['positions'].append((x, y))
                if len(tracked['positions']) > POSITION_AVG_WINDOW:
                    tracked['positions'].popleft()
                if min_avg_dist < UPDATE_DESCRIPTOR_THRESHOLD:
                    tracked['desc'] = des
                tracked['last_seen'] = frame_idx
                appearance_count[matched_id] += 1
                matched_ids_this_frame.add(matched_id)
            else:
                tracked_circles[circle_id_counter] = {
                    'positions': deque([(x, y)], maxlen=POSITION_AVG_WINDOW),
                    'desc': des,
                    'last_seen': frame_idx
                }
                appearance_count[circle_id_counter] += 1
                matched_ids_this_frame.add(circle_id_counter)
                matched_id = circle_id_counter
                circle_id_counter += 1

            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            cv2.putText(frame, f"ID {matched_id}", (x - 10, y - r - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    # Forget inactive
    for cid in list(tracked_circles):
        if frame_idx - tracked_circles[cid]['last_seen'] > MAX_IDLE:
            del tracked_circles[cid]

    # Log circle count
    framewise_counts.append({
        'Frame': frame_idx,
        'UniqueCircles': len(matched_ids_this_frame)
    })

    cv2.putText(frame, f"Frame: {frame_idx} | Circles: {len(matched_ids_this_frame)}",
                (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    out.write(frame)
    cv2.imshow("Refined Tracker", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

# Filter persistent
valid_ids = [cid for cid, count in appearance_count.items() if count >= MIN_PERSISTENCE]

# Save CSV
df = pd.DataFrame(framewise_counts)
df.to_csv(OUTPUT_CSV, index=False)

print(f" Refined Tracking Complete")
print(f" Total Persistent Circles: {len(valid_ids)}")
print(f" CSV saved: {OUTPUT_CSV}")
print(f" Video saved: {OUTPUT_VIDEO}")

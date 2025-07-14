import cv2
import numpy as np
import pandas as pd

# Load the image
image_path = 'pic1.jpg'
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (9, 9), 2)

# Detect circles
circles = cv2.HoughCircles(
    blurred,
    cv2.HOUGH_GRADIENT,
    dp=1.2,
    minDist=20,
    param1=50,
    param2=30,
    minRadius=10,
    maxRadius=100
)

# List to store circle data
circle_data = []

if circles is not None:
    circles = np.uint16(np.around(circles))
    total_detected = len(circles[0])
    
    for idx, (x, y, r) in enumerate(circles[0, :], 1):
        diameter = 2 * r
        circle_data.append({
            'Circle_No': idx,
            'Center_X': x,
            'Center_Y': y,
            'Radius': r,
            'Diameter': diameter
        })
        # Draw the circle
        cv2.circle(image, (x, y), r, (0, 255, 0), 2)
        cv2.circle(image, (x, y), 2, (0, 0, 255), 3)

    # Save to CSV
    df = pd.DataFrame(circle_data)
    
    # Add total count as a separate row at the end
    total_row = pd.DataFrame([{
        'Circle_No': 'Total',
        'Center_X': '',
        'Center_Y': '',
        'Radius': '',
        'Diameter': '',
        'Total_Detected': total_detected
    }])
    
    df = pd.concat([df, total_row], ignore_index=True)
    df.to_csv('circle_data.csv', index=False)

    print(f"{total_detected} circle(s) detected. Data saved to circle_data.csv.")

    # Show result
    cv2.imshow('Detected Circles', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print(" No circles were detected.")

import cv2
import numpy as np
from ultralytics import YOLO  # Assuming you have YOLOv8 or YOLOv11 Python bindings or implementation

# Initialize YOLOv8/YOLOv11 model
yolo = YOLO("yolov8m.pt")

# Parameters for motion tracking
motion_threshold_slow = 2  # Threshold for slow movement in pixels
motion_threshold_medium = 15  # Threshold for medium-speed movement in pixels
motion_tracking = {}
next_object_id = 1

# Initialize webcam
cap = cv2.VideoCapture(1) #change here for different cam

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set full screen for display
#cv2.namedWindow("YOLO Object Tracking", cv2.WINDOW_NORMAL)
#cv2.setWindowProperty("YOLO Object Tracking", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


# Define colors
color_still = (0, 0, 255)  # Red for still objects
color_medium = (0, 165, 255)  # Orange for medium-speed movement
color_fast = (0, 255, 0)  # Green for fast movement

# Helper function to calculate movement distance
def calculate_distance(prev_center, curr_center):
    dx = curr_center[0] - prev_center[0]
    dy = curr_center[1] - prev_center[1]
    return np.sqrt(dx ** 2 + dy ** 2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO detection
    results = yolo.predict(frame)

    current_detections = {}

    for result in results:
        for detection in result.boxes:
            x1, y1, x2, y2 = map(int, detection.xyxy[0])
            conf = detection.conf[0]
            cls = detection.cls[0]
            center = ((x1 + x2) // 2, (y1 + y2) // 2)

            if cls == 0:  # class 0 is 'person'
                matched = False
                for object_id, (prev_center, _, _) in motion_tracking.items():
                    distance = calculate_distance(prev_center, center)
                    if distance < 50:  # Threshold to match the same person
                        current_detections[object_id] = (center, distance, (x1, y1, x2, y2))
                        matched = True
                        break

                if not matched:
                    current_detections[next_object_id] = (center, 0, (x1, y1, x2, y2))
                    next_object_id += 1

    # Update motion tracking info
    motion_tracking = current_detections

    for object_id, (center, distance, bbox) in motion_tracking.items():
        color = color_still
        if distance > motion_threshold_medium:
            color = color_fast
        elif distance > motion_threshold_slow:
            color = color_medium

        # Draw bounding box with appropriate color
        x1, y1, x2, y2 = bbox
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 4)

        # Draw text with colored background
        text = f"Human {object_id}"
        (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        cv2.rectangle(frame, (x1, y1 - text_height - 10), (x1 + text_width, y1), color, -1)
        cv2.putText(frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Display the output frame
    cv2.imshow("YOLO Object Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

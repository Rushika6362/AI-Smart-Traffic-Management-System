import cv2
import threading
import time
from ultralytics import YOLO


# ---------------------------------------------------
# SETTINGS
# ---------------------------------------------------

VIDEO_PATH = "traffic.mp4"
MODEL_PATH = "models/yolov8n.pt"

# COCO vehicle class IDs
VEHICLE_CLASSES = {
    2: "Car",
    3: "Motorcycle",
    5: "Bus",
    7: "Truck"
}


# ---------------------------------------------------
# LOAD YOLO MODEL
# ---------------------------------------------------

model = YOLO(MODEL_PATH)


# ---------------------------------------------------
# SHARED DATA
# ---------------------------------------------------

latest_frame = None

vehicle_count = 0
traffic_status = "WAITING"
green_time = 20

car_count = 0
motorcycle_count = 0
bus_count = 0
truck_count = 0

lock = threading.Lock()


# ---------------------------------------------------
# TRAFFIC CALCULATION
# ---------------------------------------------------

def calculate_traffic(count):

    if count < 10:
        return "LOW", 20

    elif count < 30:
        return "MEDIUM", 40

    else:
        return "HIGH", 60


# ---------------------------------------------------
# VIDEO PROCESSING
# ---------------------------------------------------

def process_video():

    global latest_frame
    global vehicle_count
    global traffic_status
    global green_time

    global car_count
    global motorcycle_count
    global bus_count
    global truck_count

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print("ERROR: Cannot open traffic.mp4")
        return

    print("Traffic video started...")

    while True:

        success, frame = cap.read()

        # Restart video when it reaches the end
        if not success:

            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

            continue

        # ------------------------------------------------
        # YOLO DETECTION
        # ------------------------------------------------

        results = model(
            frame,
            classes=list(VEHICLE_CLASSES.keys()),
            conf=0.30,
            verbose=False
        )

        # Reset counts
        current_count = 0

        current_cars = 0
        current_motorcycles = 0
        current_buses = 0
        current_trucks = 0

        # ------------------------------------------------
        # PROCESS DETECTIONS
        # ------------------------------------------------

        for result in results:

            boxes = result.boxes

            for box in boxes:

                class_id = int(box.cls[0])

                if class_id not in VEHICLE_CLASSES:
                    continue

                current_count += 1

                # Individual vehicle count
                if class_id == 2:
                    current_cars += 1

                elif class_id == 3:
                    current_motorcycles += 1

                elif class_id == 5:
                    current_buses += 1

                elif class_id == 7:
                    current_trucks += 1

        # ------------------------------------------------
        # TRAFFIC STATUS
        # ------------------------------------------------

        current_status, current_green = calculate_traffic(
            current_count
        )

        # ------------------------------------------------
        # DRAW YOLO BOXES
        # ------------------------------------------------

        annotated_frame = results[0].plot()

        # ------------------------------------------------
        # DRAW INFORMATION ON VIDEO
        # ------------------------------------------------

        cv2.rectangle(
            annotated_frame,
            (10, 10),
            (380, 150),
            (0, 0, 0),
            -1
        )

        cv2.putText(
            annotated_frame,
            f"Vehicles: {current_count}",
            (25, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 255),
            2
        )

        cv2.putText(
            annotated_frame,
            f"Traffic: {current_status}",
            (25, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            annotated_frame,
            f"Green Signal: {current_green}s",
            (25, 115),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.putText(
            annotated_frame,
            "AI VEHICLE DETECTION",
            (25, 140),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 200, 0),
            1
        )

        # ------------------------------------------------
        # ENCODE FRAME FOR WEBSITE
        # ------------------------------------------------

        success, buffer = cv2.imencode(
            ".jpg",
            annotated_frame
        )

        if success:

            with lock:

                latest_frame = buffer.tobytes()

                vehicle_count = current_count

                traffic_status = current_status

                green_time = current_green

                car_count = current_cars

                motorcycle_count = current_motorcycles

                bus_count = current_buses

                truck_count = current_trucks

        # Small delay to prevent excessive CPU usage
        time.sleep(0.01)

    cap.release()


# ---------------------------------------------------
# START DETECTION THREAD
# ---------------------------------------------------

def start_detector():

    thread = threading.Thread(
        target=process_video,
        daemon=True
    )

    thread.start()


# ---------------------------------------------------
# GET CURRENT DATA
# ---------------------------------------------------

def get_traffic_data():

    with lock:

        return {
            "count": vehicle_count,
            "status": traffic_status,
            "green": green_time,

            "cars": car_count,
            "motorcycles": motorcycle_count,
            "buses": bus_count,
            "trucks": truck_count
        }


# ---------------------------------------------------
# VIDEO FRAME GENERATOR
# ---------------------------------------------------

def generate_frames():

    while True:

        with lock:

            frame = latest_frame

        if frame is not None:

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame
                + b"\r\n"
            )

        time.sleep(0.03)
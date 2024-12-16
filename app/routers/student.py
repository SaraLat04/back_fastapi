from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.db.database import get_db
from app.schemas.student import Student as StudentSchema, StudentCreate
from app.crud.student import get_students, get_student_by_id, create_student, update_student, delete_student
import os
import cv2
import numpy as np
from fastapi.responses import JSONResponse, HTMLResponse
from datetime import date
from app.models import Attendance, User, report, attendance_report, motivation_report, emotion
from app.models.student import Student
from app.models.classe import Classe
from app.models.Attendance import Attendance, AttendanceStatus
from deepface import DeepFace
from typing import List
import base64

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/", response_model=List[StudentSchema])
def read_students(db: Session = Depends(get_db)):
    return get_students(db)

@router.get("/scane-page")
def index():
    """Serve the HTML page for WebSocket connection."""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Attendance Scanning</title>
    </head>
    <body>
        <h1>Attendance Scanning</h1>
        <div id="camera-container">
            <video id="webcam" width="640" height="480" autoplay muted playsinline></video>
            <canvas id="canvas" width="640" height="480" style="display:none;"></canvas>
        </div>
        <input type="text" id="class-id" placeholder="Enter Class ID">
        <button id="scan-btn">Scan Attendance</button>
        <div id="results"></div>

        <script>
            const video = document.getElementById('webcam');
            const canvas = document.getElementById('canvas');
            const scanBtn = document.getElementById('scan-btn');
            const resultsDiv = document.getElementById('results');
            const classIdInput = document.getElementById('class-id');

            // WebSocket connection
            const socket = new WebSocket('ws://localhost:8000/students/scan-attendance');

            socket.onopen = function(e) {
                console.log('WebSocket connection established');
            };

            socket.onmessage = function(event) {
                resultsDiv.innerHTML = `Attendance: ${event.data}`;
            };

            socket.onerror = function(error) {
                console.log(`WebSocket Error: ${error}`);
            };

            async function startWebcam() {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                    video.srcObject = stream;
                    console.log("Webcam started successfully.");
                } catch (error) {
                    console.error("Error accessing webcam:", error);

                    if (error.name === "NotAllowedError") {
                        alert("Camera access was denied. Please allow access in your browser settings.");
                    } else if (error.name === "NotFoundError") {
                        alert("No camera found on this device. Please connect a camera and try again.");
                    } else if (error.name === "NotReadableError") {
                        alert("The camera is already in use by another application. Please close other apps and try again.");
                    } else {
                        alert("Unable to access your camera. Please check your device and browser settings.");
                    }
                }
            }

            window.onload = startWebcam;

            scanBtn.addEventListener('click', () => {
                const context = canvas.getContext('2d');
                context.drawImage(video, 0, 0, canvas.width, canvas.height);
                const imageData = canvas.toDataURL('image/jpeg');
                const classId = classIdInput.value;
                socket.send(imageData);
                socket.send(classId);
            });
        </script>
    </body>
    </html>
    """)
@router.get("/{student_id}", response_model=StudentSchema)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("/", response_model=StudentSchema)
def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    return create_student(db, student)

@router.put("/{student_id}", response_model=StudentSchema)
def modify_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    updated_student = update_student(db, student_id, student.dict())
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student

@router.delete("/{student_id}")
def remove_student(student_id: int, db: Session = Depends(get_db)):
    student = delete_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Student deleted"}

@router.post("/add-student/", response_model=StudentSchema)
async def add_student(
    first_name: str, 
    last_name: str, 
    email: str, 
    class_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    """Add a new student with their face image."""
    os.makedirs("students", exist_ok=True)

    try:
        contents = await file.read()
        np_img = np.frombuffer(contents, np.uint8)
        uploaded_image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    except Exception as e:
        return JSONResponse(content={"error": "Invalid image file"}, status_code=400)

    # Extract face encoding
    face_encodings = DeepFace.represent(img_path=uploaded_image, model_name="VGG-Face", enforce_detection=False)
    if not face_encodings:
        return JSONResponse(content={"error": "No face detected in the image"}, status_code=400)

    # Convert face encoding to bytes and then to base64 string
    face_encoding_bytes = np.array(face_encodings[0]["embedding"]).tobytes()
    face_encoding_base64 = base64.b64encode(face_encoding_bytes).decode('utf-8')

    # Create a new student instance with the face encoding
    student_create = StudentCreate(
        first_name=first_name,
        last_name=last_name,
        email=email,
        class_id=class_id,
        face_encoding=face_encoding_base64  # Store the face encoding as base64 string
    )
    student = create_student(db, student_create)

    # Save face image and update the photo_path
    student_image_path = f"students/student_{student.id}.jpg"
    cv2.imwrite(student_image_path, uploaded_image)

    # Update the student record with the photo_path
    student.photo_path = student_image_path
    db.commit()  # Commit the changes to the database

    return student

def extract_faces(image):
    """Detect faces in an image."""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return [image[y:y+h, x:x+w] for (x, y, w, h) in faces]

def filter_faces_by_class(faces, class_id, db):
    """Filter faces by class ID."""
    students = db.query(Student).filter(Student.class_id == class_id).all()
    recognized_faces = []  # List of recognized student IDs
    for face in faces:
        face_path = "uploaded_face.jpg"
        cv2.imwrite(face_path, face)
        for student in students:
            student_face_path = f"students/student_{student.id}.jpg"
            if not os.path.exists(student_face_path):
                print(f"Face image not found for student ID {student.id}")
                continue

            try:
                result = DeepFace.verify(
                    img1_path=face_path,
                    img2_path=student_face_path,
                    model_name="VGG-Face",
                    enforce_detection=False
                )
                if result["verified"]:
                    recognized_faces.append(student.id)
            except Exception as e:
                print(f"Error verifying student ID {student.id}: {str(e)}")

        if os.path.exists(face_path):
            os.remove(face_path)
    return recognized_faces
@router.websocket("/scan-attendance")
async def websocket_scan_attendance(websocket: WebSocket, db: Session = Depends(get_db)):
    """WebSocket endpoint for attendance scanning."""
    await websocket.accept()

    try:
        while True:
            image_data = await websocket.receive_text()

            if image_data.startswith("data:image/jpeg;base64,"):
                image_data = image_data.split(",")[1]

            np_img = np.frombuffer(base64.b64decode(image_data), np.uint8)
            uploaded_image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
            faces = extract_faces(uploaded_image)

            if not faces:
                await websocket.send_text("No face detected")
                continue

            class_id = await websocket.receive_text()  # Receive class ID from client
            recognized_faces = filter_faces_by_class(faces, class_id, db)

            today = str(date.today())
            all_students = db.query(Student).filter(Student.class_id == class_id).all()
            recognized_student_ids = set(recognized_faces)
            all_student_ids = set(student.id for student in all_students)
            absent_student_ids = all_student_ids - recognized_student_ids

            for student_id in recognized_student_ids:
                attendance = Attendance(
                    student_id=student_id,
                    class_id=class_id,
                    date=today,
                    status=AttendanceStatus.present
                )
                db.add(attendance)

            for student_id in absent_student_ids:
                attendance = Attendance(
                    student_id=student_id,
                    class_id=class_id,
                    date=today,
                    status=AttendanceStatus.absent
                )
                db.add(attendance)

            db.commit()

            result_message = f"Present: {', '.join(map(str, recognized_student_ids))}; Absent: {', '.join(map(str, absent_student_ids))}"
            await websocket.send_text(result_message)

    except WebSocketDisconnect:
        print("WebSocket connection closed")
    except Exception as e:
        print(f"Error in WebSocket: {str(e)}")
        await websocket.close()
import cv2
import mediapipe as mp
import speech_recognition as sr
import win32com.client
import threading
import time

# -------------------- Speech --------------------
speaker = win32com.client.Dispatch("SAPI.SpVoice")

last_spoken_direction = ""
last_speech_time = 0
speech_cooldown = 1.0


def speak(text):
    try:
        speaker.Speak(text)
    except Exception as e:
        print("Speech Error:", e)


# -------------------- Speech Recognition --------------------
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.pause_threshold = 0.8

voice_command = ""


def listen():
    global voice_command

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

        while True:
            try:
                audio = recognizer.listen(
                    source,
                    phrase_time_limit=2
                )

                command = recognizer.recognize_google(audio).lower()

                voice_command = command

                print("Voice:", command)

                if command == "stop":
                    break

            except sr.UnknownValueError:
                pass

            except Exception as e:
                print("Voice Error:", e)


threading.Thread(
    target=listen,
    daemon=True
).start()

# -------------------- MediaPipe --------------------
mp_face_mesh = mp.solutions.face_mesh
mp_draw = mp.solutions.drawing_utils

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# -------------------- Camera --------------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:

    ret, frame = cap.read()

    if not ret:
        continue

    frame = cv2.flip(frame, 1)

    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    direction = "CENTER"

    if results.multi_face_landmarks:

        for lm in results.multi_face_landmarks:

            mp_draw.draw_landmarks(
                frame,
                lm,
                mp_face_mesh.FACEMESH_TESSELATION
            )

            nose = lm.landmark[1]

            x = int(nose.x * w)
            y = int(nose.y * h)

            center_x = w // 2
            center_y = h // 2

            threshold = 30

            dx = x - center_x
            dy = y - center_y

            if abs(dx) > abs(dy):

                if dx > threshold:
                    direction = "RIGHT"

                elif dx < -threshold:
                    direction = "LEFT"

            else:

                if dy > threshold:
                    direction = "DOWN"

                elif dy < -threshold:
                    direction = "UP"

            cv2.circle(
                frame,
                (x, y),
                5,
                (0, 255, 0),
                -1
            )

    if direction != "CENTER":
        print("Detected:", direction)

    current_time = time.time()

    if (
        direction != "CENTER"
        and direction != last_spoken_direction
        and current_time - last_speech_time > speech_cooldown
    ):

        last_spoken_direction = direction
        last_speech_time = current_time

        if direction == "LEFT":
            threading.Thread(
                target=speak,
                args=("Turning left",),
                daemon=True
            ).start()

        elif direction == "RIGHT":
            threading.Thread(
                target=speak,
                args=("Turning right",),
                daemon=True
            ).start()

        elif direction == "UP":
            threading.Thread(
                target=speak,
                args=("Looking up",),
                daemon=True
            ).start()

        elif direction == "DOWN":
            threading.Thread(
                target=speak,
                args=("Looking down",),
                daemon=True
            ).start()

    if direction == "CENTER":
        last_spoken_direction = ""

    cv2.putText(
        frame,
        f"Head: {direction}",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Voice: {voice_command}",
        (30, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    cv2.imshow(
        "VISION Level 4.2",
        frame
    )

    if cv2.waitKey(1) == 27 or voice_command == "stop":
        break

cap.release()
cv2.destroyAllWindows()
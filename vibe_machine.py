import cv2
import os
import sys
import signal
from spotify import SpotifyManager, get_mood
from vibe_light import VibeLight
from visualizer.run_FFT_analyzer import run_FFT_analyzer

music = SpotifyManager()

light = VibeLight()

# face detection tutorial based on https://github.com/shantnu/PyEng
def webcam_face_detect(nogui = False, cascasdepath = "face_cascade.xml"):
    global light

    face_cascade = cv2.CascadeClassifier(cascasdepath)

    video_capture = cv2.VideoCapture(0)
    num_faces = 0


    while True:
        ret, image = video_capture.read()

        if not ret:
            break

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (30,30)

            )

        #print("The number of faces found = ", len(faces))
        num_faces = len(faces)

        if not nogui:
            for (x,y,w,h) in faces:
                cv2.rectangle(image, (x,y), (x+h, y+h), (0, 255, 0), 2)

            cv2.imshow("Faces found", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        music.change_playback(num_faces)
        if (light.is_on):
            mood = get_mood(num_faces)
            light.set_mood(mood)


    video_capture.release()
    cv2.destroyAllWindows()
    return num_faces

# Signal handler to stop music when exited
def handler(signum, frame):
    music.stop_playback()
    exit()
 

def main():
    if len(sys.argv) < 2:
        light.start()

    webcam_face_detect()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    child_pid = os.fork()
    if child_pid == 0:
        # new proc
        # run in a new thread
        if len(sys.argv) >= 2 and sys.argv[1] == 'v':
            run_FFT_analyzer()
    else:
        # orig proc  
        main()
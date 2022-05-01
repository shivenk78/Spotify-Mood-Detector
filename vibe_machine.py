import cv2
import sys
import signal
from spotify import SpotifyManager, get_mood
from vibe_light import VibeLight, Visualizer

music = SpotifyManager()

light = VibeLight()

# face detection code based on https://github.com/shantnu/PyEng
def webcam_face_detect(video_mode, nogui = False, cascasdepath = "face_cascade.xml"):

    face_cascade = cv2.CascadeClassifier(cascasdepath)

    video_capture = cv2.VideoCapture(video_mode)
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
        mood = get_mood(num_faces)
        light.set_mood(mood)


    video_capture.release()
    cv2.destroyAllWindows()
    return num_faces

# Signal handler to stop music when exited
def handler(signum, frame):
    music.stop_playback()
    exit()
 

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)

    if len(sys.argv) < 2:
        video_mode= 0
    else:
        video_mode = sys.argv[1]
    webcam_face_detect(video_mode)
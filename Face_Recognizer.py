import face_recognition
import cv2
import numpy as np
import os
import time

class FaceRecognizer:
    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    img_list = []
    known_face_encodings = []
    known_face_names = []
    face_locations = []
    face_encodings = []
    face_names = []
    img_count = 0
    process_this_fame = True

    def __init__(self):
        self.file_list = os.scandir("Assets")
        self.get_known_images()

    #Gets the stored inmages in the file
    def get_known_images(self):
        for file in self.file_list:
            if file.name.endswith(".png"):
                full_path = "Assets/" + str(file.name)
                temp_img = face_recognition.load_image_file(full_path)
                temp_encoding = face_recognition.face_encodings(temp_img)[0]

                name = str(file.name[:-4])
                self.known_face_encodings.append(temp_encoding)
                self.known_face_names.append(name)

                self.img_count += 1

    def process_face(self):
        if self.img_count == 0:
            return -1  #-1 indicates no face was found
        
        timer = 0
        while timer <= 5:
            ret, frame = self.video_capture.read()
            small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
            rgb_frame = small_frame[:, :, ::-1]

            #Process every other frame to save some time
            if self.process_this_fame:
                self.face_locations = face_recognition.face_locations(rgb_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"

                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        return name
            
            time.sleep(0.1)
            timer += 0.1

        return 0
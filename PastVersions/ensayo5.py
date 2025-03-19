import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import os
import face_recognition as fr

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition App")
        self.root.geometry("800x600")

        # Initialize camera
        self.cap = cv2.VideoCapture(0)

        # UI elements
        self.label = tk.Label(root)
        self.label.pack()

        # Face recognition data
        self.known_face_encodings, self.known_face_names = self.load_database()

        # Update frame
        self.update_frame()

    def load_database(self):
        known_face_encodings = []
        known_face_names = []

        # Path to the face database
        database_path = "database"

        for filename in os.listdir(database_path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(database_path, filename)
                face_image = fr.load_image_file(image_path)
                face_encoding = fr.face_encodings(face_image)[0]

                known_face_encodings.append(face_encoding)
                known_face_names.append(os.path.splitext(filename)[0])

        return known_face_encodings, known_face_names

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Realizar reconocimiento facial en este frame
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = fr.face_locations(rgb_frame)
            face_encodings = fr.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = fr.compare_faces(self.known_face_encodings, face_encoding)
                name = "Desconocido"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

            # Convertir a formato de imagen de tkinter y actualizar la UI
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.label.config(image=self.photo)

        self.root.after(10, self.update_frame)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.cap.release()
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()



import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import os
import face_recognition as fr
#############################################
import serial
import time
from pyModbusTCP.client import ModbusClient
#############################################


class FaceRecognitionApp:
    def __init__(self, root, esp32_ip, esp32_port):
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

        #############################################
        # ESP32 communication setup
        self.esp32_ip = esp32_ip
        self.esp32_port = esp32_port
        self.esp32_modbus = ModbusClient(host=self.esp32_ip, port=self.esp32_port, auto_open=True)
        time.sleep(2)  # Allow time for ESP32 to initialize
        #############################################

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

            # Valor User_i para el esp32
            User_i = 0
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = fr.compare_faces(self.known_face_encodings, face_encoding)
                name = "Desconocido"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]
                    User_i = 1
                    # print("Enviando valor 1")
                else:
                    User_i = 0
                    # print("Enviando valor 0")

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
            
            #############################################
            print("Indicador de Usuario: ", User_i)
            # Write '0' or '1' to Modbus registers based on user
            if User_i == 1:
                self.esp32_modbus.write_single_coil(0, 1)
                print("Enviando valor 1")  
            else:
                self.esp32_modbus.write_single_coil(0, 0) 
                print("Enviando valor 0") 
            #############################################

            # Convertir a formato de imagen de tkinter y actualizar la UI
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.label.config(image=self.photo)

        self.root.after(10, self.update_frame)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.cap.release()
            self.root.destroy()
            #############################################
            self.esp32_modbus.close()  # Close the Modbus connection
            #############################################

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root,'192.168.18.116',502)  ##PONER EL IP
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()



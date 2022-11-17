import PySimpleGUI as sg
from PIL import Image
from video_process import split_frames
import cv2 as cv
from record import webcam

def upload():
    sg.theme("GreenTan")

    layout=[
        [[sg.Text("Upload a JPG Image: "), sg.FileBrowse(key="user_pose_img", file_types=(("JPG Images", "*.jpg"),))], [sg.Button("Send Image")]],
         [sg.Text("")], 
         [sg.Text("OR:")], 
         [sg.Text("")], 
         [[sg.Text("Upload an AVI Video: "), sg.FileBrowse(key="user_pose_vid", file_types=(("AVI Video", "*.avi"),))], [sg.Button("Send Video")]],
         [sg.Text("")], 
         [sg.Text("OR:")], 
         [sg.Text("")], 
         [[sg.Button("Record Video")]]
         ]

    window = sg.Window(title="TennisNet - Pose Analysis", layout=layout, margins=(50, 50))

    while True: 
        event, values = window.read()
        if event == "Send Image" and values["user_pose_img"] is not None:
            Image.open(values["user_pose_img"]).save("input/user_pose.jpg")
            window.close()
            break
        elif event == "Send Video" and values["user_pose_vid"]:
            window.close()
            split_frames(values["user_pose_vid"])
            break
        elif event == "Record Video":
            window.close()
            webcam()
            pass
           
        elif event == sg.WIN_CLOSED:
            window.close()
            break
    


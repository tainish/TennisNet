import cv2
from video_process import split_frames

def webcam():
    #Capture video from webcam
    vid_path = "recording/cam_video.avi"
    vid_capture = cv2.VideoCapture(0)
    vid_cod = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

    frame_width = int(vid_capture.get(3))
    frame_height = int(vid_capture.get(4))

    size = (frame_width, frame_height)

    output = cv2.VideoWriter(vid_path, vid_cod, 20.0, size)
    while(True):
        # Capture each frame of webcam video
        ret,frame = vid_capture.read()

        cv2.imshow("Press X to Stop Recording", frame)
        if ret: 
            output.write(frame)

        # Close and break the loop after pressing "x" key
        if cv2.waitKey(1) &0XFF == ord('x'):
            break
    # close the already opened camera
    vid_capture.release()
    output.release()

    split_frames(vid_path)
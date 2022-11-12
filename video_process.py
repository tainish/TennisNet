import cv2

def split_frames(video):
    capture = cv2.VideoCapture(video) 
        #note: video format has to be avi - opencv will not support otherwise. 

    frame_n = 0
    while (capture.isOpened()):
        success, frame = capture.read()
        if success == False:
            break
        cv2.imwrite("input/frame_"+str(frame_n)+".png", frame)
        frame_n+=1

    capture.release()

#does not clear out unnecessary frames (e.g. empty frames)
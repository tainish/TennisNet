import cv2

def get_webcam():
    '''
	Shows webcam and allows user to capture a frame 

	Args: -

	Return:
		file_path, file path to save image of last frame before 'q' is pressed
        OR
        NULL, if 'c' is pressed
	'''

    win_name = 'Press q to take a picture'

    # Open webcam
    vid = cv2.VideoCapture(0)

    while(True):
        ret, frame = vid.read()

        cv2.imshow(win_name, frame)

        key = cv2.waitKey(1)
        if key:
            if key == ord('q'):
                break
            elif key == ord('c'):
                vid.release()
                cv2.destroyWindow(win_name)
                return

    vid.release()
    cv2.destroyWindow(win_name)

    # Save frame
    file_path = 'recording/'
    image_path = file_path + 'input/frame.jpg'
    cv2.imwrite(image_path, frame)
    print("Image saved in {}".format(file_path + 'input/frame.jpg'))

    return file_path
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def video_pose(video_path):
	'''
	Annotates the pose of the player onto each frame of the video input.

	Args:
		video file name: video file path is hardcoded to be ../test/input/ so only file name is necessary;
						 file extension must be cv2 supported

	Return:
		void, writes to output file in ../test/output/[file_name] with a copy of the original video with pose annotations on every frame
	'''

	BG_COLOR = (192, 192, 192) # gray
	INPUT_PATH = '../test/input/'
	OUTPUT_PATH = '../test/output/'

	cap = cv2.VideoCapture(INPUT_PATH + video_path)
	out = cv2.VideoWriter(OUTPUT_PATH + 'out_' + video_path, cv2.VideoWriter_fourcc('M','J','P','G'), 60, (cap.get(3), cap.get(4))) # 3 -> width, 4 -> height

	with mp_pose.Pose(
		static_image_mode=True,
		model_complexity=2,
		enable_segmentation=True,
		min_detection_confidence=0.5) as pose:

		while (cap.isOpened()):
			ret, frame = cap.read()

			# If video end, break
			if not ret: break

			image_height, image_width, _ = frame.shape

			# Convert the BGR image to RGB before processing.
			results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

			if not results.pose_landmarks:
				continue

			'''
			print(
				f'Nose coordinates: ('
				f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
				f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
			)
			'''

			annotated_image = frame.copy()

			# Draw segmentation on the frame.
			# To improve segmentation around boundaries, consider applying a joint
			# bilateral filter to "results.segmentation_mask" with "frame".
			condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
			bg_image = np.zeros(frame.shape, dtype=np.uint8)
			bg_image[:] = BG_COLOR
			annotated_image = np.where(condition, annotated_image, bg_image)

			# Draw pose landmarks on the frame.
			mp_drawing.draw_landmarks(
				annotated_image,
				results.pose_landmarks,
				mp_pose.POSE_CONNECTIONS,
				landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
			
			out.write(annotated_image)

			'''
			# Plot pose world landmarks.
			mp_drawing.plot_landmarks(
				results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
			'''
	
	# Release videos
	cap.release(0)
	out.release(0)

	cv2.destoryAllWindows()
import cv2
import glob
import mediapipe as mp
import numpy as np
import os
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def image_pose(in_folder_path='', debug=False):
	'''
	Annotates the pose of the player onto each frame of the video input.

	Args:
		video file name: video file path is hardcoded to be ../test/input/
	    so only file name is necessary;
						 file extension must be cv2 supported

	Return:
		array of keypoints, each an array of coordinates
	
		additionally writes to output file in ../test/output/[file_name] with a
		copy of the original video with pose annotations on every frame
	'''

	# Supported image types
	IMAGE_EXT = ['.png', '.jpg', '.jpeg', '.avi']
	input_file = in_folder_path + 'input\\'
	output_file = in_folder_path + 'output\\'

	IMAGE_FILES = []
	# Find all images in folder
	for ext in IMAGE_EXT:
		for filename in glob.glob(input_file + '*' + ext):
			IMAGE_FILES.append(filename)
	
	image_results = []

	BG_COLOR = (192, 192, 192) # gray
	with mp_pose.Pose(
		static_image_mode=True,
		model_complexity=2,
		enable_segmentation=True,
		min_detection_confidence=0.5) as pose:
		for idx, file in enumerate(IMAGE_FILES):
			image = cv2.imread(file)
			image_height, image_width, _ = image.shape
			# Convert the BGR image to RGB before processing.
			results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

			image_results.append(results)

			if debug:
				if not results.pose_landmarks:
					continue
				
				print(
					f'Nose coordinates: ('
					f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
					f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
				)

				# Names of pose landmarks (the nodes it detects) and id to landmark mapping
				print(vars(mp_pose.PoseLandmark))

				annotated_image = image.copy()

				# Draw segmentation on the image.
				# To improve segmentation around boundaries, consider applying a joint
				# bilateral filter to "results.segmentation_mask" with "image".
				condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
				bg_image = np.zeros(image.shape, dtype=np.uint8)
				bg_image[:] = BG_COLOR
				annotated_image = np.where(condition, annotated_image, bg_image)

				# Draw pose landmarks on the image.
				mp_drawing.draw_landmarks(
					annotated_image,
					results.pose_landmarks,
					mp_pose.POSE_CONNECTIONS,
					landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

				# Write image to file for debugging
				cv2.imwrite(output_file + os.path.basename(file), annotated_image)

				# Plot pose world landmarks to see 3d model
				#mp_drawing.plot_landmarks(
				#	results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

	return image_results
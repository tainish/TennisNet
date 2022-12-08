import cv2
import glob
import mediapipe as mp
import numpy as np
import os
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def image_pose(folder_path='./', debug=False, verbose=False, plot_model=False):
	'''
	Annotates the pose of the player onto each frame of the video input.

	Args:
		folder_path: video file should be in input folder relative to folder_path;
					 file extension of the video file must be cv2 supported

		debug: output coordinates of an example landmark and write
			   annotated images to output file

		verbose: print landmark to id mapping

		plot_model: display 3d model of entire pose

	Return:
		array of keypoints, each an array of coordinates
		array of image file paths in whatever order the program read them
	
		additionally writes to output file in ../test/output/[file_name] with a
		copy of the original video with pose annotations on every frame
	'''

	# Supported image types
	IMAGE_EXT = ['.png', '.jpg', '.jpeg', '.avi']
	input_file = folder_path + 'input/'
	output_file = folder_path + 'output/'

	IMAGE_FILES = []
	# Find all images in folder
	for ext in IMAGE_EXT:
		for filename in glob.glob(input_file + '*' + ext):
			IMAGE_FILES.append(filename)
	
	image_results = []
	image_files = []

	BG_COLOR = (192, 192, 192) # gray
	with mp_pose.Pose(
		static_image_mode=True,
		model_complexity=2,
		enable_segmentation=True,
		min_detection_confidence=0.5) as pose:
		for idx, file in enumerate(IMAGE_FILES):
			image = cv2.imread(file)
			image_files.append(file)

			image_height, image_width, _ = image.shape
			# Convert the BGR image to RGB before processing.
			results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

			image_results.append(results)

			if debug:
				if not results.pose_landmarks:
					continue
				
				print(
					f'Right shoulder coordinates: ('
					f'{results.pose_landmarks.landmark[12].x * image_width}, ' # 12 maps to the right shoulder landmark
					f'{results.pose_landmarks.landmark[12].y * image_height},'
					f'{results.pose_landmarks.landmark[12].z})'
				)

				if verbose:
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
				cv2.imwrite(output_file + os.path.basename(file), annotated_image) #don't thin that this file write is working... my output folder still has Taiga's original test image

				# Plot pose world landmarks to see 3d model
				if plot_model:
					mp_drawing.plot_landmarks(
						results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

	return image_results, image_files
import math

def scaler(pose):
	'''
	Normalizes the pose by scaling the shoulder to hip distance
	(averaged between left and right) to 1 and use right shoulder
	as origin

	Args:
		pose: BlazePose pose.process result (see BlazePose.py)

	Return:
		33, 3 array of scaled coordinates; also converts to normal array
	'''
	# 12: Right shoulder
	# 24: Right hip
	# 11: Left shoulder
	# 23: Left hip

	MIN_VIS = 0.3

	chest_L = -1
	chest_R = -1
	# Get the distance between the shoulder and the hip; TODO: figure out why pose_world_landmarks is NoneType for some images
	if pose.pose_world_landmarks.landmark[11] is not None and pose.pose_world_landmarks.landmark[23] is not None:
		chest_L = math.sqrt(pow(pose.pose_world_landmarks.landmark[11].x - pose.pose_world_landmarks.landmark[23].x, 2)
						 + pow(pose.pose_world_landmarks.landmark[11].y - pose.pose_world_landmarks.landmark[23].y, 2)
						 + pow(pose.pose_world_landmarks.landmark[11].z - pose.pose_world_landmarks.landmark[23].z, 2))
	if pose.pose_world_landmarks.landmark[12] is not None and pose.pose_world_landmarks.landmark[24] is not None:
		chest_R = math.sqrt(pow(pose.pose_world_landmarks.landmark[12].x - pose.pose_world_landmarks.landmark[24].x, 2)
						 + pow(pose.pose_world_landmarks.landmark[12].y - pose.pose_world_landmarks.landmark[24].y, 2)
						 + pow(pose.pose_world_landmarks.landmark[12].z - pose.pose_world_landmarks.landmark[24].z, 2))

	if chest_L == -1 and chest_R >= 0:
		chest_len = chest_R
	elif chest_R == -1 and chest_L >= 0:
		chest_len == chest_L
	elif chest_L >= 0 and chest_R >= 0:
		#  Right side is exposed to the camera which results in higher reliability)
		chest_len = chest_R * 0.7 + chest_L * 0.3
	else:
		chest_len = 0
		raise ValueError("Torso landmarks undetected")

	scale = 1 / chest_len
	corrected_pos = []
	for node in pose.pose_world_landmarks.landmark:
		# Use Right shoulder as origin
		dx = (node.x - pose.pose_world_landmarks.landmark[12].x) * scale
		dy = (node.y - pose.pose_world_landmarks.landmark[12].y) * scale
		dz = (node.z - pose.pose_world_landmarks.landmark[12].z) * scale

		corrected_pos.append([dx, dy, dz])

	return corrected_pos
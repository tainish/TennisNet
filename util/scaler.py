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

	# Get the distance between the shoulder and the hip
	chest_L = math.sqrt(pow(pose.world_landmarks.landmark[11].x - pose.world_landmarks.landmark[23].x, 2)
					 + pow(pose.world_landmarks.landmark[11].y - pose.world_landmarks.landmark[23].y, 2)
					 + pow(pose.world_landmarks.landmark[11].z - pose.world_landmarks.landmark[23].z, 2))
	chest_R = math.sqrt(pow(pose.world_landmarks.landmark[12].x - pose.world_landmarks.landmark[24].x, 2)
					 + pow(pose.world_landmarks.landmark[12].y - pose.world_landmarks.landmark[24].y, 2)
					 + pow(pose.world_landmarks.landmark[12].z - pose.world_landmarks.landmark[24].z, 2))

	# If the visilibility is not high enough, ignore
	if pose.world_landmarks.landmark[11].visibility < MIN_VIS or pose.world_landmarks.landmark[23].visibility < MIN_VIS:
		chest_len = chest_R
	else:
		#  Right side is exposed to the camera which results in higher reliability)
		chest_len = chest_R * 0.7 + chest_L * 0.3

	scale = 1 / chest_len
	corrected_pos = []
	for node in pose.world_landmarks.landmark:
		# Use Right shoulder as origin
		dx = (node.x - pose.world_landmarks.landmark[12].x) * scale
		dy = (node.y - pose.world_landmarks.landmark[12].y) * scale
		dz = (node.z - pose.world_landmarks.landmark[12].z) * scale

		corrected_pos.append([dx, dy, dz])

	return corrected_pos
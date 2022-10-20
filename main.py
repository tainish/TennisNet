from src.BlazePose import image_pose

if not image_pose('test\\'):
	print("Not working")
	exit()

user_results = image_pose()
pro_results = image_pose('ground_truth\\')


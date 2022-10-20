from util.BlazePose import image_pose

if not image_pose('test\\'):
	print("Not working")
	exit()

user_results = image_pose(debug=True)
pro_results = image_pose('ground_truth\\')


print(len(user_results))
print(len(pro_results))
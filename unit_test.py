'''
	TODO: make this into an actual unit test using pytest
	TODO: also automate this for github

	this looks so scuffed :(
'''

from util.BlazePose import image_pose
from util.scaler import scaler

assert image_pose('debug\\'), "Either debug\\ doesn't exist or image_pose isn't working"
	
pro_results = image_pose('ground_truth\\')

assert pro_results, "No file path ground_truth\\"
assert len(pro_results) == 100, "Images missing in ground_truth"

user_results = image_pose(debug=True)

print(type(user_results[0]))

assert user_results, "No images found in input\\ folder"
assert scaler(user_results[0]), "scaler function unsuccessful"
'''
	TODO: make this into an actual unit test using pytest
	TODO: also automate this for github

	Description for each test can be found in the error message next to each assert line
'''

from util.BlazePose import image_pose
from util.coord_to_mpl import coord_to_mpl
from util.rmse import rmse
from util.scaler import scaler

assert image_pose('debug/'), "Either debug\\ doesn't exist or image_pose isn't working"
	
pro_results, _ = image_pose('ground_truth/')

assert pro_results, "No file path ground_truth/"
assert len(pro_results) == 100, "Images missing in ground_truth"

user_results, _ = image_pose(debug=True)

assert user_results, "No images found in input/ folder"
assert scaler(user_results[0]), "scaler function unsuccessful"

# rmse tests
assert rmse([[0, 0, 0]], [[0, 0, 0]]) == 0
assert rmse([[2.5, 3.5, 8.8]], [[2.5, 3.5, 8.8]]) == 0
assert abs(rmse([[0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 0, 3]], [[0, 2, 1], [2, 0, 1], [0, 0, 3], [0, 0, 3]]) - 1.5) < 0.1 # Range since float point errors

# coord_to_mpl tests
assert coord_to_mpl([[1, 2, 3], [2, 3, 5], [3, 4, 5]])
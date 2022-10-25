import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

from util.BlazePose import image_pose
form util.coord_to_mpl import coord_to_mpl
from util.rmse import rmse
from util.scaler import scaler

# Obtain pose results of user image and ground_truth images
user_poses = image_pose()
pro_poses = image_pose('ground_truth\\')

# Normalize pose results
user_pose_norm = scaler(user_poses[0])
pro_pose_norms = []
for pro_pose in pro_poses:
	pro_pose_norms.append(scaler(pro_pose))

# Find closest professional pose to user pose
closest_pose_id = 0
i = 0
best_score = sys.maxsize # To be minimized
for pro_pose in pro_pose_norms:
	if i > 5: # Ignore face
		score = rmse(pro_pose, user_pose_norm)
		if score < best_score:
			best_score = score
			closest_pose_id = i

	i += 1

pro_x, pro_y, pro_z = coord_to_mpl(pro_pose)
user_x, user_y, user_z = coord_to_mpl(user_pose_norm)

# Plot both poses on the same graph
fig = plt.figure()
ax = plt.axes(projection='3d')


ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');
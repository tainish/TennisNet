import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

from util.BlazePose import image_pose
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
	score = rmse(pro_pose, user_pose_norm)
	if score < best_score:
		best_score = score
		closest_pose_id = i

	i += 1

# Plot both poses on the same graph
fig = plt.figure()
ax = plt.axes(projection='3d')

ax = plt.axes(projection='3d')

# Data for a three-dimensional line
zline = np.linspace(0, 15, 1000)
xline = np.sin(zline)
yline = np.cos(zline)
ax.plot3D(xline, yline, zline, 'gray')

# Data for three-dimensional scattered points
zdata = 15 * np.random.random(100)
xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');
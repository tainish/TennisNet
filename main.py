import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from mpl_toolkits import mplot3d
import sys

from util.BlazePose import image_pose
from util.coord_to_mpl import coord_to_mpl
from util.rmse import rmse
from util.scaler import scaler
from upload import upload
import matplotlib.image as mpimg 

# Here is upload (normal tkinter deprecated on mac)
# upload()

# Obtain pose results of user image and ground_truth images
user_poses, user_files = image_pose()
pro_poses, pro_files = image_pose('ground_truth/')

# Normalize pose results
user_pose_norm = scaler(user_poses[0])
pro_pose_norms = []
image_num = 1
for pro_pose in pro_poses:
	try:
		pro_pose_norms.append(scaler(pro_pose))
	except:
		print("Image {} raised an exception when inputted through the scaler function".format(image_num))

	image_num += 1

# Find closest professional pose to user pose --> assuming this is the desired swing
closest_pose_id = 0
i = 0
best_score = sys.maxsize # To be minimized
for pro_pose in pro_pose_norms:
	score = rmse(pro_pose[11:], user_pose_norm[11:]) # Ignore face
	print("Best score: {}".format(best_score))
	print("Score: {}".format(score))
	if score < best_score:
		best_score = score
		closest_pose_id = i

	i += 1

print("Best fit ground_truth is {}".format(pro_files[closest_pose_id]))
#advice(pro_files[closest_pose_id], user_pose_norm[11:])

# Again, ignore face
pro_x, pro_y, pro_z = coord_to_mpl(pro_pose_norms[closest_pose_id][11:])
user_x, user_y, user_z = coord_to_mpl(user_pose_norm[11:])

# Plot both poses on the same graph
fig, ax = plt.subplots(1, 3)

#attempt to plot images side by side for view comparison
#fig, ax = plt.subplots()

ax[1] = plt.axes(projection='3d')

# Switch y and z and make z (in mpl) negative to convert from BlazePose coordinates to MatPlotLib coordinates
ax[1].scatter3D(pro_x, pro_z, np.negative(pro_y), c=pro_z, cmap='Greens')
ax[1].scatter3D(user_x, user_z, np.negative(user_y), c=user_z, cmap='Reds')

# Connected segments in a pose ignoring face
connected_landmarks = [[11, 12],
					[11, 13],
					[11, 23],
					[12, 14],
					[12, 24],
					[13, 15],
					[14, 16],
					[15, 21],
					[15, 17],
					[15, 19],
					[16, 18],
					[16, 20],
					[16, 22],
					[17, 19],
					[18, 20],
					[23, 24],
					[23, 25],
					[24, 26],
					[25, 27],
					[26, 28],
					[27, 29],
					[27, 31],
					[28, 30],
					[28, 32],
					[29, 31],
					[30, 32]]

connected_landmarks = [[s[0] - 11, s[1] - 11] for s in connected_landmarks] # Adjust ids due to removed face nodes

for segment in connected_landmarks:
	ax[1].plot([pro_x[segment[0]], pro_x[segment[1]]], [pro_z[segment[0]], pro_z[segment[1]]], [-pro_y[segment[0]], -pro_y[segment[1]]], c='black')
	ax[1].plot([user_x[segment[0]], user_x[segment[1]]], [user_z[segment[0]], user_z[segment[1]]], [-user_y[segment[0]], -user_y[segment[1]]], c='black')

ax[0].imshow(Image.open(user_files[0]))
ax[0].set_title("User Pose")
ax[0].set_xlabel("Red Points")
ax[0].set_xticks([])
ax[0].set_yticks([])


ax[2].imshow(Image.open(pro_files[closest_pose_id]))
ax[2].set_title("Best Match Pro Pose")
ax[2].set_xlabel("Green Points")
ax[2].set_xticks([])
ax[2].set_yticks([])

plt.show()
# TennisNet
 
An application of BlazePose on tennis forms.

### Usage:

Go to macOS branch for mac M1 users.

1.  Record a video of a swing such that the camera is pointing towards the left side of the court from the right side with the center of view in line with the player (slo-mo is recommended for higher fps). Extract the frame where the racquet hits the ball and save it as an image.
	-  Alternatively stop the swing in the impact position and take a picture.
2.  Upload images of the impact pose into the `input/` folder and delete pre-existing images.
3.  Install dependencies in a virtual environment with `pip install -r requirements.txt`, then run `main.py`.
4.  The green plot is the professional and the red plot is the user.
5.	If the actual image of the professional model is desired, there should have been an id printed into command prompt, 
	

# Development

## User Interface Structure

(This is the goal; not necessarily implemented for MVP)

#### Steps:
1.  Run the program; a video recording thing pops up
2.  Press record to start recording. The user can back away, take a swing, then run back to stop the recording.
3.  Stopping the recording pulls up a side by side between the user's swing clip and a professional's swing clip with similar form.
    -  Poses are annotated on the video and can be seen as the video of the side by sides are played.
    -  The loss/error value is displayed, which changes every frame.
    -  Analysis is also displayed, which changes based on which part of the swing, split by start of the swing, the prepared position, the ball impact position, and the post-follow through position.
       -  The analysis is a 3d model of the hand trajectory from both the user's and the professional's poses.

## High level overview of algorithm for tennis swing analysis

### Full version overview

(May be compromised with simpler steps for MVP)

1.  BlazePose can be used to obtain the basic pose of the user's swing.
    -  BlazePose, unlike other pose estimation models, can also detect, albeit still quite inconsistent, the depth of each joint. To fix the inconsistency, we may input bone lengths and use a simple least squares optimization in an attempt to make the depth more consistent and accurate.
	-  See https://google.github.io/mediapipe/solutions/pose.html
2.  With all three coordinates of each joint, a complete 3D model can be made and we can standardize the models by scaling based on upper body length (it seems to have the most accurate depth position).
3.  Do a frame by frame detection of the ready pose, preparation pose, impact pose, and end pose, and record all frames where the detection model detects any of the poses. Find all instances of ready pose, preparation pose, impact pose, and end pose in a row and record those frames as an array of quadruples.
4.  For a little more setup before moving on, we need a ground truth swing:
    -  Use BlazePose on all professional swings and use a clustering model to group them into different types of swings.
	-  Find a swing path with the least loss when compared with all the swings in the group to represent the "optimal swing" of the group.
    -  Split the swing using the 4 key poses mentioned above.
5.  Compare each splice (from the key poses) of the user's swing to the optimal swing with the least loss from the user's swing as it will most likely be the desired type of swing to compare to.
    -  Give advice based on positional difference. eg. more upward if user's swing is low

### MVP version overview

##### Goal:

Only gives analysis for key poses rather than the full swing

1.  BlazePose can be used to obtain the basic pose of a swing.
    -  BlazePose, unlike other pose estimation models, can also detect, albeit still quite inconsistent, the depth of each joint. To fix the inconsistency, we may input bone lengths and use a simple least squares optimization in an attempt to make the depth more consistent and accurate.
2.  We need a ground truth swing:
    -  Standardize all professional swing poses after using BlazePose and take the average for the "optimal" swing, or the swing with the least loss from all professional swings.
    -  Mark 4 key poses for all swings: ready pose, preparation pose, impact pose, and end pose; use a detection model and train using this dataset to detect these key poses
3.  With all three coordinates of each joint, a complete 3D model can be made.
    -  Detect 4 key poses: ready pose, preparation pose, impact pose, and end pose using the detection model
4.  Compare key poses of the user's swing and professional swing, then show the difference between the two for analysis.

##### What I'm probably going to achieve

Only gives analysis for one pose (impact with the ball)

1.  BlazePose can be used to obtain the basic pose of the impact position.
2.  We need a ground truth swing:
    -  Use Roger Federer's swing and treat each impact position as a different type and standardize based on upper body length.
3.  Find the position with the least loss from the user's and show a side by side comparison as well as an overlapped version.

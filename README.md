# TennisNet
 
An application of MoveNet on tennis forms.

## User Interface Structure

(This is the goal; not necessarily implemented for MVP)

Steps:
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

1.  MoveNet can be used to obtain the basic pose of the user's swing.
    -  MoveNet, unlike other pose estimation models, can also detect, albeit still quite inconsistent, the depth of each joint. To fix the inconsistency, we may input bone lengths and use a simple least squares optimization in an attempt to make the depth more consistent and accurate.
2.  With all three coordinates of each joint, a complete 3D model can be made.
3.  Do a frame by frame detection of the ready pose, preparation pose, impact pose, and end pose, and record all frames where the detection model detects any of the poses. Find all instances of ready pose, preparation pose, impact pose, and end pose in a row and record those frames as an array of quadruples.
4.  For a little more setup before moving on, we need a ground truth swing:
    -  Standardize all professional swing poses after using MoveNet and take the average for the "optimal" swing, or the swing with the least loss from all professional swings.
    -  Split the swing using the 4 key poses mentioned above.
5.  Compare each splice (from the key poses) of the user's swing to the optimal swing
    -  Give advice based on positional difference. eg. more upward if user's swing is low

### MVP version overview

Only gives analysis for key poses rather than the full swing

1.  MoveNet can be used to obtain the basic pose of a swing.
    -  MoveNet, unlike other pose estimation models, can also detect, albeit still quite inconsistent, the depth of each joint. To fix the inconsistency, we may input bone lengths and use a simple least squares optimization in an attempt to make the depth more consistent and accurate.
2.  We need a ground truth swing:
    -  Standardize all professional swing poses after using MoveNet and take the average for the "optimal" swing, or the swing with the least loss from all professional swings.
    -  Mark 4 key poses for all swings: ready pose, preparation pose, impact pose, and end pose; use a detection model and train using this dataset to detect these key poses
3.  With all three coordinates of each joint, a complete 3D model can be made.
    -  Detect 4 key poses: ready pose, preparation pose, impact pose, and end pose using the detection model
4.  Compare key poses of the user's swing and professional swing, then show the difference between the two for analysis
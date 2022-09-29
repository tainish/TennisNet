# TennisNet
 
An application of BlazePose on tennis forms.

## Usage

(This is the goal; not necessarily implemented for MVP)

Steps:
1.  Run the program; a video recording thing pops up
2.  Press record to start recording. The user can back away, take a swing, then run back to stop the recording.
3.  Stopping the recording pulls up a side by side between the user's swing clip and a professional's swing clip with similar form.
    -  Poses are annotated on the video and can be seen as the video of the side by sides are played.
    -  The loss/error value is displayed, which changes every frame.
    -  Analysis is also displayed, which changes based on which part of the swing, split by start of the swing, the prepared position, the ball impact position, and the post-follow through position.
        - Analysis contains a 3d model of the hand trajectory from both the user's and the professional's poses.

## Algorithm for tennis swing analysis

(May be compromised with simpler steps for MVP)

1. 
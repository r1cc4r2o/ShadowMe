import cv2
import sys
import pickle
import numpy as np
import mediapipe as mp
from angle import combJointAngle
from landmark import extractLandmarks
from jointRotations import JOINT_ROTATIONS



# initialize
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

dictionary = dict() # here we store all the coordinates of each frame
frm = 0 # index of the current frame

pose = mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6)

cap = cv2.VideoCapture(sys.argv[1])

if cap.isOpened() == False:
    print("No file available with this name")
    raise TypeError

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# output directory, input file name
outdir, inputfilename = sys.argv[1][:sys.argv[1].rfind('/')+1], sys.argv[1][sys.argv[1].rfind('/')+1:]
# separate filename, extension
filename, extension = inputfilename.split('.')

out_filename = f'{outdir}{filename}_annotated.{extension}'
out = cv2.VideoWriter(out_filename, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 10, (frame_width, frame_height))

while cap.isOpened():
    # initialize
    ret, image = cap.read()
    if not ret:
        break
    # Store the RGB color in the frame
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Process and detect landmarks but 
    # remove the color from the image
    results = pose.process(image)

    # Recoloring the image
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # try to extract the landmarks
    # 1: extract the landmarks
    # 2: save dict coords current frame
    dictionary['coordsFrame_'+str(frm)] = extractLandmarks(mp_pose, results)
    # compute the angle between the joints
    dictionary['angleFrame_'+str(frm)] = combJointAngle(dictionary['coordsFrame_'+str(frm)], JOINT_ROTATIONS)
    
    frm = frm + 1 # next frame

    # plot the landmark and the connections in the current rendered frame  
    mp_drawing.draw_landmarks(image, # current frame
                                results.pose_landmarks, # each pose landmarks
                                mp_pose.POSE_CONNECTIONS, # each pose connections
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), # the joint
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)  # the connection
                                )
    
    out.write(image)

# save the dictionary into a file
with open('dictLandmarks.pickle', 'wb') as handle:
    pickle.dump(dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)

pose.close()
cap.release()
out.release()

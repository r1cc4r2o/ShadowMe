import cv2
import sys
import pickle
import numpy as np
import mediapipe as mp
from Angle import combJointAngle
from Landmark import extractLandmarks
from JointRotations import JOINT_ROTATIONS
from Angle3D import Angle

realTime = False

# initialize
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

dictionary = dict() # here we store all the coordinates of each frame
frm = 0 # index of the current frame

pose = mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6)

if realTime:
    cap = cv2.VideoCapture(1)
else:
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
out = cv2.VideoWriter(out_filename, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 24, (frame_width, frame_height))

while True:
    if not realTime and not cap.isOpened():
        break

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

    # dictionary['coordsFrame_'+str(frm)] = {}
    dictionary['angleFrame_'+str(frm)] = {}
    i = 0
    for joints in JOINT_ROTATIONS:
        positions = dictionary['coordsFrame_'+str(frm)]
        point_a = (positions[joints[0]].x, positions[joints[0]].y, positions[joints[0]].z)
        point_b = (positions[joints[1]].x, positions[joints[1]].y, positions[joints[1]].z)
        point_c = (positions[joints[2]].x, positions[joints[2]].y, positions[joints[2]].z)
        angle = Angle(point_a, point_b, point_c)
        i += 1
        cv2.putText(image, 
                    f'{joints} | {angle.compute()[0]}, {angle.compute()[1]}, {angle.compute()[2]}', 
                    (50, 50 + 55*i), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, 
                    (0, 0, 0), 
                    2, 
                    cv2.LINE_4)

        dictionary['angleFrame_'+str(frm)][f'({joints[0]}, {joints[1]}, {joints[2]})'] = angle.compute()
    
    frm = frm + 1 # next frame

    # plot the landmark and the connections in the current rendered frame  
    mp_drawing.draw_landmarks(image, # current frame
                                results.pose_landmarks, # each pose landmarks
                                mp_pose.POSE_CONNECTIONS, # each pose connections
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), # the joint
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)  # the connection
                                )

    out.write(image)

    if realTime:
        cv2.imshow('frame', image)

        if cv2.waitKey(1) == ord('q'):
            break
        

# save the dictionary into a file
with open('/Users/riccardotedoldi/Desktop/ais/I/sem2/cv/project/PoseEstimationTo3Drender/poseExtraction/data/dictLandmarks.pickle', 'wb') as handle:
    pickle.dump(dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)

pose.close()
cap.release()
out.release()

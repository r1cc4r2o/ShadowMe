

def extractLandmarks(mp_pose, estimated):
    r""" This function extract the landmarks.

        Input:
            mp_pose: mediapipe.python.solutions.pose 
            estimated: estimated.pose_landmarks.landmark
        
        Output:
            d: dict {'0': 
                        x coord_x
                        y coord_y
                        z coord_z
                        visibility # confidence
                     '1': 
                        ...
                        ...
                    } # coords of the current frame

    """
    # we use a try except because in some case 
    # when the subject is occluded isn't possi-
    # ble to extract the landmark
    try:
        landmarks = estimated.pose_landmarks.landmark
    except:
        pass

    d = dict() # dictionary of the landmarks of the current frame
    for i, j in zip(landmarks, mp_pose.PoseLandmark):
        d[j+1] = i
    
    return d
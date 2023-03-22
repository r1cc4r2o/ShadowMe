import numpy as np


def calculateAngle(a, b, c):
    r""" That function given the coords of the
        joints as a list provide in output the
        angle in the joint b.

            Input:
                a: list [x ,y]
                b: list [x ,y]
                c: list [x ,y]

            Output:
                angle: float angle
            
    """
    # cast coords
    a = np.array(a) 
    b = np.array(b) 
    c = np.array(c) 
    
    # compute the angle
    # source: https://stackoverflow.com/questions/1211212/how-to-calculate-an-angle-from-three-points
    #                     result = atan2(P3.y - P1.y, P3.x - P1.x) - atan2(P2.y - P1.y, P2.x - P1.x);
    radians = np.arctan2(c[1]-b[1], c [0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs (radians*180.0/np.pi)
    
    # make sure the angle angle<180.0
    if angle>180.0:
        angle = 360-angle
    return angle

def combJointAngle(dictionary, comb_joint):
    r""" Compute the angle between the joints
        combinations.

            Input:
                dictionary: dict {'0': 
                                    x coord_x
                                    y coord_y
                                    z coord_z
                                    visibility # confidence
                                  '1': 
                                    ...
                                    ...
                                }
                comb_joint: list [(a, b, c), ...]

            Output:
                angles: list of float contains the computed angles
            
    """
    
    angles = [calculateAngle(
                [dictionary[a].x, dictionary[a].y], 
                [dictionary[b].x, dictionary[b].y],
                [dictionary[c].x, dictionary[c].y] ) for (a, b, c) in comb_joint]
    return angles
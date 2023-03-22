"""
    In the dictionary I have stored the values
    of the joints in this order:
        O. nose
        1. left_eye_inner
        2. left_eye
        3. left_eye_outer
        4. right_eye_inner
        5. right_eye
        6. right_eye_outer
        7. left_ear
        8. right_ear
        9. mouth_left
        10. mouth_right
        11. left_shoulder
        12. right_shoulder
        13. left_elbow
        14. right_elbow
        15. left_wrist
        16. right_wrist
        17. left_pinky
        18. right_pinky
        19. left_index
        20. right_index
        21. left thumb
        22. right_thumb
        23. left_hip
        24. right_hip
        25. left_knee
        26. right_knee
        27. left_ankle
        28. right_ankle
        29. left_heel
        30. right_heel
        31. left_foot_index
        32. right_foot_index
        
"""
# JOINT_ROTATIONS = [(19,15,21),
#                     (21,15,13),
#                     (13,15,17), 
#                     (15,13,11),
#                     (13,11,12),
#                     (13,11,23),

#                     (11,12,14),
#                     (12,14,16),
#                     (14,16,22),
#                     (14,16,20),
#                     (14,16,18),
#                     (24,12,14),


#                     (23,24,26),
#                     (24,26,28),
#                     (26,28,32),
#                     (26,28,30),

#                     (24,23,25),
#                     (23,25,27),
#                     (25,27,31),
#                     (25,27,29)]

JOINT_ROTATIONS = [
    #(11, 13, 23), # Left shoulder
    #(12, 14, 24), # Right shoulder
    (13, 11, 23), # Left shoulder
    (14, 12, 24), # Right shoulder
]
import threading
import time
import bpy
from math import *
from mathutils import Euler
import json

# MAN
mapping = {
    '2': 'CC_Base_L_Eye',
    '5': 'CC_Base_R_Eye',
    '11': 'CC_Base_L_Clavicle',
    '12': 'CC_Base_R_Clavicle',
    '13': 'CC_Base_L_ElbowShareBone',
    '14': 'CC_Base_R_ElbowShareBone',
    '15': 'CC_Base_L_Hand',
    '16': 'CC_Base_R_Hand',
    '17': 'CC_Base_L_Pinky3',
    '18': 'CC_Base_R_Pinky3',
    '19': 'CC_Base_L_Index3',
    '20': 'CC_Base_R_Index3',
    '21': 'CC_Base_L_Thumb3',
    '22': 'CC_Base_R_Thumb3',
    '23': 'CC_Base_L_Thigh',
    '24': 'CC_Base_R_Thigh',
    '25': 'CC_Base_L_KneeShareBone',
    '26': 'CC_Base_R_KneeShareBone',
    '27': 'CC_Base_L_Foot',
    '28': 'CC_Base_R_Foot',
    '29': 'CC_Base_L_Foot',
    '30': 'CC_Base_R_Foot',
    '31': 'CC_Base_L_BigToe1',
    '32': 'CC_Base_R_BigToe1'
}

# Simple skeleton
mapping = {
    '2': 'CC_Base_L_Eye',
    '5': 'CC_Base_R_Eye',
    '11': 'shoulder.L',
    '12': 'shoulder.R',
    '13': 'forearm_fk.L',
    '14': 'forearm_fk.R',
    '15': 'CC_Base_L_Hand',
    '16': 'CC_Base_R_Hand',
    '17': 'CC_Base_L_Pinky3',
    '18': 'CC_Base_R_Pinky3',
    '19': 'CC_Base_L_Index3',
    '20': 'CC_Base_R_Index3',
    '21': 'CC_Base_L_Thumb3',
    '22': 'CC_Base_R_Thumb3',
    '23': 'ORG-pelvis.L',
    '24': 'ORG-pelvis.R',
    '25': 'CC_Base_L_KneeShareBone',
    '26': 'CC_Base_R_KneeShareBone',
    '27': 'CC_Base_L_Foot',
    '28': 'CC_Base_R_Foot',
    '29': 'CC_Base_L_Foot',
    '30': 'CC_Base_R_Foot',
    '31': 'CC_Base_L_BigToe1',
    '32': 'CC_Base_R_BigToe1'
}

# Simple skeleton NO rig
mapping = {
    #'2': 'CC_Base_L_Eye',
    #'5': 'CC_Base_R_Eye',
    '11': 'shoulder.L',
    '12': 'shoulder.R',
    '13': 'forearm.L',
    '14': 'forearm.R',
    '15': 'hand.L',
    '16': 'hand.R',
    '17': 'f_pinky.01.L',
    '18': 'f_pinky.01.R',
    '19': 'f_index.01.L',
    '20': 'f_index.01.L',
    '21': 'thumb.01.L',
    '22': 'thumb.01.L',
    '23': 'thigh.L', # maybe pelvis.L
    '24': 'thigh.R', # maybe pelvis.R
    '25': 'shin.L',
    '26': 'shin.R',
    '27': 'foot.L', # should be an ankle
    '28': 'foot.R',
    '29': 'heel.02.L',
    '30': 'heel.02.R',
    '31': 'toe.L',
    '32': 'toe.R'
}

# Simple skeleton NO rig
mapping = {
    #'2': 'CC_Base_L_Eye',
    #'5': 'CC_Base_R_Eye',
    'leftUpperArm': 'upper_arm.L',
    'rightUpperArm': 'upper_arm.R',
    'leftLowerArm': 'forearm.L',
    'rightLowerArm': 'forearm.R',
    'leftHand': 'hand.L',
    'rightHand': 'hand.R',
    #'17': 'f_pinky.01.L',
    #'18': 'f_pinky.01.R',
    #'19': 'f_index.01.L',
    #'20': 'f_index.01.L',
    #'21': 'thumb.01.L',
    #'22': 'thumb.01.L',
    'leftUpperLeg': 'thigh.L', # maybe pelvis.L
    'rightUpperLeg': 'thigh.R', # maybe pelvis.R
    'leftLowerLeg': 'shin.L',
    'rightLowerLeg': 'shin.R',
    #'27': 'foot.L', # should be an ankle
    #'28': 'foot.R',
    #'29': 'heel.02.L',
    #'30': 'heel.02.R',
    #'31': 'toe.L',
    #'32': 'toe.R'
}


class ScriptThread (threading.Thread):
    def __init__(self, threadID, name, mapping):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.mapping = mapping
        self.landmarks_file = '/Users/marco/Documents/Computer Vision/landmarks.json'
        self.landmarks_file = '/Users/marco/Documents/Computer Vision/PE2R/landmarks_js.json'
        
        self.man = bpy.data.objects['man3']

        # Enter pose mode
        bpy.ops.object.mode_set(mode='POSE')

        # Get the bones
        self.bones = self.man.pose.bones
        self.initial_position = {}

        # Get the finger
        #self.finger = self.man.pose.bones['CC_Base_R_Thumb3']

    def load_landmarks(self, file_name):
        with open(file_name) as file:
            landmarks = json.load(file)
            return landmarks

    def run(self):
        landmarks = self.load_landmarks(self.landmarks_file)
        print('File loaded!')
        
        print('Saving initial locations...')
        for source_coordinate in self.mapping:
            self.initial_position[self.mapping[source_coordinate]] = self.bones[self.mapping[source_coordinate]].location.copy()
        
        FPS = 30
        is_running = True

        tick = time.time()
        max_loops = len(landmarks)
        #max_loops = 200
        loop = 0
        alpha = 50
        while is_running is True:
            if time.time() >= tick+(1/FPS):
                tick = time.time()
                
                print(f'\033[2;31;43m Frame: {loop} \033[0;0m')
                #self.finger.location = (self.finger.location[0] + 0.1, self.finger.location[1], self.finger.location[2])
                #bpy.context.scene.cursor.location = finger.location
                #bpy.ops.transform.rotate(value=radians(self.finger.rotation_euler[0] + 0.5), orient_axis='X')
                
                for source_coordinate in self.mapping:
                    # Coordinates
                    coordinates = landmarks[f'frame_{loop}']['coordinates']
                    #self.bones[self.mapping[source_coordinate]].location = (
                    #    coordinates[source_coordinate]['x'] * alpha,
                    #    coordinates[source_coordinate]['z'] * alpha,
                    #    coordinates[source_coordinate]['y'] * alpha
                    #)
                    
                    # Rotations
                    angles = landmarks[f'frame_{loop}']['angles']
                    #self.bones[self.mapping[source_coordinate]].rotation_mode = 'XYZ'
                    #self.bones[self.mapping[source_coordinate]].rotation_euler = Euler((
                    #    radians(angles[source_coordinate]), radians(angles[source_coordinate]), radians(angles[source_coordinate])
                    #), 'XYZ')
                
                for angle in landmarks[f'frame_{loop}']['angles']:
                    print(f'Angle: {angle}')
                    #joints = angle[1:-1].split(', ')
                    angles = landmarks[f'frame_{loop}']['angles'][angle]
                    print(f'Angles: {angles}')
                    
                    #print(f"Setting bone {self.mapping[f'{joints[1]}']} to {(angles[0]), (angles[1]), (angles[2])}")
                    joints = [angle, angle, angle]
                    
                    if joints[1] not in self.mapping:
                        continue
                    
                    self.bones[self.mapping[f'{joints[1]}']].rotation_mode = 'XYZ'
                    self.bones[self.mapping[f'{joints[1]}']].rotation_euler = Euler((
                        #radians(angles[0]), radians(angles[1]), radians(angles[2])
                        angles['x'], angles['y'], angles['z']
                    ), 'XYZ')
                    #self.bones[self.mapping[f'{joints[1]}']].rotation_mode = 'QUATERNION'
                    #self.bones[self.mapping[f'{joints[1]}']].rotation_quaternion = [angles['x'], angles['y'], angles['z'], angles['w']]
                
                time.sleep(1/FPS)
                loop += 1
                if loop >= max_loops:
                    is_running = False
            else:
                continue
            
        # End of update, restore initial positions after 5 seconds
        print('Restoring initial positions in 5 seconds!')
        time.sleep(5)
        for coordinate in self.initial_position:
            self.bones[coordinate].location = self.initial_position[coordinate]
        print('Initial positions restored!')

#Make thread
thread = ScriptThread(1, "thread", mapping)
thread.start()
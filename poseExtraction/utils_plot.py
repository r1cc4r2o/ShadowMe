import matplotlib.pyplot as plt 
import glob
from PIL import Image

class PlotGenerator():
    """
       This class provide a set of function to produce the 
        plots. 
        
            plot3dFrame:          plot in 3d the landmarks of all the 
                                  frames calling 'plot_world_landmarks'
                                  
            generateGIF:          generate the GIF
            
            
    """
    def __init__(self) -> None:
        pass

    def plot3dFrames(self, dictionary: dict):
        # list of the keys with all the coords of the landmarks
        keyCoord = [i for i in list(dictionary.keys()) if i[0] in 'c' ]
        # produce a list of landmarks ordered from frame_0 to frame_n
        landmarks = [dictionary[i] for i in keyCoord]
        # run the function to produce the frame and store them
        # in the folder frame
        self.plot_world_landmarks(landmarks, visibility_th=0.5)
        
    def generateGIF(self, path: str = 'frame/', duration: int = 50 ) -> None:
        images = sorted(glob.glob(f'./'+path+'*'))
        gif = []
        # append the images in a list
        [gif.append(Image.open(im)) for im in images]
        # generate the GIF
        gif[0].save('./poseExtraction/GIF.gif', save_all=True, append_images=gif[1:], optimize=False, duration=duration, loop=0)

    def plot_world_landmarks(
        self,
        landmark: list,
        visibility_th: float = 0.5,
        ) -> None:
        """ source: https://github.com/Kazuhito00/mediapipe-python-sample/blob/main/sample_pose.py

            This function has been a little bit modified by me. Specifically,
            given the list of the landmark produce a pic of the skeleton in the 
            scene and store in a specific folder all the generated frame.

                Input:
                    landmark: list of landmarks

                Output:
                    store the 3D pic of the scene in
                    the frame folder.
        """
        frame = 0
        for landmarks in landmark:
            #fig = plt.figure(figsize=(16, 16), dpi=400)
            fig = plt.figure(figsize=(16, 16))
            ax = fig.add_subplot(1, 1, 1, projection='3d')
            landmark_point = []

            for index, landmark in enumerate(landmarks.landmark):
                landmark_point.append(
                    [landmark.visibility, (landmark.x, landmark.y, landmark.z)])

            face_index_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            right_arm_index_list = [11, 13, 15, 17, 19, 21]
            left_arm_index_list = [12, 14, 16, 18, 20, 22]
            right_body_side_index_list = [11, 23, 25, 27, 29, 31]
            left_body_side_index_list = [12, 24, 26, 28, 30, 32]
            shoulder_index_list = [11, 12]
            waist_index_list = [23, 24]

            # 顔
            face_x, face_y, face_z = [], [], []
            for index in face_index_list:
                point = landmark_point[index][1]
                face_x.append(point[0])
                face_y.append(point[2])
                face_z.append(point[1] * (-1))

            # 右腕
            right_arm_x, right_arm_y, right_arm_z = [], [], []
            for index in right_arm_index_list:
                point = landmark_point[index][1]
                right_arm_x.append(point[0])
                right_arm_y.append(point[2])
                right_arm_z.append(point[1] * (-1))

            # 左腕
            left_arm_x, left_arm_y, left_arm_z = [], [], []
            for index in left_arm_index_list:
                point = landmark_point[index][1]
                left_arm_x.append(point[0])
                left_arm_y.append(point[2])
                left_arm_z.append(point[1] * (-1))

            # 右半身
            right_body_side_x, right_body_side_y, right_body_side_z = [], [], []
            for index in right_body_side_index_list:
                point = landmark_point[index][1]
                right_body_side_x.append(point[0])
                right_body_side_y.append(point[2])
                right_body_side_z.append(point[1] * (-1))

            # 左半身
            left_body_side_x, left_body_side_y, left_body_side_z = [], [], []
            for index in left_body_side_index_list:
                point = landmark_point[index][1]
                left_body_side_x.append(point[0])
                left_body_side_y.append(point[2])
                left_body_side_z.append(point[1] * (-1))

            # 肩
            shoulder_x, shoulder_y, shoulder_z = [], [], []
            for index in shoulder_index_list:
                point = landmark_point[index][1]
                shoulder_x.append(point[0])
                shoulder_y.append(point[2])
                shoulder_z.append(point[1] * (-1))

            # 腰
            waist_x, waist_y, waist_z = [], [], []
            for index in waist_index_list:
                point = landmark_point[index][1]
                waist_x.append(point[0])
                waist_y.append(point[2])
                waist_z.append(point[1] * (-1))
                    
            ax.cla()
            ax.set_xlim3d(-1, 1)
            ax.set_ylim3d(-1, 1)
            ax.set_zlim3d(-1, 1)

            ax.scatter(face_x, face_y, face_z)
            ax.plot(right_arm_x, right_arm_y, right_arm_z)
            ax.plot(left_arm_x, left_arm_y, left_arm_z)
            ax.plot(right_body_side_x, right_body_side_y, right_body_side_z)
            ax.plot(left_body_side_x, left_body_side_y, left_body_side_z)
            ax.plot(shoulder_x, shoulder_y, shoulder_z)
            ax.plot(waist_x, waist_y, waist_z)
            

            if frame<=9:
                plt.savefig(f'./frame/00{frame}.png')
            elif frame<=99:
                plt.savefig(f'./frame/0{frame}.png')
            else:
                plt.savefig(f'./frame/{frame}.png')
            
            frame = frame + 1

        return
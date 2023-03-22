import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Define a function to calculate the angle between three points
'''
def calculate_angle(a,b,c):
  a = np.array(a) 
  b = np.array(b) 
  c = np.array(c) 
  
  radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
  angle = np.abs(radians*180.0/np.pi)
  
  if angle >180.0:
    angle = 360-angle
    
  return angle
'''

def calculate_angle(a,b,c):
  a = np.array(a) 
  b = np.array(b) 
  c = np.array(c) 
  
  radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
  angle = np.abs(radians*180.0/np.pi)
  
  if angle >180.0:
    angle = 360-angle
    
  return angle


# Create a video capture object
cap = cv2.VideoCapture('/Users/riccardotedoldi/Desktop/ais/I/sem2/cv/project/PoseEstimationTo3Drender/poseExtraction/data/test2.mp4')

# Initialize the pose model
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
  
  while cap.isOpened():
    ret, frame = cap.read()
    
    # Recolor the image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Make detection
    results = pose.process(image)
    
    # Recolor back to BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    try:
      # Extract landmarks
      landmarks = results.pose_world_landmarks.landmark
      
      # Get coordinates of the right leg and waist landmarks 
      right_hip_x, right_hip_y = int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x * image.shape[1]), int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * image.shape[0])
      right_knee_x, right_knee_y = int(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x * image.shape[1]), int(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y * image.shape[0])
      right_ankle_x, right_ankle_y = int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * image.shape[1]), int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * image.shape[0])

      # Get coordinates of the left leg and waist landmarks 
      left_hip_x, left_hip_y = int(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * image.shape[1]), int(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * image.shape[0])
      left_knee_x, left_knee_y = int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * image.shape[1]), int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * image.shape[0])
      left_ankle_x, left_ankle_y = int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * image.shape[1]), int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * image.shape[0])
      
      right_shoulder_x, right_shoulder_y = int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * image.shape[1]), int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * image.shape[0])
      left_shoulder_x, left_shoulder_y = int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * image.shape[1]), int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * image.shape[0])
      
      # Calculate the angles
      angle_right_leg_waist = calculate_angle((right_hip_x,right_hip_y), (right_knee_x,right_knee_y), (right_shoulder_x,right_shoulder_y))
      angle_left_leg_waist = calculate_angle((left_hip_x,left_hip_y), (left_knee_x,left_knee_y), (left_shoulder_x,left_shoulder_y))
      
      # Visualize the angles
      cv2.putText(image, str(angle_right_leg_waist), 
                   tuple(np.multiply((right_knee_x,right_knee_y), 1).astype(int)), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
      
      cv2.putText(image, str(angle_left_leg_waist), 
                   tuple(np.multiply((left_knee_x,left_knee_y), 1).astype(int)), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
      
    except:
      pass
    
    # Render detections
    mp_drawing.draw_landmarks(image,
                              results.pose_landmarks,
                              mp_pose.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(245 ,117 ,66 ), thickness=2),
                              mp_drawing.DrawingSpec(color=(245 ,66 ,230 ), thickness=2))
    
    cv2.imshow('Mediapipe Feed', image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
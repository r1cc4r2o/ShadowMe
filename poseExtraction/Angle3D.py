import numpy as np

class Angle():
    """
    The three planes formed by unit vectors i, j, k.
    Assuming the coordinates order is x, y, z.
    """
    _xy = np.array([1, 1, 0]) # No z
    _xz = np.array([1, 0, 1]) # No y
    _yz = np.array([0, 1, 1]) # No x

    def __init__(self, point_a, point_b, point_c):
        self.point_a = point_a
        self.point_b = point_b
        self.point_c = point_c
        # self.vector_ab = Angle.unit_vector(point_a - point_b)
        # self.vector_bc = Angle.unit_vector(point_c - point_b)

    @staticmethod
    def unit_vector(vector):
        return vector / np.linalg.norm(vector)
    
    def computeAngle(self, plane):
        point_a = self.point_a * plane
        point_b = self.point_b * plane
        point_c = self.point_c * plane

        # Compute the angle
        radians = np.arctan2(point_c[1] - point_b[1], point_c[0] - point_b[0]) - np.arctan2(point_a[1] - point_b[1], point_a[0] - point_b[0])
        angle = np.rad2deg(radians)

        if angle > 180.0:
            angle = 360 - angle
        
        return angle

    def compute(self):
        """
        To get the rotation along axis x, the vector has to be
        projected onto plane yz first. Analogous for y and z.
        """
        angle_x = self.computeAngle(self._yz)
        angle_y = self.computeAngle(self._xz)
        angle_z = self.computeAngle(self._xy)

        return (angle_x, angle_y, angle_z)
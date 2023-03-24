import numpy as np

class Angle():
    """
    The three planes formed by unit vectors i, j, k.
    Assuming the coordinates order is x, y, z.
    """
    _xy = np.array([1, 1, 0]) # No z
    _xz = np.array([1, 0, 1]) # No y
    _yz = np.array([0, 1, 1]) # No x

    def __init__(self, point_a, point_b):
        self.point_a = point_a
        self.point_b = point_b
        #self.point_c = point_c
        # self.vector_ab = Angle.unit_vector(point_a - point_b)
        # self.vector_bc = Angle.unit_vector(point_c - point_b)

    @staticmethod
    def unit_vector(vector):
        return vector / np.linalg.norm(vector)
    """
    def computeAngle(self, plane):
        point_a = self.point_a * plane
        point_b = self.point_b * plane
        point_c = self.point_c * plane

        # Compute the angle
        radians = np.arctan2(point_c[1] - point_b[1], point_c[0] - point_b[0]) - np.arctan2(point_a[1] - point_b[1], point_a[0] - point_b[0])
        angle = np.rad2deg(radians)

        angle = abs(angle)
        if angle > 180.0:
            angle = 360 - angle
        # return angle % 180.0
        
        return angle
    """
    
    def computeAngle(self, plane):
        # point_a = self.point_a * plane
        # point_b = self.point_b * plane
        # point_c = self.point_c * plane

        # Compute the angle of 2D vectors
        
        # source: https://stackoverflow.com/questions/1211212/how-to-calculate-an-angle-from-three-points
        #                     result = atan2(P3.y - P1.y, P3.x - P1.x) - atan2(P2.y - P1.y, P2.x - P1.x);
        # radians = np.arctan2(point_c[1] - point_b[1], point_c[0] - point_b[0]) - np.arctan2(point_a[1] - point_b[1], point_a[0] - point_b[0])
        # angle = np.rad2deg(radians)
        
        point_a = self.point_a * plane
        point_b = self.point_b * plane
        
        # source: https://stackoverflow.com/questions/1211212/how-to-calculate-an-angle-from-three-points
        # a•b = (ax bx, ay by, az bz)
        a_dot_b = np.array([Va*Vb for Va, Vb in zip(point_a, point_b)]).sum()
        # |ab|•|bc|
        norm_a_dot_b = np.sqrt(np.array([Va**2 for Va in point_a]).sum()) * np.sqrt(np.array([Vb**2 for Vb in point_b]).sum()) 
        # angle = arccos(ab•bc / |ab|•|bc|)
        angle = np.rad2deg(np.arccos(a_dot_b/norm_a_dot_b))

        angle = abs(angle)
        if angle > 180.0:
            angle = 360 - angle
        return angle
        # return angle % 360.0
        
    
    def compute(self):
        """
        To get the rotation along axis x, the vector has to be
        projected onto plane yz first. Analogous for y and z.
        """
        angle_x = self.computeAngle(self._yz)
        angle_y = self.computeAngle(self._xz)
        angle_z = self.computeAngle(self._xy)

        return (angle_x, angle_y, angle_z)
    
    
class AnglePlane3D():
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
    """
    def computeAngle(self, plane):
        point_a = self.point_a * plane
        point_b = self.point_b * plane
        point_c = self.point_c * plane

        # Compute the angle
        radians = np.arctan2(point_c[1] - point_b[1], point_c[0] - point_b[0]) - np.arctan2(point_a[1] - point_b[1], point_a[0] - point_b[0])
        angle = np.rad2deg(radians)

        angle = abs(angle)
        if angle > 180.0:
            angle = 360 - angle
        # return angle % 180.0
        
        return angle
    """
    
    def computeAngle(self, plane):
        # point_a = self.point_a * plane
        # point_b = self.point_b * plane
        # point_c = self.point_c * plane

        # Compute the angle of 2D vectors
        
        # source: https://stackoverflow.com/questions/1211212/how-to-calculate-an-angle-from-three-points
        #                     result = atan2(P3.y - P1.y, P3.x - P1.x) - atan2(P2.y - P1.y, P2.x - P1.x);
        # radians = np.arctan2(point_c[1] - point_b[1], point_c[0] - point_b[0]) - np.arctan2(point_a[1] - point_b[1], point_a[0] - point_b[0])
        # angle = np.rad2deg(radians)
        
        point_a = self.point_a * plane
        point_b = self.point_b * plane
        point_c = self.point_c * plane
        
        # source: https://stackoverflow.com/questions/1211212/how-to-calculate-an-angle-from-three-points
        # a•b = (ax bx, ay by, az bz)
        a_dot_b = [Va-Vb for Va, Vb in zip(point_a, point_b)]
        # b•c = (bx cx,  by cy,  bz cz)
        b_dot_c = [Vb-Vc for Vb, Vc in zip(point_b, point_c)]
        # ab•bc = abx*bcx + aby*bcy + abz*bcz 
        ab_dot_bc = np.array([ab*bc for ab, bc in zip(a_dot_b, b_dot_c)]).sum()
        # |ab|•|bc|
        norm_a_dot_b = np.sqrt(np.array([Vab**2 for Vab in a_dot_b]).sum()) * np.sqrt(np.array([Vbc**2 for Vbc in b_dot_c]).sum()) 
        # angle = arccos(ab•bc / |ab|•|bc|)
        angle = np.rad2deg(np.arccos(ab_dot_bc/norm_a_dot_b))

        angle = abs(angle)
        if angle > 180.0:
            angle = 360 - angle
        return angle
        # return angle % 360.0
        
    
    def compute(self):
        """
        To get the rotation along axis x, the vector has to be
        projected onto plane yz first. Analogous for y and z.
        """
        angle_x = self.computeAngle(self._yz)
        angle_y = self.computeAngle(self._xz)
        angle_z = self.computeAngle(self._xy)

        return (angle_x, angle_y, angle_z)
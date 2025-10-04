import math
import numpy as np
from typing import Generator
class HeartController:
    def debug_points(self):
        yield np.array([1, 1])
        yield np.array([-1, 1])
        yield np.array([-1, -1])
        yield np.array([1, -1])
    
    def generate_points(self) -> Generator[np.ndarray, None, None] : 
        center = np.array([0, 0])
        yield center
        len = 3
        v_angle = math.pi / 4.5
        step = 30

        v_right = np.array([len * math.sin(v_angle), len * math.cos(v_angle)])
        yield v_right        
        
        r = len * math.sin(v_angle) * 0.5
        height = len * math.cos(v_angle)
        r_center = np.array([r, height]) 
        l_center = np.array([-r, height])

        for angle in range(0, 180, step):
            rad = math.radians(angle)
            yield r_center + np.array([r * math.cos(rad), r * math.sin(rad)])
        
        for angle in range(0, 180, step):
            rad = math.radians(angle)
            yield l_center + np.array([r * math.cos(rad), r * math.sin(rad)])

        v_left = np.array([-len * math.sin(v_angle), len * math.cos(v_angle)])
        yield v_left 
        yield center
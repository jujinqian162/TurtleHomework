import math
from typing import Iterable, Iterator, Tuple, Union
import numpy as np
Point2D = np.ndarray
Number = Union[int, float]

class PointsTransformer: # AI generate !
    """
    可迭代的点转换器（2D）。接受一个 points_iter（任何可迭代/生成器，元素为 (x,y)）和角度，
    每次迭代 yield 旋转后的 (x', y')。
    
    参数:
    - points_iter: Iterable[Point2D] | Iterator[Point2D]，点来源（会被惰性消费）
    - angle: 旋转角度（数值）
    - degrees: True 表示 angle 以度为单位；False 表示以弧度为单位
    - origin: 旋转中心 (ox, oy)，默认 (0,0)
    """
    def __init__(self,
                 points_iter: Iterable[Point2D],
                 angle: Number,
                 degrees: bool = True,
                 origin: Point2D = np.array([0.0, 0.0])):
        self._it = iter(points_iter)
        if degrees:
            angle = math.radians(angle)
        self._cos = math.cos(angle)
        self._sin = math.sin(angle)
        self._origin = (float(origin[0]), float(origin[1]))

    def __iter__(self) -> "PointsTransformer":
        return self

    def __next__(self) -> Point2D:
        x, y = next(self._it)  # 可能抛 StopIteration，遵循迭代器协议
        ox, oy = self._origin
        # 平移到原点，旋转，再平移回去
        xr = x - ox
        yr = y - oy
        x2 = xr * self._cos - yr * self._sin + ox
        y2 = xr * self._sin + yr * self._cos + oy
        return np.array([x2, y2])

def transform_points(points_iter: Iterable[Point2D],
                     angle: Number,
                     degrees: bool = True,
                     origin: Point2D = np.array([0.0, 0.0])) -> Iterator[Point2D]:
    """
    生成器版本：对 points_iter 中的每个点 yield 旋转后的坐标。
    """
    if degrees:
        angle = math.radians(angle)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    ox, oy = float(origin[0]), float(origin[1])

    for x, y in points_iter:
        xr = x - ox
        yr = y - oy
        x2 = xr * cos_a - yr * sin_a + ox
        y2 = xr * sin_a + yr * cos_a + oy
        yield np.array([x2, y2])

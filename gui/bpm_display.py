from typing import List

import numpy as np


class BPMsDisplay:
    name: List[str] = ["DT11", "DT12", "DT13"]
    x_center: np.ndarray = np.array([660, 872, 1140])  # pixels
    y_center: np.ndarray = np.array([510, 211, 97])
    angle: np.ndarray = np.array([0.8, 0.8, 0.2])  # rads
    scale: float = 0.05

    @classmethod
    def get_absolute_pos(cls, y_coords: List[float]):
        y_coords = np.array(y_coords)
        x = cls.x_center * cls.scale - y_coords * np.sin(cls.angle)
        y = cls.y_center * cls.scale - y_coords * np.cos(cls.angle)
        return x, y

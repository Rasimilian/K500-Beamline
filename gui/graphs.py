from typing import List

import numpy as np
import pyqtgraph as pg
from PIL import Image

from PyQt5.QtGui import QTransform

from gui.bpm_display import BPMsDisplay


class Graphs:
    def __init__(self, bpms: List[str]):
        colors = ['r', 'b', 'g', 'k']
        self.x_orbit_plot = pg.PlotDataItem(symbol='o', symbolSize=7, symbolBrush='r', name='X', pen=pg.mkPen(color='r', width=2))
        self.y_orbit_plot = pg.PlotDataItem(symbol='o', symbolSize=7, symbolBrush='b', name='Y', pen=pg.mkPen(color='b', width=2))
        self.i_plot = pg.PlotDataItem(symbol='o', symbolSize=7, symbolBrush='r', name='I', pen=pg.mkPen(color='r', width=2))
        self.i_vs_x_plots = {bpm: pg.PlotDataItem(symbol='o', symbolSize=7, symbolBrush=colors[idx], name=bpm, pen=None) for idx, bpm in enumerate(bpms)}
        self.i_vs_y_plots = {bpm: pg.PlotDataItem(symbol='o', symbolSize=7, symbolBrush=colors[idx], name=bpm, pen=None) for idx, bpm in enumerate(bpms)}

        tr = QTransform()
        tr.scale(BPMsDisplay.scale, BPMsDisplay.scale)
        self.img = Image.open("gui/resources/k500_structure.jpg")
        img_to_array = np.asarray(self.img)
        self.img = pg.ImageItem(image=img_to_array, axisOrder='row-major')
        self.img.setTransform(tr)
        self.plot_orbit_beamline = pg.PlotDataItem(symbol='o', symbolSize=8, symbolBrush='r', name='Orbit Y', pen=pg.mkPen(color='r', width=5))

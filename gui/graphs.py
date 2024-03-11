from typing import List

import numpy as np
import pyqtgraph as pg
from PIL import Image

from PyQt5.QtGui import QTransform
from PyQt5.QtCore import Qt

from beam_control.beam_passing import BeamStats
from gui.bpm_display import BPMsDisplay

pg.setConfigOptions(antialias=True)


class Graphs:
    def __init__(self, bpms: List[str]):
        markers = ["o", "x", "s", "t"]
        self.x_orbit_plot = pg.PlotDataItem(symbol='o', symbolSize=7, symbolBrush='r', name='X', pen=pg.mkPen(color='r', width=2))
        self.y_orbit_plot = pg.PlotDataItem(symbol='o', symbolSize=7, symbolBrush='b', name='Y', pen=pg.mkPen(color='b', width=2))
        self.i_plot = pg.PlotDataItem(symbol='o', symbolSize=7, symbolBrush='r', name='I', pen=pg.mkPen(color='r', width=2))
        self.i_vs_xy_plots = {bpm: pg.ScatterPlotItem(pxMode=False, symbol=markers[idx], name=bpm) for idx, bpm in enumerate(bpms)}
        for plot in self.i_vs_xy_plots.values():
            plot.setOpacity(0.3)
        self._colormap = pg.colormap.get('copper_r', source='matplotlib')

        tr = QTransform()
        tr.scale(BPMsDisplay.scale, BPMsDisplay.scale)
        self.img = Image.open("gui/resources/k500_structure.jpg")
        img_to_array = np.asarray(self.img)
        self.img = pg.ImageItem(image=img_to_array, axisOrder='row-major')
        self.img.setTransform(tr)
        self.plot_orbit_beamline = pg.PlotDataItem(symbol='o', symbolSize=8, symbolBrush='r', name='Orbit Y', pen=pg.mkPen(color='r', width=5))

    def set_data(self, beam_stats: BeamStats):
        x = []
        y = []
        i = []
        for bpm, data in beam_stats.history.items():
            x.append(data[bpm].x[-1])
            y.append(data[bpm].y[-1])
            i.append(data[bpm].i[-1])
            points = []
            x_all = np.array(data[bpm].x)
            y_all = np.array(data[bpm].y)
            i_all = np.array(data[bpm].i)
            i_all_scaled_sorted_index = np.argsort((i_all - i_all.min()) / np.ptp(i_all))
            colors = self._colormap.getLookupTable(0, 1, nPts=i_all.size, alpha=True)
            for idx in range(len(i_all)):
                points.append({'pos': (x_all[i_all_scaled_sorted_index[idx]], y_all[i_all_scaled_sorted_index[idx]]),
                               'size': 0.1,
                               'pen': {'color': 'k', 'width': 1},
                               'brush': colors[idx]})
                if i_all.argmax() == idx:
                    points.append({'pos': (x_all[idx], y_all[idx]),
                                   'size': 0.7,
                                   'symbol': 's',
                                   'pen': {'color': 'k', 'width': 2, 'style': Qt.DashLine},
                                   'brush': 'w'})
            self.i_vs_xy_plots[bpm].addPoints(points)
        self.x_orbit_plot.setData(x)
        self.y_orbit_plot.setData(y)
        self.i_plot.setData(i)
        x_beamline, y_beamline = BPMsDisplay.get_absolute_pos(y[:-1])
        self.plot_orbit_beamline.setData(x_beamline, y_beamline)

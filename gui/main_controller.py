import numpy as np
from PIL import Image
import pyqtgraph as pg

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QTransform

from beam_passing import BeamStats
import gui.gui_designs.main as design
from gui.bpm_display import BPMsDisplay


class Application(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('K500')
        self.initUI()

    def initUI(self):
        self.beam_stats = BeamStats()

        self.pushButton.clicked.connect(self.connect)
        self.pushButton_2.clicked.connect(self.save_history)

        styles = {'color': 'k', 'font-size': '20px'}
        self.graphicsView.setBackground('w')
        self.graphicsView.addLegend()
        self.graphicsView.getPlotItem().setLabel('left', "Position [mm]", **styles)
        self.graphicsView.getPlotItem().setLabel('bottom', 'BPM index', **styles)
        self.graphicsView_2.setBackground('w')
        self.graphicsView_2.addLegend()
        self.graphicsView_2.getPlotItem().setLabel('left', "Current History [mA]", **styles)
        self.graphicsView_2.getPlotItem().setLabel('bottom', 'X Position History [mm]', **styles)
        self.graphicsView_3.setBackground('w')
        self.graphicsView_3.addLegend()
        self.graphicsView_3.getPlotItem().setLabel('left', "Current [mA]", **styles)
        self.graphicsView_3.getPlotItem().setLabel('bottom', "BPM index", **styles)
        self.graphicsView_4.setBackground('w')
        self.graphicsView_4.addLegend()
        self.graphicsView_4.getPlotItem().setLabel('left', "Current History [mA]", **styles)
        self.graphicsView_4.getPlotItem().setLabel('bottom', "Y Position History [mm]", **styles)
        pen = pg.mkPen(color='r', width=2)
        pen1 = pg.mkPen(color='b', width=2)
        colors = ['r', 'b', 'g', 'k']
        self.x_orbit_plot = pg.PlotDataItem(symbol='o', symbolSize=7, symbolBrush='r', name='X', pen=pen)
        self.y_orbit_plot = pg.PlotDataItem(symbol='o', symbolSize=7, symbolBrush='b', name='Y', pen=pen1)
        self.i_plot = pg.PlotDataItem(symbol='o', symbolSize=7, symbolBrush='r', name='I', pen=pen)
        self.i_vs_x_plots = {bpm: pg.PlotDataItem(symbol='o', symbolSize=7, symbolBrush=colors[idx], name=bpm, pen=None) for idx, bpm in enumerate(self.beam_stats.BPMS)}
        self.i_vs_y_plots = {bpm: pg.PlotDataItem(symbol='o', symbolSize=7, symbolBrush=colors[idx], name=bpm, pen=None) for idx, bpm in enumerate(self.beam_stats.BPMS)}
        self.graphicsView.addItem(self.x_orbit_plot)
        self.graphicsView.addItem(self.y_orbit_plot)
        self.graphicsView_3.addItem(self.i_plot)
        for plot in self.i_vs_x_plots.values():
            self.graphicsView_2.addItem(plot)
        for plot in self.i_vs_y_plots.values():
            self.graphicsView_4.addItem(plot)

        self.graphicsView_17.setBackground('w')
        self.graphicsView_17.addLegend()
        self.graphicsView_17.invertY(True)
        tr = QTransform()
        tr.scale(BPMsDisplay.scale, BPMsDisplay.scale)
        img = Image.open("gui/resources/k500_structure.jpg")
        img_to_array = np.asarray(img)
        img = pg.ImageItem(image=img_to_array, axisOrder='row-major')
        img.setTransform(tr)
        pen = pg.mkPen(color='r', width=5)
        self.plot_orbit_beamline = pg.PlotDataItem(symbol='o', symbolSize=8, symbolBrush='r', name='Orbit Y', pen=pen)
        self.graphicsView_17.addItem(img)
        self.graphicsView_17.addItem(self.plot_orbit_beamline)

    @pyqtSlot()
    def save_history(self):
        comment = self.plainTextEdit_13.toPlainText()
        if comment: comment = "_" + comment
        self.beam_stats.save_data(comment)

    @pyqtSlot()
    def connect(self):
        self.beam_stats.connect()
        self.beam_stats.pvs[self.beam_stats.bpm_for_callback].x.add_callback(self.add_plot_callback)

    def add_plot_callback(self, pvname=None, value=None, char_value=None, **kw):
        x = []
        y = []
        i = []
        for bpm, data in self.beam_stats.history.items():
            x.append(data.x[-1])
            y.append(data.y[-1])
            i.append(data.i[-1])
            self.i_vs_x_plots[bpm].setData(data.x, data.i)
            self.i_vs_y_plots[bpm].setData(data.y, data.i)
        self.x_orbit_plot.setData(x)
        self.y_orbit_plot.setData(y)
        self.i_plot.setData(i)
        x_beamline, y_beamline = BPMsDisplay.get_absolute_pos(y[:-1])
        self.plot_orbit_beamline.setData(x_beamline, y_beamline)

        if self.pushButton_7.isChecked():
            best_idx = self.beam_stats.history["1P7"].best_shot_num
        elif self.pushButton_6.isChecked():
            best_idx = self.beam_stats.history["DT13"].best_shot_num
        elif self.pushButton_5.isChecked():
            best_idx = self.beam_stats.history["DT12"].best_shot_num
        elif self.pushButton_4.isChecked():
            best_idx = self.beam_stats.history["DT11"].best_shot_num
        self.plainTextEdit.setPlainText(str(self.beam_stats.history["DT11"].x[best_idx]))
        self.plainTextEdit_4.setPlainText(str(self.beam_stats.history["DT11"].y[best_idx]))
        self.plainTextEdit_9.setPlainText(str(self.beam_stats.history["DT11"].i[best_idx]))
        self.plainTextEdit_2.setPlainText(str(self.beam_stats.history["DT12"].x[best_idx]))
        self.plainTextEdit_5.setPlainText(str(self.beam_stats.history["DT12"].y[best_idx]))
        self.plainTextEdit_8.setPlainText(str(self.beam_stats.history["DT12"].i[best_idx]))
        self.plainTextEdit_3.setPlainText(str(self.beam_stats.history["DT13"].x[best_idx]))
        self.plainTextEdit_6.setPlainText(str(self.beam_stats.history["DT13"].y[best_idx]))
        self.plainTextEdit_7.setPlainText(str(self.beam_stats.history["DT13"].i[best_idx]))
        self.plainTextEdit_10.setPlainText(str(self.beam_stats.history["1P7"].x[best_idx]))
        self.plainTextEdit_11.setPlainText(str(self.beam_stats.history["1P7"].y[best_idx]))
        self.plainTextEdit_12.setPlainText(str(self.beam_stats.history["1P7"].i[best_idx]))

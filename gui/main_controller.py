from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot

from beam_control.beam_passing import BeamStats

import gui.qt_designs.main as design
from gui.graphs import Graphs


class Application(QtWidgets.QMainWindow, design.Ui_MainWindow):
    beam_stats: BeamStats
    graphs: Graphs

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('K500')
        self.initUI()

    def initUI(self):
        self.beam_stats = BeamStats()
        self.graphs = Graphs(self.beam_stats.bpms)

        self.pushButton.clicked.connect(self.connect)
        self.pushButton_2.clicked.connect(self.save_history)

        styles = {'color': 'k', 'font-size': '20px'}
        self.graphicsView.setBackground('w')
        self.graphicsView.addLegend()
        self.graphicsView.getPlotItem().setLabel('left', "Position [mm]", **styles)
        self.graphicsView.getPlotItem().setLabel('bottom', 'BPM index', **styles)
        self.graphicsView_2.setBackground('w')
        self.graphicsView_2.addLegend()
        self.graphicsView_2.getPlotItem().setLabel('left', "Current [mA]", **styles)
        self.graphicsView_2.getPlotItem().setLabel('bottom', "BPM index", **styles)
        self.graphicsView_3.setBackground('w')
        self.graphicsView_3.addLegend()
        self.graphicsView_3.getPlotItem().setLabel('left', "Y Position History [mm]", **styles)
        self.graphicsView_3.getPlotItem().setLabel('bottom', "X Position History [mm]", **styles)

        self.graphicsView.addItem(self.graphs.x_orbit_plot)
        self.graphicsView.addItem(self.graphs.y_orbit_plot)
        self.graphicsView_2.addItem(self.graphs.i_plot)
        for plot in self.graphs.i_vs_xy_plots.values():
            self.graphicsView_3.addItem(plot)

        self.graphicsView_17.setBackground('w')
        self.graphicsView_17.addLegend()
        self.graphicsView_17.invertY(True)
        self.graphicsView_17.addItem(self.graphs.img)
        self.graphicsView_17.addItem(self.graphs.plot_orbit_beamline)

    @pyqtSlot()
    def save_history(self):
        comment = self.plainTextEdit_13.toPlainText()
        if comment: comment = "_" + comment
        self.beam_stats.save_data(comment)

    @pyqtSlot()
    def connect(self):
        self.beam_stats.connect()
        self.beam_stats.pvs[self.beam_stats.bpm_for_callback].x.add_callback(self.add_plot_callback)
        self.pushButton.setEnabled(False)

    def add_plot_callback(self):
        self.graphs.set_data(self.beam_stats)

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

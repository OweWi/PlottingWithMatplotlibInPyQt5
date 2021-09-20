import sys
import random
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# Figure Widget
class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        layout = QtWidgets.QHBoxLayout()

        # Position widget
        self.position_plot = MplCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.position_plot)
        n_data = 50
        self.xdata_pp = list(range(n_data))
        self.ydata_pp = [0 for i in range(n_data)]
        self.update_position_plot()
        
        # Velocity widget
        self.velocity_plot = MplCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.velocity_plot)
        n_data = 50
        self.xdata_vp = list(range(n_data))
        self.ydata_vp = [0 for i in range(n_data)]
        self.update_velocity_plot()

        # Show main window
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(20)
        self.timer.timeout.connect(self.update_velocity_plot)
        self.timer.timeout.connect(self.update_position_plot)
        self.timer.start()

    def update_velocity_plot(self):
        # Drop off the first element, append a new one.
        self.ydata_vp = self.ydata_vp[1:] + [random.randint(0, 10)]
        self.velocity_plot.axes.cla()  # Clear the canvas.
        self.velocity_plot.axes.plot(self.xdata_vp, self.ydata_vp, 'r')
        # Axis labels must be set after the data is in the plot
        self.velocity_plot.axes.set_xlabel('Timestep')
        self.velocity_plot.axes.set_ylabel('Velocity')
        # Trigger the canvas to update and redraw.
        self.velocity_plot.draw()
    
    def update_position_plot(self):
        # Drop off the first element, append a new one.
        self.ydata_pp = self.ydata_pp[1:] + [random.randint(-5, 5)]
        self.position_plot.axes.cla()  # Clear the canvas.
        self.position_plot.axes.plot(self.xdata_pp, self.ydata_pp, 'r')
        # Axis labels must be set after the data is in the plot
        self.position_plot.axes.set_xlabel('Timestep')
        self.position_plot.axes.set_ylabel('Position')
        # Trigger the canvas to update and redraw.
        self.position_plot.draw()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
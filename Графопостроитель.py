import sys
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

global data_x
global data_y


class MplCanvas(FigureCanvasQTAgg):
        # создание фигуры в которой будет располагаться график
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        global fig
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def show_graph_build_dw(self):
        # сбор координат по икс
        text_x, pressed_x = QtWidgets.QInputDialog.getText(QtWidgets.QWidget(), "Graph builder",
                                                           "Введите координаты по X через пробел",
                                                           QtWidgets.QLineEdit.Normal, "")
        if pressed_x:
            # и по y 
            text_y, pressed_y = QtWidgets.QInputDialog.getText(QtWidgets.QWidget(), "Graph builder",
                                                               "Введите координаты по Y через пробел",
                                                               QtWidgets.QLineEdit.Normal, "")
            if pressed_y:
                data_x = list(map(float, text_x.split()))
                data_y = list(map(float, text_y.split()))
                # проверка на соотвествие длин списков
                if len(data_x) != len(data_y):
                    self.msg.showMessage('Кол-во чисел по X не соответствует кол-ву числе по Y')
                else:
                    # отрисовка нового графика
                    self.sc.axes.plot(data_x, data_y)
                    fig.canvas.draw()


    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle('Графопостроитель')
        # отрисовка графика по умолчанию
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.axes.plot(0, 0)
        self.msg = QtWidgets.QErrorMessage()
        # Создание кнопок управления графиком(тулбара).
        toolbar = NavigationToolbar(self.sc, self)
        layout = QtWidgets.QVBoxLayout()  # добавление графика и тулбара в лэйаут
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)

        # Создание плэйсхолдера для тулбара и самого графика.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        b = QtWidgets.QPushButton('Plot your graph', widget)  # добавление кнопки построения своего графика
        b.move(275, 11)
        b.clicked.connect(self.show_graph_build_dw)
        self.show()
    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()

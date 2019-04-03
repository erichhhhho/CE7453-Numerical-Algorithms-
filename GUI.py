import sys
import numpy as np
import ast
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy import interpolate
import datetime
from main import param,basis,solve
from PyQt5.QtWidgets import QWidget, \
    QPushButton, \
    QToolTip, \
    QMessageBox, \
    QApplication, \
    QDesktopWidget, \
    QMainWindow, \
    QAction, \
    qApp, \
    QVBoxLayout, \
    QHBoxLayout, \
    QTextBrowser, \
    QLineEdit, \
    QLabel, \
    QInputDialog, \
    QColorDialog, \
    QFontDialog, \
    QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, \
    QIcon


# QMainWindow是QWidget的派生类
class CMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # ToolTip设置
        QToolTip.setFont(QFont('华文楷体', 10))
        self.figure = plt.figure(figsize=(7, 5))
        self.figure.tight_layout()
        self.axes = self.figure.add_subplot(111)
        self.axes.set_title('CE7453 Numerical Algorithms B-Spline interpolation', fontsize=15)
        self.axes.set_xlabel('x', horizontalalignment='center', fontsize=15)
        self.axes.set_ylabel('y', horizontalalignment='center', fontsize=15)


        # statusBar设置
        self.statusBar().showMessage('Ready')
        self.canvas = FigureCanvas(self.figure)

        # 退出Action设置
        exitAction = QAction(QIcon('exit.jpg'), '&Exit', self)
        exitAction.setShortcut('ctrl+Q')
        exitAction.setStatusTip('Quit the application')
        exitAction.triggered.connect(qApp.quit) 

        # 打开文件Action设置
        OpenFileAction = QAction(QIcon('file.png'), '&Open file', self)
        OpenFileAction.setShortcut('ctrl+O')
        OpenFileAction.setStatusTip('Open file')
        OpenFileAction.triggered.connect(self.funOpenFile)

        # menuBar设置
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(OpenFileAction)
        fileMenu.addAction(exitAction)

        # toolBar设置
        self.toolbar = self.addToolBar('File')
        self.toolbar.addAction(OpenFileAction)
        self.toolbar.addAction(exitAction)

        Draw=QPushButton("Draw")
        Draw.setToolTip("Click Here to Draw the curve!")
        Draw.setStatusTip("Click Here to Draw the curve!")
        Draw.clicked.connect(self.plot_)
        Draw.resize(Draw.sizeHint())

        Clear = QPushButton("Clear")
        Clear.setToolTip("Click Here to Clear the curve!")
        Clear.setStatusTip("Click Here to Clear the curve!")
        Clear.clicked.connect(self.clear_)
        Clear.resize(Clear.sizeHint())

        Draw_Data_Points = QPushButton("Data Points")
        Draw_Data_Points.setToolTip("Click Here to Draw Data Points Only!")
        Draw_Data_Points.setStatusTip("Click Here to Draw Data Points Only!")
        Draw_Data_Points.clicked.connect(self.plot_data_points)
        Draw_Data_Points.resize(Draw_Data_Points.sizeHint())

        Draw_Curve = QPushButton("Curve Only")
        Draw_Curve.setToolTip("Click Here to Draw the interpolating Curve Only!")
        Draw_Curve.setStatusTip("Click Here to Draw the interpolating Curve Only!")
        Draw_Curve.clicked.connect(self.plot_cruve)
        Draw_Curve.resize(Draw_Curve.sizeHint())

        Draw_Polygon = QPushButton("Control Polygon")
        Draw_Polygon.setToolTip("Click Here to Draw the Control Polygon Only!")
        Draw_Polygon.setStatusTip("Click Here to Draw the Control Polygon Only!")
        Draw_Polygon.clicked.connect(self.plot_polygon)
        Draw_Polygon.resize(Draw_Polygon.sizeHint())

        # 确认PushButton设置
        btnOK = QPushButton("Compute the interpolation result")
        btnOK.setToolTip("Click here to compute the result!")
        btnOK.setStatusTip("Click here to compute the result!")
        btnOK.clicked.connect(self.compute_again)
        btnOK.resize(btnOK.sizeHint())

        # 取消PushButton设置
        btnCancel = QPushButton("Clear data")
        btnCancel.setToolTip("Click here to clear all input data!")
        btnCancel.setStatusTip("Click here to clear all input data!")
        btnCancel.clicked.connect(self.funCancel)
        btnCancel.resize(btnCancel.sizeHint())

        # 退出PushButton设置
        btnQuit = QPushButton('Exit')
        btnQuit.setToolTip("Click the button to exit the application!")
        btnQuit.setStatusTip("Click the button to exit the application!!")
        btnQuit.clicked.connect(qApp.quit)
        btnQuit.resize(btnQuit.sizeHint())



        # 更改背景色PushButton设置
        btnBackgroundColor = QPushButton('Modify BG Color in tips')
        btnBackgroundColor.setToolTip("Modify the bg color here!")
        btnBackgroundColor.setStatusTip("Modify the bg color here!")
        btnBackgroundColor.clicked.connect(self.funBackgroundColor)
        btnBackgroundColor.resize(btnBackgroundColor.sizeHint())

        # 更改字体PushButton设置
        btnFont = QPushButton('Modify Font in the tips')
        btnFont.setToolTip("Click this button to modify font!")
        btnFont.setStatusTip("Click this button to modify font!")
        btnFont.clicked.connect(self.funFont)
        btnFont.resize(btnFont.sizeHint())

        # PushButton布局
        hBox1 = QHBoxLayout()
        hBox1.addStretch(1)
        hBox1.addWidget(btnOK)
        hBox1.addWidget(btnCancel)
        hBox1.addWidget(btnFont)
        hBox1.addWidget(btnBackgroundColor)
        hBox1.addWidget(btnQuit)

        hBox3 = QHBoxLayout()
        hBox3.addStretch(1)
        hBox3.addWidget(Draw)
        hBox3.addWidget(Draw_Data_Points)
        hBox3.addWidget(Draw_Curve)
        hBox3.addWidget(Draw_Polygon)
        hBox3.addWidget(Clear)



        # QTextBrwoser是只读的多行文本框，既可以显示普通文本，又可以显示HTML
        self.labTip1 = QLabel(">>Data Points<<:")
        self.textBrowser = QTextBrowser()
        self.textBrowser.append('The default data points are stored in data.txt')
        self.textBrowser.append('The default control points and other info are stored in output_from_ui.txt')
        self.textBrowser.append('Please click the right top button to load the data.txt file first')
        self.textBrowser.append('You are able to modify the loaded data points through the text bar below after loading the file')
        # 提示标签
        self.labTip2 = QLabel(">>Plot<<:")
        self.labTip3 = QLabel(">>Tips<<:")
        # 单行文本框
        self.lineEdit = QLineEdit("Read the Data points from the data.txt file")
        self.lineEdit.selectAll()
        self.lineEdit.setEnabled(False)
        self.lineEdit.returnPressed.connect(self.funOK)
        # 布局
        hBox2 = QHBoxLayout()
        hBox2.addWidget(self.labTip1)
        hBox2.addWidget(self.lineEdit)
        # 布局
        vBox = QVBoxLayout()
        vBox.addWidget(self.labTip2)
        vBox.addWidget(self.canvas)
        vBox.addWidget(self.labTip3)
        vBox.addWidget(self.textBrowser)
        vBox.addLayout(hBox2)
        vBox.addLayout(hBox1)
        vBox.addLayout(hBox3)
        widget = QWidget()
        self.setCentralWidget(widget)  # 建立的widget在窗体的中间位置
        widget.setLayout(vBox)

        # 布局完毕后，才可得到焦点
        self.lineEdit.setFocus()

        # Window设置
        self.resize(500, 300)
        self.center()
        self.setFont(QFont('华文楷体', 10))
        self.setWindowTitle('CE7453 Numerical Algorithms B-Spline Interpolation --Developed By He Wei')
        self.setWindowIcon(QIcon('NTU-logo.jpg'))
        self.show()
    def clear_(self):

        self.axes.cla()
        self.axes.set_title('CE7453 Numerical Algorithms B-Spline interpolation', fontsize=15)
        self.axes.set_xlabel('x', horizontalalignment='center', fontsize=15)
        self.axes.set_ylabel('y', horizontalalignment='center', fontsize=15)
        self.canvas.draw()

    def plot_cruve(self):
        self.axes.cla()

        data = []

        control_point_list = []

        with open("data.txt", "rt") as file:
            for line in file:
                data.append(list(map(int, line.strip().split(" "))))
        with open("output_from_ui.txt", "rt") as output:
            for idx, line in enumerate(output.readlines()):
                line = line.strip('\n')
                if idx == 0:
                    k = int(line.strip('\n'))
                elif idx == 1:
                    num_cpoints = int(line.strip('\n'))
                elif idx == 3:
                    knot = line.strip('\n').split(' ')
                    knot.pop()
                    knot = list(map(float, knot))
                elif idx >= 5:
                    control_point = line.strip("\n").split(' ')
                    control_point = list(map(float, control_point))
                    control_point_list.append(control_point)

        control_point_list = np.array(control_point_list)
        control_point_x = control_point_list[:, 0]
        control_point_y = control_point_list[:, 1]



        unew = np.arange(0, 1, 0.01)
        inter_x, inter_y = np.array(interpolate.splev(unew, (knot, control_point_list.T, 3)))
        self.axes.set_title('CE7453 Numerical Algorithms B-Spline interpolation', fontsize=15)
        self.axes.set_xlabel('x', horizontalalignment='center', fontsize=15)
        self.axes.set_ylabel('y', horizontalalignment='center', fontsize=15)
        self.axes.plot(inter_x, inter_y, linestyle='-', color='green', label='Degree 3 B-Spline Curve(Chord)')
        self.axes.legend()
        self.canvas.draw()

    def plot_data_points(self):
        self.axes.cla()
        data = []
        with open("data.txt", "rt") as file:
            for line in file:
                data.append(list(map(int, line.strip().split(" "))))
        data = np.array(data)
        x = data[:, 0]
        y = data[:, 1]

        self.axes.set_title('CE7453 Numerical Algorithms B-Spline interpolation', fontsize=15)
        self.axes.set_xlabel('x', horizontalalignment='center', fontsize=15)
        self.axes.set_ylabel('y', horizontalalignment='center', fontsize=15)
        self.axes.plot(x, y, 'ko', label='Data Points', markersize=4)
        self.axes.legend()
        self.canvas.draw()

    def plot_polygon(self):
        self.axes.cla()
        control_point_list=[]
        with open("output_from_ui.txt", "rt") as output:
            for idx, line in enumerate(output.readlines()):
                line = line.strip('\n')
                if idx == 0:
                    k = int(line.strip('\n'))
                elif idx == 1:
                    num_cpoints = int(line.strip('\n'))
                elif idx == 3:
                    knot = line.strip('\n').split(' ')
                    knot.pop()
                    knot = list(map(float, knot))
                elif idx >= 5:
                    control_point = line.strip("\n").split(' ')
                    control_point = list(map(float, control_point))
                    control_point_list.append(control_point)

        control_point_list = np.array(control_point_list)
        control_point_x = control_point_list[:, 0]
        control_point_y = control_point_list[:, 1]

        self.axes.set_title('CE7453 Numerical Algorithms B-Spline interpolation', fontsize=15)
        self.axes.set_xlabel('x', horizontalalignment='center', fontsize=15)
        self.axes.set_ylabel('y', horizontalalignment='center', fontsize=15)
        self.axes.plot(control_point_x, control_point_y, color='red', marker='.', linestyle='--',
                       label='Control Polygon(Chord)', markersize=6)
        self.axes.legend()
        self.canvas.draw()

    def plot_(self):


        self.axes.cla()

        data = []
        knots = []
        knots_uniform = []
        control_point_list = []
        control_point_list_uniform = []
        with open("data.txt", "rt") as file:
            for line in file:
                data.append(list(map(int, line.strip().split(" "))))
        with open("output_from_ui.txt", "rt") as output:
            for idx, line in enumerate(output.readlines()):
                line = line.strip('\n')
                if idx == 0:
                    k = int(line.strip('\n'))
                elif idx == 1:
                    num_cpoints = int(line.strip('\n'))
                elif idx == 3:
                    knot = line.strip('\n').split(' ')
                    knot.pop()
                    knot = list(map(float, knot))
                elif idx >= 5:
                    control_point = line.strip("\n").split(' ')
                    control_point = list(map(float, control_point))
                    control_point_list.append(control_point)

        control_point_list = np.array(control_point_list)
        control_point_x = control_point_list[:, 0]
        control_point_y = control_point_list[:, 1]

        data = np.array(data)
        x = data[:, 0]
        y = data[:, 1]
        tck, u = interpolate.splprep([x, y], s=0, k=3)
        unew = np.arange(0, 1, 0.01)
        u = np.linspace(0, 1, num=100, endpoint=True)
        out = interpolate.splev(u, tck)

        inter_x, inter_y = np.array(interpolate.splev(unew, (knot, control_point_list.T, 3)))

        self.axes.set_title('CE7453 Numerical Algorithms B-Spline interpolation', fontsize=15)
        self.axes.set_xlabel('x', horizontalalignment='center', fontsize=15)
        self.axes.set_ylabel('y', horizontalalignment='center', fontsize=15)
        # plt.plot(out[0], out[1], 'y',color='blue',label='Degree 3 Scipy method')
        self.axes.plot(control_point_x, control_point_y, color='red', marker='.', linestyle='--',
                 label='Control Polygon(Chord)', markersize=6)
        self.axes.plot(inter_x, inter_y, linestyle='-', color='green', label='Degree 3 B-Spline Curve(Chord)')
        self.axes.plot(x, y, 'ko', label='Data Points', markersize=4)
        self.axes.legend()
        # ax.tight_layout()
        # plt.savefig('Comparison.png')
        # plt.show()

        self.canvas.draw()

    def center(self):
        # 得到主窗体的框架信息
        qr = self.frameGeometry()
        # 得到桌面的中心
        cp = QDesktopWidget().availableGeometry().center()
        # 框架的中心与桌面中心对齐
        qr.moveCenter(cp)
        # 自身窗体的左上角与框架的左上角对齐
        self.move(qr.topLeft())
    def compute_again(self):
        try:
            degree=3
            text = self.lineEdit.text()


            data = ast.literal_eval(text)

            with open("data.txt", "wt") as output:
                for points in data:
                    output.write(str(points[0]) + " " + str(points[1]) + '\n')

            n = len(data) - 1
            knots_len = n + 7
            control_points_num = knots_len - degree - 1

            t_list, u_list = param(data, type='chord')
            N = basis(t_list, u_list)
            x_list = []
            y_list = []
            x_list.append(0)
            y_list.append(0)
            for points in data:
                x_list.append(points[0])
                y_list.append(points[1])
            x_list.append(0)
            y_list.append(0)

            control_points_x_list = solve(N, x_list)
            control_points_y_list = solve(N, y_list)
            control_points_x_list[abs(control_points_x_list) < ((np.e) ** (-10))] = 0.0
            control_points_y_list[abs(control_points_y_list) < ((np.e) ** (-10))] = 0.0

            self.textBrowser.append(str(datetime.datetime.now())+'\tData Points List(Totally {}):'.format(str(len(data))))
            self.textBrowser.append(str(datetime.datetime.now())+'\t'+''.join(str(e) + ' ' for e in data))
            # print(data)
            self.textBrowser.append(str(datetime.datetime.now())+'\tControl Points List(Totally {}):'.format(str(len(control_points_x_list))))
            for x, y in zip(control_points_x_list, control_points_y_list):
                # print('[' + str(round(x, 2)) + " " + str(round(y, 2)) + ']')
                self.textBrowser.append(str(datetime.datetime.now())+'\t[' + str(round(x, 2)) + " " + str(round(y, 2)) + ']')
            np.set_printoptions(suppress=True, precision=2)
            self.textBrowser.append(str(datetime.datetime.now())+'Matrix N:')
            self.textBrowser.append(str(datetime.datetime.now())+'\n'+'\n'.join('\t'.join('%0.3f' %x for x in y) for y in N))



            with open("output_from_ui.txt", "wt") as output:
                output.write(str(degree) + '\n')
                output.write(str(len(control_points_x_list)) + '\n')
                output.write('\n')
                for knots in u_list:
                    output.write(str(knots) + ' ')

                output.write('\n')
                output.write('\n')
                for x, y in zip(control_points_x_list, control_points_y_list):
                    output.write(str(x) + " " + str(y) + '\n')
            self.textBrowser.append(str(datetime.datetime.now())+"\tAlready Output the computation result on output_from_ui.txt\n")

        except:
            self.textBrowser.append(str(datetime.datetime.now())+"\tInput Invalid! You didn't open a file or the input format is not correct! Try again pls!")

    def funOK(self):
        try:
            text = self.lineEdit.text()
            self.textBrowser.append(str(datetime.datetime.now())+"\tInput Data Points: {}".format(text))
        except:
            self.textBrowser.append(str(datetime.datetime.now())+"\tInput Invalid! You didn't open a file or the input format is not correct! Try again pls!")

    def funCancel(self):
        self.lineEdit.clear()

    def funTip(self):
        # 返回两个值：输入的文本和点击的按钮
        text, ok = QInputDialog.getText(self, 'Input new symbol', 'Symbol：')
        if ok:
            self.labTip.setText(text)

    def funBackgroundColor(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.textBrowser.setStyleSheet("QTextBrowser{background-color:%s}" % col.name())


    def funFont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.textBrowser.setFont(font)

    def funOpenFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', 'data.txt', '*.txt')
        data=[]
        degree = 3
        try:
            if fname[0]:

                with open(fname[0], "rt") as file:
                    for line in file:
                        data.append(list(map(int, line.strip().split(" "))))
                    str1 = ','.join(str(e) for e in data)
                    self.lineEdit.setText(str1)
                n = len(data) - 1
                knots_len = n + 7
                control_points_num = knots_len - degree - 1

                t_list, u_list = param(data, type='chord')
                N = basis(t_list, u_list)
                x_list = []
                y_list = []
                x_list.append(0)
                y_list.append(0)
                for points in data:
                    x_list.append(points[0])
                    y_list.append(points[1])
                x_list.append(0)
                y_list.append(0)

                control_points_x_list = solve(N, x_list)
                control_points_y_list = solve(N, y_list)
                control_points_x_list[abs(control_points_x_list) < ((np.e) ** (-10))] = 0.0
                control_points_y_list[abs(control_points_y_list) < ((np.e) ** (-10))] = 0.0

                self.textBrowser.append(str(datetime.datetime.now())+'\tData Points List(Totally {}):'.format(str(len(data))))
                self.textBrowser.append(str(datetime.datetime.now())+'\t'+''.join(str(e) + ' ' for e in data))
                # print(data)
                self.textBrowser.append(str(datetime.datetime.now())+'\tControl Points List(Totally {}):'.format(str(len(control_points_x_list))))
                for x, y in zip(control_points_x_list, control_points_y_list):
                    # print('[' + str(round(x, 2)) + " " + str(round(y, 2)) + ']')
                    self.textBrowser.append(str(datetime.datetime.now())+'\t[' + str(round(x, 2)) + " " + str(round(y, 2)) + ']')
                with open("output_from_ui.txt", "wt") as output:
                    output.write(str(degree) + '\n')
                    output.write(str(len(control_points_x_list)) + '\n')
                    output.write('\n')
                    for knots in u_list:
                        output.write(str(knots) + ' ')

                    output.write('\n')
                    output.write('\n')
                    for x, y in zip(control_points_x_list, control_points_y_list):
                        output.write(str(x) + " " + str(y) + '\n')
                self.textBrowser.append(str(datetime.datetime.now())+"\tAlready Output the interpolation result on output_from_ui.txt\n")
                self.lineEdit.setEnabled(True)

        except:
            self.textBrowser.append(str(datetime.datetime.now())
            +"Read Error!!!")

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, QCloseEvent):
        reply = QMessageBox.question(self,
                                     'CE7453 Numerical Algorithms B-Spline Interpolation',
                                     "Quit？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = CMainWindow()
    MainWindow.resize(1080, 880)
    MainWindow.show()

    sys.exit(app.exec_())
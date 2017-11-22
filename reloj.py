from PyQt5 import QtCore, QtGui, QtWidgets

class ShapedClock(QtWidgets.QWidget):
    hourHand = QtGui.QPolygon([
        QtCore.QPoint(7, 8),
        QtCore.QPoint(-7, 8),
        QtCore.QPoint(0, -40)
    ])

    minuteHand = QtGui.QPolygon([
        QtCore.QPoint(7, 8),
        QtCore.QPoint(-7, 8),
        QtCore.QPoint(0, -70)
    ])

    hourColor = QtGui.QColor(127, 0, 127)
    minuteColor = QtGui.QColor(0, 127, 127, 191)

    def __init__(self, parent=None):
        super(ShapedClock, self).__init__(parent,
                QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)

        quitAction = QtWidgets.QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=QtWidgets.qApp.quit)
        self.addAction(quitAction)

        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.setToolTip("Drag the clock with the left mouse button.\n"
                "Use the right mouse button to open a context menu.")
        self.setWindowTitle(self.tr("Shaped Analog Clock"))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def paintEvent(self, event):
        side = min(self.width(), self.height())
        time = QtCore.QTime.currentTime()

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(ShapedClock.hourColor)

        painter.save()
        painter.rotate(30.0 * ((time.hour() + time.minute() / 60.0)))
        painter.drawConvexPolygon(ShapedClock.hourHand)
        painter.restore()

        painter.setPen(ShapedClock.hourColor)

        for i in range(12):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(30.0)

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(ShapedClock.minuteColor)

        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.drawConvexPolygon(ShapedClock.minuteHand)
        painter.restore()

        painter.setPen(ShapedClock.minuteColor)

        for j in range(60):
            if (j % 5) != 0:
                painter.drawLine(92, 0, 96, 0)

            painter.rotate(6.0)

    def resizeEvent(self, event):
        side = min(self.width(), self.height())

        maskedRegion = QtGui.QRegion(self.width()/2 - side/2, self.height()/2 - side/2, side, side, QtGui.QRegion.Ellipse)
        self.setMask(maskedRegion)

    def sizeHint(self):
        return QtCore.QSize(100, 100)


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    clock = ShapedClock()
    clock.show()
    sys.exit(app.exec_()) 
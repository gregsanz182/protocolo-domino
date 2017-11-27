from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLabel, QInputDialog, QLineEdit, QHBoxLayout
from PyQt5.QtCore import QSize, Qt

class InputDialog(QDialog):

    def __init__(self, tituloVentana, textoLabel, padre=None):
        super().__init__(padre)
        self.setWindowTitle(tituloVentana)
        self.layout = QVBoxLayout(self)
        self.label = QLabel(textoLabel)
        self.layout.addWidget(self.label)
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedHeight(23)
        self.lineEdit.setStyleSheet("font-size: 13px;")
        self.lineEdit.setMaxLength(13)
        self.layout.addWidget(self.lineEdit)
        self.botonAceptar = QPushButton("Aceptar")
        self.botonAceptar.setFixedHeight(28)
        self.layout2 = QHBoxLayout()
        self.layout.addLayout(self.layout2)
        self.layout2.addStretch()
        self.layout2.addWidget(self.botonAceptar)
        self.layout2.addStretch()
        self.botonAceptar.clicked.connect(self.aceptarTexto)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

    def aceptarTexto(self):
        self.close()

    @staticmethod
    def getText(tituloVentana, textoLabel, padre=None):
        d = InputDialog(tituloVentana, textoLabel, padre)
        d.show()
        d.exec_()
        return d.lineEdit.text()
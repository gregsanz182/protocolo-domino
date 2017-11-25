from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLabel, QTableWidget, QInputDialog, QLineEdit, QHBoxLayout, QMessageBox
from PyQt5.QtCore import QSize, Qt

class PreferencesDialog(QDialog):

    def __init__(self, padre=None):
        super().__init__(padre)
        self.setWindowTitle('Servidores')
        self.layout = QVBoxLayout(self)
        self.setFixedSize(QSize(420, 320))

        self.labelDescripcion = QLabel("Selecciona una de las siguientes mesas disponibles:")
        self.tablaServidores = QTableWidget()
        self.botonConectar = QPushButton("Conectar")

        self.layout.addWidget(self.labelDescripcion)
        self.layout.addWidget(self.tablaServidores)
        self.layout.addWidget(self.botonConectar)

    @staticmethod
    def getPreferences(padre=None):
        nombre = InputDialog.getText("Nombre de jugador", "Ingrese su nombre de jugador (máximo 13 caracteres)", padre)
        dialog = PreferencesDialog(padre)
        dialog.show()
        dialog.exec_()

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
        self.botonAceptar.clicked.connect(self.aceptarNombre)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

    def aceptarNombre(self):
        self.close()

    @staticmethod
    def getText(tituloVentana, textoLabel, padre=None):
        d = InputDialog(tituloVentana, textoLabel, padre)
        d.show()
        d.exec_()
        return d.lineEdit.text()

from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLabel, QListWidget, QInputDialog, QLineEdit, QHBoxLayout, QMessageBox, QAbstractItemView
from PyQt5.QtCore import QSize, Qt

class ServidoresDialog(QDialog):

    def __init__(self, metodoSlot, padre=None):
        super().__init__(padre)
        self.setWindowTitle('Servidores')
        self.layout = QVBoxLayout(self)
        self.setFixedSize(QSize(420, 320))
        self.setModal(True)

        self.metodoSlot = metodoSlot

        self.servidores = []

        self.labelDescripcion = QLabel("Selecciona una de las siguientes mesas disponibles:")
        self.listaServidores = QListWidget()
        self.listaServidores.setSelectionMode(QAbstractItemView.SingleSelection)
        self.botonConectar = QPushButton("Conectar")
        self.botonConectar.setFixedHeight(28)

        self.layout.addWidget(self.labelDescripcion)
        self.layout.addWidget(self.listaServidores)
        self.layout.addWidget(self.botonConectar)
        self.botonConectar.clicked.connect(self.conectarServer)

    def nuevoServer(self, serverInfo):
        flag = False
        for servidor in self.servidores:
            if servidor['nombre'] == serverInfo['nombre'] and servidor['direccion'] == serverInfo['direccion']:
                flag = True
        if not flag:
            self.servidores.append(serverInfo)
            self.listaServidores.addItem("'{0}' ====> {1}".format(serverInfo['nombre'], serverInfo['direccion']))

    def conectarServer(self):
        indexes = self.listaServidores.selectedIndexes()
        if len(indexes) > 0:
            self.metodoSlot(self.servidores[indexes[0].row()])
            self.close()

        

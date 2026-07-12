from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QStatusBar,
    QToolBar,
)

from gui.image_view import ImageView


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Straightener Pro")
        self.resize(1400, 900)

        self.viewer = ImageView()
        self.setCentralWidget(self.viewer)

        self.create_toolbar()

        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready")

    def create_toolbar(self):

        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)

        self.addToolBar(toolbar)

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_image)

        toolbar.addAction(open_action)

    def open_image(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Images (*.jpg *.jpeg *.png *.bmp *.tif *.tiff)"
        )

        if not filename:
            return

        self.statusBar().showMessage(filename)
        self.viewer.load_image(filename)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QToolBar,
)

from gui.image_view import ImageView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Straightener")
        self.resize(1400, 900)

        # Create image viewer
        self.viewer = ImageView()
        self.setCentralWidget(self.viewer)

        # Toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_image)
        toolbar.addAction(open_action)

        # Status bar
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready")

    def open_image(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
        )

        if not filename:
            return

        if self.viewer.load_image(filename):
            self.statusBar().showMessage(f"Loaded: {filename}")
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Unable to load the selected image."
            )
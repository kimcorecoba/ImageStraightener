from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsView,
)


class ImageView(QGraphicsView):
    def __init__(self):
        super().__init__()

        # Create the scene
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Image item
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

        # Viewer settings
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)

    def load_image(self, filename):
        """Load an image into the viewer."""

        pixmap = QPixmap(filename)

        if pixmap.isNull():
            return False

        self.pixmap_item.setPixmap(pixmap)

        self.scene.setSceneRect(self.pixmap_item.boundingRect())

        self.fitInView(
            self.scene.sceneRect(),
            Qt.KeepAspectRatio
        )

        return True

    def wheelEvent(self, event):
        """Zoom with the mouse wheel."""

        zoom_factor = 1.15

        if event.angleDelta().y() > 0:
            self.scale(zoom_factor, zoom_factor)
        else:
            self.scale(1 / zoom_factor, 1 / zoom_factor)
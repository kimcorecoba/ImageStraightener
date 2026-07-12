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

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

        self.setRenderHints(
            self.renderHints()
        )

        self.setDragMode(QGraphicsView.ScrollHandDrag)

        self.setTransformationAnchor(
            QGraphicsView.AnchorUnderMouse
        )

    def load_image(self, filename):

        pixmap = QPixmap(filename)

        if pixmap.isNull():
            return

        self.pixmap_item.setPixmap(pixmap)

        self.scene.setSceneRect(
            self.pixmap_item.boundingRect()
        )

        self.fitInView(
            self.scene.sceneRect(),
            Qt.KeepAspectRatio
        )

    def wheelEvent(self, event):

        zoom = 1.25

        if event.angleDelta().y() > 0:
            self.scale(zoom, zoom)
        else:
            self.scale(1 / zoom, 1 / zoom)
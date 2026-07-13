from PySide6.QtCore import QRectF
from PySide6.QtGui import QColor, QPen
from PySide6.QtWidgets import (
    QGraphicsRectItem,
)


class RectangleOverlay(QGraphicsRectItem):

    def __init__(self):

        super().__init__()

        self.setPen(
            QPen(
                QColor(0, 255, 0),
                3
            )
        )

        self.hide()

    def set_rectangle(self, x, y, w, h):

        self.setRect(
            QRectF(
                x,
                y,
                w,
                h
            )
        )

        self.show()

    def clear(self):

        self.hide()
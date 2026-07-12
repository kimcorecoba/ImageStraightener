
import cv2
import numpy as np


class RectangleDetector:
    """
    Detects the best rectangular object in an image.
    """

    def __init__(self, min_area_ratio=0.05):
        self.min_area_ratio = min_area_ratio

    def detect(self, image):
        """
        Returns:
            corners: ndarray (4,2) or None
            confidence: float (0-1)
        """

        original = image.copy()

        scale = 1200 / max(image.shape[:2])

        if scale < 1:
            image = cv2.resize(
                image,
                None,
                fx=scale,
                fy=scale,
                interpolation=cv2.INTER_AREA
            )

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        candidates = []

        methods = self._generate_binary_images(gray)

        for binary in methods:

            contours, _ = cv2.findContours(
                binary,
                cv2.RETR_LIST,
                cv2.CHAIN_APPROX_SIMPLE
            )

            for contour in contours:

                area = cv2.contourArea(contour)

                if area < image.shape[0] * image.shape[1] * self.min_area_ratio:
                    continue

                peri = cv2.arcLength(contour, True)

                approx = cv2.approxPolyDP(
                    contour,
                    0.02 * peri,
                    True
                )

                if len(approx) != 4:
                    continue

                if not cv2.isContourConvex(approx):
                    continue

                score = self._score_rectangle(
                    approx.reshape(4, 2),
                    area
                )

                candidates.append(
                    (score, approx.reshape(4, 2))
                )

        if len(candidates) == 0:
            return None, 0.0

        candidates.sort(key=lambda x: x[0], reverse=True)

        best_score, best = candidates[0]

        if scale < 1:
            best = best / scale

        confidence = min(best_score / 100.0, 1.0)

        return best.astype(np.float32), confidence

    def _generate_binary_images(self, gray):

        images = []

        canny = cv2.Canny(gray, 50, 150)
        images.append(canny)

        adaptive = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            15,
            5
        )
        images.append(adaptive)

        _, otsu = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        images.append(otsu)

        return images

    def _score_rectangle(self, points, area):

        score = 0

        score += area / 1000

        angles = []

        for i in range(4):

            p0 = points[i]
            p1 = points[(i + 1) % 4]
            p2 = points[(i + 2) % 4]

            v1 = p0 - p1
            v2 = p2 - p1

            cosine = np.dot(v1, v2) / (
                np.linalg.norm(v1) *
                np.linalg.norm(v2)
            )

            angle = np.degrees(
                np.arccos(
                    np.clip(cosine, -1, 1)
                )
            )

            angles.append(angle)

        penalty = sum(abs(a - 90) for a in angles)

        score -= penalty

        return score
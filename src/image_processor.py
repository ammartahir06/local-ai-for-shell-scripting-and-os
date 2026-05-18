"""Image processing module using OpenCV.

Provides image preprocessing capabilities for extracting code from
screenshots or photos of code. Uses OpenCV for image manipulation
including grayscale conversion, thresholding, noise reduction,
contour detection, and perspective correction.

This enables users to take a photo of code on a whiteboard or
screenshot and have the assistant process it.
"""

import os
import numpy as np
import cv2


class ImageProcessor:
    """Process code images using OpenCV for text extraction preparation.

    Applies computer vision techniques to enhance code images:
    - Grayscale conversion
    - Adaptive thresholding for varying lighting
    - Noise reduction with Gaussian blur
    - Morphological operations to clean text
    - Contour detection to find code regions
    - Perspective correction for angled photos
    - Edge detection for structure analysis
    """

    def __init__(self, output_dir: str = "output/processed"):
        """Initialize with output directory for processed images."""
        self._output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def preprocess_for_ocr(self, image_path: str) -> str:
        """Apply full preprocessing pipeline to prepare image for OCR.

        Steps:
        1. Load image
        2. Convert to grayscale
        3. Apply Gaussian blur for noise reduction
        4. Apply adaptive thresholding
        5. Apply morphological operations
        6. Save processed image

        Args:
            image_path: Path to the input image

        Returns:
            Path to the processed image ready for OCR
        """
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Cannot load image: {image_path}")

        # Step 1: Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Step 2: Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)

        # Step 3: Apply adaptive thresholding
        # This handles varying lighting conditions in photos
        thresh = cv2.adaptiveThreshold(
            blurred, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            blockSize=11,
            C=2,
        )

        # Step 4: Morphological operations to clean up text
        kernel = np.ones((1, 1), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)

        # Save processed image
        basename = os.path.splitext(os.path.basename(image_path))[0]
        output_path = os.path.join(self._output_dir, f"{basename}_processed.png")
        cv2.imwrite(output_path, cleaned)

        return output_path

    def detect_code_region(self, image_path: str) -> tuple[np.ndarray, list]:
        """Detect the region containing code in an image.

        Uses contour detection to find the largest rectangular region
        that likely contains code text.

        Args:
            image_path: Path to the input image

        Returns:
            Tuple of (cropped_image, bounding_box_coordinates)
        """
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Cannot load image: {image_path}")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Edge detection
        edges = cv2.Canny(gray, 50, 150)

        # Dilate to connect nearby edges
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=2)

        # Find contours
        contours, _ = cv2.findContours(
            dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return img, [0, 0, img.shape[1], img.shape[0]]

        # Find the largest contour (likely the code block)
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)

        # Add padding
        padding = 10
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(img.shape[1] - x, w + 2 * padding)
        h = min(img.shape[0] - y, h + 2 * padding)

        cropped = img[y:y+h, x:x+w]
        return cropped, [x, y, w, h]

    def correct_perspective(self, image_path: str) -> str:
        """Apply perspective correction for angled photos of code.

        Detects the four corners of the code region and applies
        a perspective transform to get a flat, rectangular view.

        Args:
            image_path: Path to the input image

        Returns:
            Path to the perspective-corrected image
        """
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Cannot load image: {image_path}")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 75, 200)

        # Find contours
        contours, _ = cv2.findContours(
            edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
        )

        # Sort by area and find the largest quadrilateral
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        target_contour = None
        for contour in contours[:5]:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            if len(approx) == 4:
                target_contour = approx
                break

        if target_contour is None:
            # No quadrilateral found, return original
            output_path = os.path.join(
                self._output_dir,
                f"{os.path.splitext(os.path.basename(image_path))[0]}_corrected.png"
            )
            cv2.imwrite(output_path, img)
            return output_path

        # Order points: top-left, top-right, bottom-right, bottom-left
        pts = target_contour.reshape(4, 2).astype(np.float32)
        pts = self._order_points(pts)

        # Compute dimensions of the new image
        width = int(max(
            np.linalg.norm(pts[0] - pts[1]),
            np.linalg.norm(pts[2] - pts[3])
        ))
        height = int(max(
            np.linalg.norm(pts[0] - pts[3]),
            np.linalg.norm(pts[1] - pts[2])
        ))

        # Destination points
        dst = np.array([
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
            [0, height - 1],
        ], dtype=np.float32)

        # Apply perspective transform
        matrix = cv2.getPerspectiveTransform(pts, dst)
        warped = cv2.warpPerspective(img, matrix, (width, height))

        output_path = os.path.join(
            self._output_dir,
            f"{os.path.splitext(os.path.basename(image_path))[0]}_corrected.png"
        )
        cv2.imwrite(output_path, warped)
        return output_path

    def enhance_contrast(self, image_path: str) -> str:
        """Enhance image contrast using CLAHE (Contrast Limited Adaptive
        Histogram Equalization) for better text visibility.

        Args:
            image_path: Path to the input image

        Returns:
            Path to the contrast-enhanced image
        """
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Cannot load image: {image_path}")

        # Convert to LAB color space
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)

        # Apply CLAHE to the L channel
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced_l = clahe.apply(l_channel)

        # Merge channels back
        enhanced_lab = cv2.merge([enhanced_l, a_channel, b_channel])
        enhanced_img = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

        output_path = os.path.join(
            self._output_dir,
            f"{os.path.splitext(os.path.basename(image_path))[0]}_enhanced.png"
        )
        cv2.imwrite(output_path, enhanced_img)
        return output_path

    def analyze_code_structure(self, image_path: str) -> dict:
        """Analyze the visual structure of code in an image.

        Uses line detection and spacing analysis to estimate:
        - Number of code lines
        - Indentation levels
        - Code density

        Args:
            image_path: Path to the input image

        Returns:
            Dictionary with structural analysis results
        """
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Cannot load image: {image_path}")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape

        # Threshold to get text regions
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Horizontal projection to detect lines
        h_projection = np.sum(binary, axis=1)

        # Count lines (regions with significant horizontal content)
        threshold = width * 0.05  # At least 5% of width has content
        in_line = False
        line_count = 0
        line_heights = []
        line_start = 0

        for i, val in enumerate(h_projection):
            if val > threshold and not in_line:
                in_line = True
                line_start = i
            elif val <= threshold and in_line:
                in_line = False
                line_count += 1
                line_heights.append(i - line_start)

        # Estimate indentation by analyzing left margins
        v_projection = np.sum(binary, axis=0)
        left_margin = 0
        for i, val in enumerate(v_projection):
            if val > height * 0.02:
                left_margin = i
                break

        # Code density (percentage of image that contains text)
        text_pixels = np.sum(binary > 0)
        total_pixels = height * width
        density = text_pixels / total_pixels if total_pixels > 0 else 0

        return {
            "estimated_lines": line_count,
            "image_dimensions": (width, height),
            "avg_line_height": float(np.mean(line_heights)) if line_heights else 0,
            "left_margin_px": left_margin,
            "code_density": round(density * 100, 1),
            "has_indentation": left_margin > width * 0.05,
        }

    @staticmethod
    def _order_points(pts: np.ndarray) -> np.ndarray:
        """Order 4 points as: top-left, top-right, bottom-right, bottom-left."""
        rect = np.zeros((4, 2), dtype=np.float32)

        # Top-left has smallest sum, bottom-right has largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        # Top-right has smallest difference, bottom-left has largest
        d = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(d)]
        rect[3] = pts[np.argmax(d)]

        return rect

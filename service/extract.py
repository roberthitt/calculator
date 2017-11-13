"""
Module for extracting text from images.
"""

import io

from PIL import Image
import pytesseract


class Extractor:
    """
    Class for extracting text from images.
    """

    @staticmethod
    def extract(file_bytes):
        """
        Extracts the text from the given image.

        Args:
            file_bytes: binary image file
        """

        f = io.BytesIO(file_bytes)
        return pytesseract.image_to_string(Image.open(f))

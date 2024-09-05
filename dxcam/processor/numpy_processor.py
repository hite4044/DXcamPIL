import ctypes
import time

from PIL import Image
from .base import Processor


class NumpyProcessor(Processor):
    def process(self, rect, width, height, region, rotation_angle):
        pitch = int(rect.Pitch)

        if rotation_angle in (0, 180):
            size = pitch * height
        else:
            size = pitch * width

        buffer = ctypes.string_at(rect.pBits, size)
        pitch = pitch // 4
        if rotation_angle in (0, 180): # BGRA
            image = Image.frombuffer("RGBA", (pitch, height), buffer)
            # image = np.ndarray((height, pitch, 4), dtype=np.uint8, buffer=buffer)
        elif rotation_angle in (90, 270):
            image = Image.frombuffer("RGBA", (width, pitch), buffer)
            # image = np.ndarray((width, pitch, 4), dtype=np.uint8, buffer=buffer)
        blue, green, red, alpha = image.split()
        image = Image.merge("RGBA", (red, green, blue, alpha))

        if rotation_angle == 90:
            image = image.transpose(Image.ROTATE_90)
            # image = np.rot90(image, axes=(1, 0))
        elif rotation_angle == 180:
            image = image.transpose(Image.ROTATE_180)
            # image = np.rot90(image, k=2, axes=(0, 1))
        elif rotation_angle == 270:
            image = image.transpose(Image.ROTATE_270)
            # image = np.rot90(image, axes=(0, 1))

        if rotation_angle in (0, 180) and pitch != width:
            image = image.crop((0, 0, width, image.height))
            # image = image[:, :width, :]
        elif rotation_angle in (90, 270) and pitch != height:
            image = image.crop((0, 0,image.width, height))
            # image = image[:height, :, :]

        if region[2] - region[0] != width or region[3] - region[1] != height:
            image = image.crop((region[0], region[1], region[2] - region[0], region[3] - region[1]))
            # image = image[region[1] : region[3], region[0] : region[2], :]

        return image

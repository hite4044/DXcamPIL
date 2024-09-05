import ctypes

from PIL import Image


class PillowProcessor:
    def __init__(self, color_mode: str = "RGB"):
        self.color_mode = color_mode

    def process(self, rect, width, height, region, rotation_angle):
        pitch = int(rect.Pitch)

        if rotation_angle in (0, 180):
            size = pitch * height
        else:
            size = pitch * width

        buffer = ctypes.string_at(rect.pBits, size)
        pitch //= 4
        # 先将数据已错误的通道载入
        if rotation_angle in (0, 180):
            image = Image.frombuffer("RGBA", (pitch, height), buffer)
        elif rotation_angle in (90, 270):
            image = Image.frombuffer("RGBA", (width, pitch), buffer)
        else:
            raise RuntimeError("Error Rotation Angle")
        # 再分离通道并以正确的通道进行组合
        blue, green, red, alpha = image.split()
        if self.color_mode == "RGB":
            image = Image.merge("RGB", (red, green, blue))
        elif self.color_mode == "RGBA":
            image = Image.merge("RGBA", (red, green, blue, alpha))
        else:
            raise RuntimeError(f"Bad color mode: {self.color_mode}, "
                               "support RGBA or RGB, "
                               "reprocess if need another format")

        if rotation_angle == 90:
            image = image.transpose(Image.Transpose.ROTATE_90)
        elif rotation_angle == 180:
            image = image.transpose(Image.Transpose.ROTATE_180)
        elif rotation_angle == 270:
            image = image.transpose(Image.Transpose.ROTATE_270)

        if rotation_angle in (0, 180) and pitch != width:
            image = image.crop((0, 0, width, image.height))
        elif rotation_angle in (90, 270) and pitch != height:
            image = image.crop((0, 0, image.width, height))

        if region[2] - region[0] != width or region[3] - region[1] != height:
            image = image.crop((region[0], region[1], region[2] - region[0], region[3] - region[1]))

        return image

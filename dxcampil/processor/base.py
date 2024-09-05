class Processor:
    def __init__(self, output_color: str = "RGB"):
        self.color_mode = output_color
        self.backend = self._initialize_backend()

    def process(self, rect, width, height, region, rotation_angle):
        return self.backend.process(rect, width, height, region, rotation_angle)

    def _initialize_backend(self):
        from dxcampil.processor.pillow_processor import PillowProcessor

        return PillowProcessor(self.color_mode)

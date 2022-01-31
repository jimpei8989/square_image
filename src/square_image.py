from typing import Optional
from pathlib import Path
from PIL import Image

from background_generator import BackgroundGenerator
from image_processor import ImageProcessor

class Wrapper:
    def __init__(self, args):
        self.background_generator = BackgroundGenerator(args)
        self.image_processor = ImageProcessor(args)
        self.show_image = args.show_image

    def square_single(self, input_path: Path, output_path: Optional[Path]):
        img = Image.open(input_path)

        background_img = self.background_generator(img)
        output_img = self.image_processor(img, background_img)

        if self.show_image:
            output_img.show()

        if output_path is not None:
            output_img.save(output_path)

    def process_single(self, input_path, output_path):
        self.square_single(input_path, output_path)

    def process_batch(self, input_path, output_path):
        raise NotImplementedError()


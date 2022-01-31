from typing import Tuple
from PIL import Image

class ImageProcessor:
    def __init__(self, args):
        self.min_padding = args.min_padding
        self.max_padding = args.max_padding     # Not implemented yet
        self.output_ratio = args.output_ratio
        self.fixed_output_resolution = args.fixed_output_resolution

        if self.max_padding != 0:
            raise NotImplementedError("Some features are not implemented yet")

    def _define_output_size(self, original_size: Tuple[int, int]) -> Tuple[int, int]:
        w, h = map(float, original_size)
        w, h = max((h * self.output_ratio, h), (w, w / self.output_ratio))

        if isinstance(self.min_padding, int):
            w, h = map(lambda x: x + self.min_padding, (w, h))
        elif isinstance(self.min_padding, float):
            w, h = map(lambda x: x * (1 + self.min_padding), (w, h))
        else:
            raise ValueError()

        return tuple(map(round, (w, h)))

    def _scale_and_crop(self, img: Image, target_size: Tuple[int, int]) -> Image:
        scale_rate = max(lambda a, b: a / b, zip(img.size, target_size))
        new_size = tuple(round(x * scale_rate) for x in img.size)
        left, upper = map(lambda a, b: (a - b) // 2, zip(new_size, target_size))
        return ret.resize(new_size).crop(left, upper, left + target_size[0], upper + target_size[1])

    def __call__(self, img: Image, background_img: Image) -> Image:
        bg_size = self._define_output_size(img.size)
        output_img = background_img.resize(bg_size)

        output_w, output_h = output_img.size

        left, upper = output_w // 2 - img.size[0] // 2, output_h // 2 - img.size[1] // 2

        output_img.paste(img, box=(left, upper))

        if self.fixed_output_resolution is not None:
            output_img.resize(self.output_resolution)
        return output_img


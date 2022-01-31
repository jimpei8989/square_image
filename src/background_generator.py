from typing import Union
from PIL import Image, ImageFilter

class BackgroundGenerator:
    def __init__(self, args):
        self.method = None
        self.args = {}

        if args.method == "color":
            self.func = self.gen_color_background
            self.args["color"] = args.color
        elif args.method == "blur":
            self.func = self.gen_blurred_background
            self.args["blur_radius"] = args.blur_radius
            assert isinstance(args.blur_radius, int) or 0 <= args.blur_radius <= 1
        else:
            raise ValueError(
                "Unsupported method. Supported methods are color,"
                "blur..."
            )

    def __call__(self, img: Image) -> Image:
        return self.func(img, **self.args)

    @staticmethod
    def gen_color_background(
        img: Image,
        color = 0,  # set the default value to zero since None is invalid
    ) -> Image:
        return Image.new("RGB", img.size, color)

    @staticmethod
    def gen_blurred_background(img: Image, blur_radius: Union[int, float]) -> Image:
        def _calc_radius():
            return blur_radius if isinstance(blur_radius, int) else max(img.size) * blur_radius
        return img.filter(ImageFilter.GaussianBlur(radius=_calc_radius()))


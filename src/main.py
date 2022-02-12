#!/usr/env/bin python3

import re
from argparse import ArgumentParser
from pathlib import Path
from PIL import Image
from PIL.ImageColor import getrgb

from square_image import Wrapper

PERCENTAGE_PATTERN_STR = "^([0-9]*[.])?[0-9]+%$"
PERCENTAGE_PATTERN = re.compile(PERCENTAGE_PATTERN_STR)

INTEGER_PATTERN_STR = "^[0-9]+$"
INTEGER_PATTERN = re.compile(INTEGER_PATTERN_STR)

RATIO_PATTERN_STR = "^[0-9]+:[0-9]+$"
RATIO_PATTERN = re.compile(RATIO_PATTERN_STR)

def parse_args():
    def parse_percentage(input_str: str):
        if re.match(PERCENTAGE_PATTERN, input_str) is not None:
            return float(input_str[:-1]) / 100
        return None

    def parse_int(input_str: str):
        if re.match(INTEGER_PATTERN, input_str) is not None:
            return int(input_str)
        return None

    def parse_int_or_percent(input_str: str):
        if (ret := parse_percentage(input_str)) is not None:
            return ret
        elif (ret := parse_int(input_str)) is not None:
            return ret
        else:
            raise ValueError(f"Cannot parse padding {input_str}")

    def parse_ratio(input_str: str) -> float:
        if re.match(RATIO_PATTERN, input_str) is not None:
            a, b = map(float, input_str.split(":"))
            if any(x == 0 for x in [a, b]):
                raise ValueError("Ratio cannot be zeros")
            return a / b
        else:
            raise ValueError(f"Cannot parse ratio {input_str}")
            
    parser = ArgumentParser()
    parser.add_argument("task", choices=("single", "batch"))

    parser.add_argument("-s", "--show_image", action="store_true")
    parser.add_argument("-i", "--input_path", type=Path, required=True)
    parser.add_argument("-o", "--output_path", type=Path)

    # Background
    parser.add_argument("-m", "--method", choices=("color", "blur"), default="blur")
    parser.add_argument("-c", "--color", type=getrgb)
    parser.add_argument("-r", "--blur_radius", type=parse_int_or_percent, default=0.1)

    # Image
    parser.add_argument("--min_padding", type=parse_int_or_percent, default=0)
    parser.add_argument("--max_padding", type=parse_int_or_percent, default=0)
    parser.add_argument("--output_ratio", type=parse_ratio, default=1.0)
    parser.add_argument("--fixed_output_resolution", type=int, nargs=2)

    return parser.parse_args()

def main(args):
    wrapper = Wrapper(args)

    if args.task == "single":
        if args.output_path is not None and args.output_path.exists():
            res = input(f"W - Output path {args.output_path} exists... overwrite? (y/n) ")
            if res != "y":
                exit(1)
        wrapper.process_single(args.input_path, args.output_path)

    elif args.task == "batch":
        if not args.input_path.is_dir():
            raise FileNotFoundError("E - input_dir is not a directory")

        if not args.output_path.exists():
            print(f"I - Creating dir for output dir {args.output_path}...")
            args.output_path.mkdir(parents=True)
        elif args.output_path.is_dir():
            print(f"W - {args.output_path} exists")
        else:
            raise ValueError("E - Output dir {output_dir} is not a directory, aborting...")
        wrapper.process_batch(args.input_path, args.output_path)

main(parse_args())


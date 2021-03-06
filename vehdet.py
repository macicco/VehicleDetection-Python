#!/usr/bin/env python
"""
OpenCV Python program to detect cars in video frame

https://docs.opencv.org/3.4.2/d1/de5/classcv_1_1CascadeClassifier.html
"""
from argparse import ArgumentParser
import vehicledetection as vdet
from pathlib import Path

R = Path(__file__).parent


def main():
    p = ArgumentParser()
    p.add_argument('fn', help='filename or camera device handle')
    p.add_argument('-train', help='training data', default=R/'data/cars.xml')
    p.add_argument('-v', '--verbose', help='show video preview', action='store_true')
    p.add_argument('-r', '--resolution', help='image width x height', type=int, nargs=2, default=(640, 480))
    p.add_argument('-o', '--outdir', help='directory to write previews to (slow!)')
    p = p.parse_args()

    vdet.carcascade(p.fn, p.outdir, p.train, p.resolution, p.verbose)


if __name__ == '__main__':
    main()

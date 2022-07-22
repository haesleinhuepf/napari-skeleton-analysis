import numpy as np
from pathlib import Path
from skimage.io import imread

def retina():
    return [(imread(Path(__file__).parent / "600px-Fundus_photograph_of_normal_right_eye.jpg"), {})]
    # Image data source: https://commons.wikimedia.org/wiki/File:Fundus_photograph_of_normal_right_eye.jpg
    # CC0
    #
    # Häggström, Mikael (2014). "Medical gallery of Mikael Häggström 2014". WikiJournal of Medicine 1 (2). DOI:10.15347/wjm/2014.008. ISSN 2002-4436. Public Domain.


def retina_binary():
    return [(imread(Path(__file__).parent / "600px-Fundus_photograph_of_normal_right_eye_binarized.tif"), {}, 'labels')]


def retina_skeleton():
    return [(imread(Path(__file__).parent / "600px-Fundus_photograph_of_normal_right_eye_skeletonized.tif"), {}, 'labels')]

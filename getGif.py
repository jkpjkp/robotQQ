import cv2  # pip install opencv-python # 图像处理库
import glob  # 导入文件处理库
import argparse  # 命令行解析库
import numpy as np  # 数据处理库
from tqdm import tqdm  # 导入进度条库
from itertools import product  # 导入迭代器库
import logging  # 导入日志库
import imageio
from datetime import datetime

from getImg import getImg

logger = logging.getLogger("GIF合成器")


def generateGif(num, downPath):
    paths = getImg(num, True, downPath)
    gif_image = []
    for path in paths:
        gif_image.append(imageio.imread(path))
    gif_path = downPath + datetime.now().strftime("%Y%m%d%H%M%S") + '.gif'
    imageio.mimsave(gif_path, gif_image, fps=1)

if __name__ == '__main__':
    generateGif(10, 'F:/img2/')

# coding: utf-8
from win32gui import *
import win32gui
import win32api
import win32con
import time
import pygame
import imagehash
from PIL import Image, ImageGrab
import sys
import os
from config import game

pygame.init()
titles = set()


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


'''
version:0.1
功能1：单个本自定义刷次数（例子：某个本 5次）
功能2（待加入）：多个本自定义刷次数（例子：0-2 5次 -> 1.7 15次...）
'''

if __name__ == '__main__':
    ce_path = resource_path(os.path.join("src", 'c.png'))
    start_path = resource_path(os.path.join("src", 'start.png'))
    now1_end_path = resource_path(os.path.join("src", 'now1.png'))
    exp_path = resource_path(os.path.join("src", 'exp.png'))
    now2_end_path = resource_path(os.path.join("src", 'now2.png'))

    while True:
        print("鲨鲨代理为你服务...")
        k = eval(input("是否开始，开始请扣1，结束扣0: \n"))
        if k == 1:
            n = eval(input("请输入代理次数: \n"))
            game(n, ce_path, start_path, now1_end_path, exp_path, now2_end_path)
        else:
            break

# coding: utf-8
import sys
from win32gui import *
import win32gui
import win32api
import win32con
import time
import pygame
import imagehash
from PIL import Image, ImageGrab
import random
import os

pygame.init()
titles = set()


def r():
    return random.random() / 10


def foo(hwnd, mouse):
    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
        titles.add(GetWindowText(hwnd))


def play_game(start_path):
    global titles
    EnumWindows(foo, 0)
    wins = [t for t in titles if t]
    height = 600
    weight = 900
    # print(wins)
    for NAME in wins:
        if "MuMu模拟器" in NAME and "明日方舟" in NAME:
            print("  | {} |关联窗口".format(NAME))
            hwnd = win32gui.FindWindow(None, NAME)
            # win32gui.SetForegroundWindow(hwnd)
            # win32gui.SetWindowPos(hwnd)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                                  0, 0, weight, height,
                                  win32con.SWP_SHOWWINDOW)
            size = win32gui.GetWindowRect(hwnd)
            ImageGrab.grab((730, 480, 875, 515)).save(start_path)
            return size, NAME


def mouse_click(x, y):
    win32api.SetCursorPos([x, y])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def game(n, ce_path, start_path, now1_end_path, exp_path, now2_end_path):
    size, name = play_game(start_path)
    print("锁定窗口：", size)

    hash_start = imagehash.average_hash(Image.open(start_path), hash_size=6)
    time.sleep(1 + r())

    ImageGrab.grab((730, 480, 875, 515)).save(ce_path)
    hash_c = imagehash.average_hash(Image.open(ce_path), hash_size=6)
    # if abs(hash_c - hash_start) >= 1:
    #     print("请调试初始状况，存在某些问题！模拟器界面：1280*720")

    window = win32gui.FindWindow(0, name)
    win32gui.ShowWindow(window, win32con.SW_SHOW)
    ImageGrab.grab((730, 480, 875, 515)).save(now1_end_path)
    hash_now1 = imagehash.average_hash(Image.open(now1_end_path), hash_size=6)
    hash_exp = imagehash.average_hash(Image.open(exp_path), hash_size=6)

    number = 1
    while 1 - (hash_now1 - hash_start):
        print("第{}次代理开始...".format(number), " ", end="")
        time.sleep(1 + r())
        mouse_click(800, 500)
        time.sleep(2 + r())
        mouse_click(780, 400)
        time.sleep(36 + r())  # 可修复优化
        while True:
            ImageGrab.grab((345, 400, 445, 470)).save(now2_end_path)
            hash_now2 = imagehash.average_hash(Image.open(now2_end_path), hash_size=6)
            print("测试判断偏差：{}".format(hash_now2 - hash_exp))
            if abs(hash_now2 - hash_exp) <= 5:
                time.sleep(2 + r())
                mouse_click(500, 300)
                time.sleep(3 + r())  # 优化
                break
            else:
                time.sleep(1 + r())
                continue
        if number == n:
            break
        number += 1
        print("代理结束，正在启动下次...")
    print("代理结束了哦，感谢使用！")

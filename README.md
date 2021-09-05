# shasha-agent
Arknights agent script

利用hash图像匹配，简单的制作一个明日方舟【MuMu模拟器】的代理作战脚本。（等效于高级连点器<3)

如果你想直接使用exe（Windows下）
从这里下载
链接：https://pan.baidu.com/s/19sY-dS2G-co5dK7at5fONA 
提取码：niqo 

### 前言

首先简单介绍一些，游戏内部刷同一个关卡，例如1-7满疲劳刷完需要刷很多次，有没有简单的代理方式呢，一种是可以做一个连点器记录然后挂着，学习了计算机视觉，于是考虑写个小脚本来代替连点器。最后功能是没问题的，还有一些地方可以优化，如果可以让按键功能挂后台的话，体验会更好，因为你不会担心鼠标干别的事情突然被抢走<3

### 代码实现+原理

1. **用到的包**

```python
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
```

2. 流程

首先将模拟器固定大小并窗口置顶，通过截取部分画面来和资源图片去做hash匹配，如果匹配程度大于某个值阈值，认定匹配，然后通过pygame去让鼠标触发某些事件。为了防止物理检测到每次点击间隔相同，对于每一次鼠标的触发插入了随机帧，让它看起来比较自然。[虽然我并不认为它有这种检测功能]

3. 代码实现

**定义随机帧**

```python
def r():
    return random.random() / 10
```

**窗口初始操作**

```python
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
```

如果MuMu模拟器在进程中，而且明日方舟运行中，将窗口置顶并固定大小。

**主干操作**

```python
def game(n, ce_path, start_path, now1_end_path, exp_path, now2_end_path):
    size, name = play_game(start_path)
    print("锁定窗口：", size)

    hash_start = imagehash.average_hash(Image.open(start_path), hash_size=6)
    time.sleep(1 + r())

    ImageGrab.grab((730, 480, 875, 515)).save(ce_path)
    hash_c = imagehash.average_hash(Image.open(ce_path), hash_size=6)

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
```

具体什么图像匹配成功触发鼠标的什么操作。

中间加入了一些文本提示。


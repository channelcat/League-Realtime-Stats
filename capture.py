#!/usr/bin/python
# -*- coding: <encoding name> -*-

import win32gui

from PIL import ImageGrab


class Screenshot():
    width = None
    height = None
    image = None
    data = None
    def __init__(self, image):
        self.image = image
        self.width, self.height = image.size
        self.data = image.getdata()
    def pixel(self, x,y):
        return self.data[y*self.width+x]

def screenshot_image(hwnd = None, number = ''):
    if not hwnd:
        hwnd=win32gui.GetDesktopWindow()

    #bbox = win32gui.GetWindowRect(hwnd)
    window_box = win32gui.GetClientRect(hwnd)
    screen_box = win32gui.ClientToScreen(hwnd, window_box[0:2]) + win32gui.ClientToScreen(hwnd, window_box[2:4])

    image = ImageGrab.grab(screen_box)

    return image

def get_windows_bytitle(title_text, exact = False):
    def _window_callback(hwnd, all_windows):
        all_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    windows = []
    win32gui.EnumWindows(_window_callback, windows)

    if exact:
        return [hwnd for hwnd, title in windows if title_text == title]
    else:
        return [hwnd for hwnd, title in windows if title_text.lower() in title.lower()]


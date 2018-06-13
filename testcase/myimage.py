# -*- coding: utf-8 -*-
'''
Created on 2018.4.23
@author: Cindy
图片处理相关
'''

from PIL import Image, ImageGrab

def screenshot(imagefile):
    '''截取整个屏幕图片并保存到imagefile'''
    image = ImageGrab.grab()
    return image.save(imagefile)


def screenshot_by_size(imagefile,x1,y1,x2,y2):
    '''截取x1,y1到x2,y2坐标范围内的屏幕图片并保存到imagefile'''
    image = ImageGrab.grab((x1,y1,x2,y2))
    return image.save(imagefile)



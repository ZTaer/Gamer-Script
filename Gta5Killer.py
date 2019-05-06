#!/usr/bin/python3
#-*- coding:utf-8 -*-

# a)检测按键需要
import win32api as wapi
import time

# b)执行按键
import ctypes
import time

# 声音提示模块
import winsound

# 程序退出
import sys


# 按键仓库-BGN
SendInput = ctypes.windll.user32.SendInput
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20

M = 0x32
R = 0x13
T = 0x14
C = 0x2E

O1 = 0x02
O2 = 0x03
O3 = 0x04
O4 = 0x05
O5 = 0x06
O6 = 0x07
O7 = 0x08
O8 = 0x09
O9 = 0x0A
O0 = 0x0B

UP = 0xC8
LEFT = 0xCB
RIGHT = 0xCD
DOWN = 0xD0

CAPITAL = 0x3A
ENT = 0x1C

# 按键仓库-END

# a)获取键盘按键-BGN
keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890,.'£$/\\":
    keyList.append(char)


def key_check():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys
# a)获取键盘-END

# b)执行按键-BGN
# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def set_pos(x, y):
    x = 1 + int(x * 65536./1920.)
    y = 1 + int(y * 65536./1080.)
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(x, y, 0, (0x0001 | 0x8000), 0, ctypes.pointer(extra))
    command = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))

def left_click():
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    time.sleep(0.3) # 按驻鼠标左键3秒

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, 0x0004, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# b)执行按键-END

# c)功能调试区域-BGN

# 0. -G- 火箭筒快速发射
def t_rpg():
    PressKey(O5)
    time.sleep(0.2)
    ReleaseKey(O5)

    PressKey(O4)
    time.sleep(0.2)
    ReleaseKey(O4)

    left_click()

    PressKey(O5)
    time.sleep(0.2)
    ReleaseKey(O5)

    PressKey(O4)
    time.sleep(0.2)
    ReleaseKey(O4)

    left_click()

#   1. -K- 秒自杀
def suicide():
    PressKey(M)
    time.sleep(0.2)
    ReleaseKey(M)

    PressKey(UP)
    time.sleep(0.2)
    ReleaseKey(UP)

    PressKey(UP)
    time.sleep(0.2)
    ReleaseKey(UP)

    PressKey(C)
    time.sleep(0.2)
    PressKey(CAPITAL)
    time.sleep(0.2)
    ReleaseKey(CAPITAL)
    PressKey(ENT)
    time.sleep(0.2)
    ReleaseKey(C)
    ReleaseKey(ENT)

#   2. -R- 快速换巴雷特子弹
def r_gun_reset():
    PressKey(O5)
    time.sleep(0.2)
    ReleaseKey(O5)

    PressKey(O9)
    time.sleep(0.2)
    ReleaseKey(O9)

door = False
#   开启CEO隐匿
#   如果是door为false
#       否则,memory值传入时间验证器
#           验证时间(单独书写模块):
#               获取nowhor/nowmin当前系统小时/分钟
#               如果小时相等则分钟相减result>8则返回true
#               如果小时相减等1,则60 - memory的分钟+ 当前分钟数 result> 8是则返回true
#                   否则响应结果次数报警并且返回false
#   是: 开启隐匿,door = True,memory存入当前时间

#   获取当前时间
def cooling_time():
    localtime = time.localtime(time.time())
    nowHur = localtime[3]
    nowMin = localtime[4]
    return (nowHur,nowMin)



# c)功能调试区域-END

#   #   功能构思:
# 用法:
#   0. -KS- 开启功能
#   1. -JS- 关闭功能
#   2. -TC- 退出程序

# 功能:
#   0. -G- 火箭筒快速发射
#   1. -K- 秒自杀
#   2. -R- 快速换巴雷特子弹
#   3. -X- 秒吃CEO药品
#   4. -B- 秒购买护甲
#   5. -0- 秒购买火箭筒子弹
#   6. -CEO-
#   --- 冷却时间不够将不执行,后台计入时间,单位为分钟,差几分钟响应几声报警声 ---
#   7. -CYN- CEO隐匿   ( 3分钟 - 冷却5分钟 )
#   8. -LYN- 莱斯特隐匿 ( 1分钟 - 冷却5分钟 )
#
#   获取时间 import time
#   localtime = time.localtime(time.time())
#   localtime[4] = 分钟数

if __name__ == "__main__":
    print("-----欢迎使用OO7的'GTA5_Killer v1.0'撕逼玩家专用程序( 此程序完全免费只供个人研究学习 )")
    print("-----开源地址/更新地址:\n")
    print("---用法:\n--开启功能: 进入游戏同时按下'KS'字母键\n--关闭功能: 游戏中同时按下'JS'字母键\n--退出程序: 先'关闭功能后'同时按下'TC'字母键,即可完全关闭程序\n--提示: \n  ‘开启功能’时会有 1 声提示音\n  ‘关闭功能’时会有 2 声提示音\n  '关闭功能'后输入'KS'依然可以再一次开启功能\n")
    print("---功能:\n -G- 火箭筒快速发射\n -R- 快速换巴雷特子弹\n -X- 秒吃CEO药品( CEO时使用 )\n -B- 秒购买护甲( CEO时使用 )\n -0- 秒购买火箭筒子弹")

    while( True ):
        bgn = False
        keysIng = key_check()
        if( 'K' in keysIng and 'S' in keysIng ):
            bgn = True
            winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
        elif ('T' in keysIng and 'C' in keysIng):
            print("成功退出,欢迎下次使用!")
            time.sleep(2)
            sys.exit()
        else:
            continue
        while(bgn):
            keysIng = key_check()
            if( 'G' in keysIng ):
                t_rpg()
                continue
            elif( 'R' in keysIng ):
                r_gun_reset()
                continue
            elif( 'J' in keysIng and 'S' in keysIng ):
                try:
                    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                except:
                    bgn = False
                bgn = False



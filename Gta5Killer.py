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

    time.sleep(0.3) # 按驻鼠标左键0.3秒

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, 0x0004, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# b)执行按键-END

# c)功能调试区域-BGN

#   快捷输入
def buttonNum( num, keys, times ):
    for i in range(num):
        PressKey(keys)
        time.sleep(times)
        ReleaseKey(keys)
        time.sleep(times)

# 0. -Q- 火箭筒快速发射
def t_rpg():
    buttonNum(1,O5,0.05)
    buttonNum(1,O4, 0.05)

    left_click()
    time.sleep(0.2)

#   1. -K- 秒自杀
def suicide():
    buttonNum(1, M, 0.1)
    buttonNum(2, UP, 0.05)

    PressKey(C)
    time.sleep(0.035)
    PressKey(CAPITAL)
    PressKey(ENT)
    time.sleep(0.035)
    ReleaseKey(ENT)
    ReleaseKey(CAPITAL)
    ReleaseKey(C)

#   2. -R- 快速换巴雷特子弹
def r_gun_reset():
    buttonNum(1,O5,0.05)
    buttonNum(1,O9, 0.05)
    left_click()
    time.sleep(0.15)

#   3. -N- 非CEO秒购买对应武器子弹
def rock_buy():
    buttonNum(1, M, 0.1)
    buttonNum(1, DOWN, 0.05)
    buttonNum(1, ENT, 0.1)
    buttonNum(3, DOWN, 0.05)
    buttonNum(1, ENT, 0.1)
    buttonNum(1, UP, 0.05)
    buttonNum(1, ENT, 0.1)
    buttonNum(1, M, 0.1)

#   3. -N- CEO秒购买对应武器子弹
def ceo_rock_buy():
    buttonNum(1, M, 0.1)
    buttonNum(2, DOWN, 0.05)
    buttonNum(1, ENT, 0.1)
    buttonNum(3, DOWN, 0.05)
    buttonNum(1, ENT, 0.1)
    buttonNum(1, UP, 0.05)
    buttonNum(1, ENT, 0.1)
    buttonNum(1, M, 0.1)

#   4.0 -CEO- 秒开CEO
def ceo_bgn():
    buttonNum(1, M, 0.1)
    buttonNum(7, DOWN, 0.05)
    buttonNum(3, ENT, 0.1)

#   4.1 -CEO- 秒关CEO
def ceo_end():
    buttonNum(1, M, 0.1)
    buttonNum(1, ENT, 0.1)
    buttonNum(1, UP, 0.05)
    buttonNum(2, ENT, 0.1)

#   5. -X- 秒吃CEO药品
def ceo_eat_medicine():
    buttonNum(1, M, 0.1)
    buttonNum(1, ENT, 0.1)
    buttonNum(3, UP, 0.05)
    buttonNum(1, ENT, 0.1)
    buttonNum(1, DOWN, 0.05)
    buttonNum(1, ENT, 0.1)

#   6. -0- 秒购买护甲
def ceo_buy_armor():
    buttonNum(1, M, 0.1)
    buttonNum(1, ENT, 0.1)
    buttonNum(3, UP, 0.05)
    buttonNum(1, ENT, 0.1)
    buttonNum(3, DOWN, 0.05)
    buttonNum(1, ENT, 0.1)

#   7. -CH- CEO隐匿
def ceo_hiden():
    buttonNum(1, M, 0.1)
    buttonNum(1, ENT, 0.1)
    buttonNum(3, UP, 0.05)
    buttonNum(1, ENT, 0.1)
    buttonNum(3, UP, 0.05)
    buttonNum(1, ENT, 0.1)

#   8. -秒开摩托帮
def mtb_bgn():
    buttonNum(1, M, 0.1)
    buttonNum(8, DOWN, 0.05)
    buttonNum(3, ENT, 0.1)

#   8. -秒关摩托帮
def mtb_end():
    buttonNum(1, M, 0.1)
    buttonNum(1, ENT, 0.1)
    buttonNum(1, UP, 0.05)
    buttonNum(2, ENT, 0.1)

#   9. -BJ- 快速呼叫摩托( 停留在菜单页面 )
def mtb_car():
    buttonNum(1, M, 0.1)
    buttonNum(1, ENT, 0.1)

#   10.-FJ-快速呼叫飞机( 停留在菜单没页面 )
def airport():
    buttonNum(1, M, 0.1)
    buttonNum(3, DOWN, 0.05)
    buttonNum(1, ENT, 0.1)
    buttonNum(1, DOWN, 0.05)

def airport_mtb():
    buttonNum(1, M, 0.1)
    buttonNum(4, DOWN, 0.05)
    buttonNum(1, ENT, 0.1)
    buttonNum(1, DOWN, 0.05)


# c)功能调试区域-END

#   #   功能构思:
# 用法:
#   0. -KS- 开启功能
#   1. -JS- 关闭功能
#   2. -TC- 退出程序

#   --v1.0目前版本
# 功能:
#   0. -Q- 火箭筒快速发射
#   1. -K- 秒自杀
#   2. -R- 快速换巴雷特子弹( 连续按R键也可以快速使用巴雷特开枪 )
#   3. -N- 秒购买对应武器子弹( 自动切换非CEO/CEO购买模式 )

#   4. -CEO- 秒开/关CEO( 5~7功能只有在CEO模式下才能执行，及时你是摩托帮也可以直接开启CEO )
#   5. -X- 秒吃CEO药品
#   6. -0- 秒购买护甲
#   7. -CH- CEO隐匿( 3分钟 - 冷却5分钟 )

#   --v2.0更新内容
#   8. -BJ- 秒开/关摩托帮( 即使你是CEO也可以直接开启摩托帮 )
#   9. -BJ- 快速呼叫摩托( 停留在菜单页面 )
#   10.-FJ-快速呼叫飞机( 停留在菜单没页面 )

if __name__ == "__main__":
    print("\
\n\
#   GTA5Killer v2.1( 撕逼玩家专用线上模式 )\n\
#   作者: __OO7__ ( 反馈意见给作者: QQ - 1069798804 )\n\
#   作者更新链接及开源链接: https://github.com/ZTaer/GTA5_Killer\n\
#   注意: 此程序仅供个人研究学习,恶意使用本程序造成游戏破坏,作者将不承担任何法律责任( 依然执行本程序代表你已同意此协议! )\n\
#   注意: 此程序完全免费,如果想获得最新版本可以访问上方GitHub链接\n\
#   注意: 如果你有什么更好的改进意见可以联系上放作者QQ( 加好友留言时输入: GTA5KillerUser )\n\
#   注意: 开启功能时,必须要'非CEO/摩托帮'状态,并且要使用本程序功能键来开启/关闭'CEO/摩托帮',否则将无法有效检测是否为CEO/摩托帮状态\n\
    \n\
# 用法:\n\
#   0. -KS- 开启功能( 进入游戏中输入即可 )\n\
#   1. -JS- 结束功能( 结束功能后,再次输入KS依然可以开启功能 )\n\
#   2. -TC- 退出程序\n\
    \n\
# 功能:\n\
#   0. -Q- 火箭筒快速发射\n\
#   1. -K- 秒自杀\n\
#   2. -R- 快速换巴雷特子弹( 连续按R键也可以快速使用巴雷特开枪 )\n\
#   3. -N- 秒购买对应武器子弹( 自动切换非CEO/CEO购买模式 )\n\
    \n\
#   4. -CEO- 秒开/关CEO( 5~7功能只有在CEO模式下才能执行，即使你是摩托帮也可以直接开启CEO )\n\
#   5. -X- 秒吃CEO药品\n\
#   6. -0- 秒购买护甲\n\
#   7. -CH- CEO隐匿( 3分钟 - 冷却5分钟 )\n\
    \n\
#   8. -BJ- 快速呼叫摩托( 即使你是CEO也可以直接开启摩托帮，停留在呼叫菜单页面 )\n\
#   9. -FJ-快速呼叫飞机( 停留在菜单页面 )"\
        )
    print("\n!!!开启成功 - OPEN SUCCESSFULLY!!!( 注意: 直接进入游戏,不要关闭本窗口,最小化即可 )")
    while( True ):
        ceoNum = 0  # ceo开启关闭开关
        mtbNum = 0 # mtb开关
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
            if( 'Q' in keysIng ):
                t_rpg()
                continue
            elif( 'K' in keysIng ):
                suicide()
                continue
            elif( 'R' in keysIng ):
                r_gun_reset()
                continue
            elif( 'N' in keysIng ):
                if( ceoNum or mtbNum ):
                    ceo_rock_buy()
                else:
                    rock_buy()
                continue
            elif ('C' in keysIng and 'E' in keysIng and 'O' in keysIng ):
                if(not ceoNum and mtbNum):
                    mtb_end()
                    mtbNum = 0
                    ceo_bgn()
                    ceoNum = 1
                    continue
                elif(not ceoNum and not mtbNum ):
                    ceo_bgn()
                    ceoNum = 1
                    continue
                else:
                    ceo_end()
                    ceoNum = 0
                    continue
            elif ( 'X' in keysIng and ceoNum ):
                ceo_eat_medicine()
                continue
            elif ('0' in keysIng and ceoNum):
                ceo_buy_armor()
                continue
            elif ('C' in keysIng and 'H' in keysIng and ceoNum):
                ceo_hiden()
                continue
            elif ('B' in keysIng and 'J' in keysIng ):
                if(not mtbNum and ceoNum):
                    ceo_end()
                    ceoNum = 0
                    mtb_bgn()
                    mtb_car()
                    mtbNum = 1
                    continue
                elif(not mtbNum and not ceoNum ):
                    mtb_bgn()
                    mtb_car()
                    mtbNum = 1
                    continue
                else:
                    mtb_end()
                    mtbNum = 0
                    continue
            elif ('F' in keysIng and 'J' in keysIng):
                if(mtbNum or ceoNum):
                    airport_mtb()
                    continue
                else:
                    airport()
                    continue

            elif( 'J' in keysIng and 'S' in keysIng ):
                if(ceoNum):
                    ceo_end()
                    ceoNum = 0
                    continue
                try:
                    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                except:
                    bgn = False
                bgn = False



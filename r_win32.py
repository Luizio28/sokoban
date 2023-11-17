import ctypes
from ctypes import *

renderer_gHandle = ctypes.windll.kernel32.GetStdHandle(c_long(-11))

def setcursor (y, x):
   value = x + (y << 16)
   ctypes.windll.kernel32.SetConsoleCursorPosition(renderer_gHandle, c_ulong(value))

def drawglyph(i,j,string):
    setcursor(i,j)
    ctypes.windll.kernel32.WriteConsoleW(renderer_gHandle, c_wchar_p(string), c_ulong(len(string)), c_void_p(), None)

#this bit i got from nneonneo at stackoverflow   
class CONSOLE_CURSOR_INFO(Structure):
    _fields_ = [('dwSize', c_int),
                ('bVisible', c_int)]
STD_OUTPUT_HANDLE = -11

hStdOut = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
cursorInfo = CONSOLE_CURSOR_INFO()

def console_cursor(a):
    if a == "hide":
        cursorInfo.dwSize = 1
        cursorInfo.bVisible = 0
        windll.kernel32.SetConsoleCursorInfo(hStdOut, byref(cursorInfo))
    if a == "show":
        cursorInfo.dwSize = 1
        cursorInfo.bVisible = 1
        windll.kernel32.SetConsoleCursorInfo(hStdOut, byref(cursorInfo))
        
def print_line(i,j,string: str,k):
    drawglyph(i,j,string+" "*(k-len(list(string))))
import keyboard  #监听键盘
import time


keyboard.add_hotkey('ctrl', print, args=('aaa',))
recorded = keyboard.record(until='esc')
print(recorded)
# def abc():
#     if keyboard.wait(hotkey='shift') == None:

#         if keyboard.wait(hotkey='shift') == None:

#             print("运行程序！")


# abc()
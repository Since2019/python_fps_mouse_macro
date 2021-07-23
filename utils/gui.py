
import tkinter
from tkinter import Listbox
root = tkinter.Tk()
root.wm_attributes('-topmost', 1)


li = ['C', 'python', 'php', 'html', 'SQL', 'java']

list = Listbox(root)      # 创建两个列表组件
for item in li:           # 第一个小部件插入数据
    list.insert(0, item)

list.pack()

# 进入消息循环
root.mainloop()

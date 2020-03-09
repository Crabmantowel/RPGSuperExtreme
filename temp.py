# from tkinter import *
# root = Tk()
#
#
# def getV(root):
#     a = scale1.get()
#     print("Значение", a)
#
#
# scale1 = Scale(root, orient=HORIZONTAL, length=300, from_=50, to=80, tickinterval=5,
#                resolution=5)
# button1 = Button(root, text=u"Получить значение")
# scale1.pack()
# button1.pack()
# button1.bind("<Button-1>", getV)
# root.mainloop()

# import tkinter as tk
#
# window = tk.Tk()
# window.title('My Window')
#
# window.geometry('500x300')
#
# var1 = tk.StringVar()
# l = tk.Label(window, bg='green', fg='yellow',font=('Arial', 12), width=10, textvariable=var1)
# l.pack()
#
# def print_selection():
#     value = lb.get(lb.curselection())
#     var1.set(value)
#
# b1 = tk.Button(window, text='print selection', width=15, height=2, command=print_selection)
# b1.pack()
#
# var2 = tk.StringVar()
# var2.set((1,2,3,4))
# lb = tk.Listbox(window, listvariable=var2)
#
# list_items = [11,22,33,44]
# for item in list_items:
#     lb.insert('end', item)
# lb.insert(1, 'first')
# lb.insert(2, 'second')
# lb.delete(2)
# lb.pack()
#
# window.mainloop()


# from tkinter import Tk, BOTH, IntVar, LEFT
# from tkinter.ttk import Frame, Label, Scale, Style
#
# class Example(Frame):
#
#     def __init__(self):
#         super().__init__()
#
#         self.initUI()
#
#
#     def initUI(self):
#
#         self.master.title("Scale")
#         self.style = Style()
#         self.style.theme_use("default")
#
#         self.pack(fill=BOTH, expand=1)
#
#         scale = Scale(self, from_=0, to=100,
#             command=self.onScale)
#         scale.pack(side=LEFT, padx=15)
#
#         self.var = IntVar()
#         self.label = Label(self, text=0, textvariable=self.var)
#         self.label.pack(side=LEFT)
#
#
#     def onScale(self, val):
#
#         v = int(float(val))
#         self.var.set(v)
#
#
# def main():
#
#     root = Tk()
#     ex = Example()
#     root.geometry("250x100+300+300")
#     root.mainloop()
#
#
# if __name__ == '__main__':
#     main()

from tkinter import *
master = Tk()
scales=list()
Nscales=10
for i in range(Nscales):
    w=Scale(master, from_=0, to=100) # creates widget
    w.pack(side=RIGHT) # packs widget
    scales.append(w) # stores widget in scales list
def read_scales():
    for i in range(Nscales):
        print("Scale %d has value %d" %(i,scales[i].get()))
b=Button(master,text="Read",command=read_scales) # button to read values
b.pack(side=RIGHT)
mainloop()

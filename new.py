from Tkinter import *
import ttk

root = Tk()
note = ttk.Notebook(root)

b = Button(root, text="OK")
b.pack()

tab1 = Frame(note)
tab2 = Frame(note)
tab3 = Frame(note)
Button(root, text='Exit', command=root.destroy)

note.add(tab1, text = "Tab One")
note.add(tab2, text = "Tab Two")
note.add(tab3, text = "Tab Three")

root.mainloop()

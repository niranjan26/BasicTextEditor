from Tkinter import *
from tkFileDialog import *
import ttk
filename = None
class Notebook(Frame):
    def __init__(self, parent, activerelief = SOLID, inactiverelief = SOLID, xpad = 4, ypad = 4, activefg = 'black',activebg='green',inactivebg='grey',bd=1,inactivefg = 'black', **kw):                                                                
        self.activefg = activefg
        self.activebg=activebg
        self.bd=bd
        self.inactivebg=inactivebg
        self.inactivefg = inactivefg
        self.deletedTabs = []        
        self.xpad = xpad
        self.ypad = ypad
        self.activerelief = activerelief
        self.inactiverelief = inactiverelief                                               
        self.kwargs = kw                                                                   
        self.tabVars = {}                                                                 
        self.tabs = 0                                                                                                                                                 
        self.noteBookFrame = Frame(parent)                                                 
        self.BFrame = Frame(self.noteBookFrame)                                            
        self.noteBook = Frame(self.noteBookFrame, relief = RAISED, bd = 1, **kw)           
        self.noteBook.grid_propagate(0)                                                    
        Frame.__init__(self)
        self.noteBookFrame.grid()
        self.BFrame.grid(row =0, sticky = W)
        self.noteBook.grid(row = 1, column = 0, columnspan = 27)

    def add_tab(self, width = 1, **kw):            
            temp = self.tabs                                                                   
            self.tabVars[self.tabs] = [Label(self.BFrame, relief = RIDGE, **kw)]               
            self.tabVars[self.tabs][0].bind("<Button-1>", lambda Event:self.change_tab(temp))  
            self.tabVars[self.tabs][0].pack(side = LEFT, ipady = self.ypad, ipadx = self.xpad) 
            self.tabVars[self.tabs].append(Frame(self.noteBook, **self.kwargs))                
            self.tabVars[self.tabs][1].grid(row = 0, column = 0)                               
            self.change_tab(0)                                                                 
            self.tabs += 1                                                                     
            return self.tabVars[temp][1]
    def change_tab(self, IDNum): 
        for i in (a for a in range(0, len(self.tabVars.keys()))):
            if not i in self.deletedTabs:                                                  
                if i <> IDNum:                                                             
                    self.tabVars[i][1].grid_remove()                                       
                    self.tabVars[i][0]['relief'] = self.inactiverelief                     
                    self.tabVars[i][0]['fg'] = self.inactivefg
                    self.tabVars[i][0]['bg'] = self.inactivebg
                    self.tabVars[i][0]['bd'] = self.bd
                else:                                                                      
                    self.tabVars[i][1].grid()                                                                    
                    self.tabVars[IDNum][0]['relief'] = self.activerelief                   
                    self.tabVars[i][0]['fg'] = self.activefg
                    self.tabVars[i][0]['bg'] = self.activebg
                    self.tabVars[i][0]['bd'] = self.bd
#Function for creating a new file
def newFile():
	textnew = Text(root, width=400, height=400 , undo = True)
	global filename
	filename = "Untitled"
	text.delete(0.0, END)

#Function for saving a file
def saveFile():
	global filename
	t = text.get(0.0, END)
	f = open(filename, 'w')
	f.write(t)
	f.close()

#Function for saving a new file as 
def saveAs():
	f = asksaveasfile(mode='w',defaultextension='.txt')
	t = text.get(0.0, END)
	try:
		f.write(t.rstrip())
	except:
		showerror(title="Oops!", message="Unable to save file...!")

#Function for opening an existing file
def  openFile():
	f = askopenfile(mode='r')
	t = f.read()
	text.delete(0.0, END)
	text.insert(0.0, t)

#Function for Undo
def undo(root, event=None):
    if root.steps != 0:
        root.steps -= 1
        root.delete(0, END)
        root.insert(END, root.changes[root.steps])


def redo(root, event=None):
	if root.steps < len(root.changes):
		root.delete(0, END)
		root.insert(END, root.changes[root.steps])
		root.steps += 1

#Function for BOLD
def bold():
	text.tag_add('bld', 'SEL_FIRST', 'SEL_LAST')
	text.tag_configure('bld' ,font='helvetica 14 bold')  

	
	

def add_changes(root, event=None):
	if root.get() != root.changes[-1]:
		root.changes.append(root.get())
		root.steps += 1




root=Tk()
root.title("TEXT Editor")
menubar = Menu(root)
#1st drop down menu: File
filemenu = Menu(menubar,tearoff=0)
filemenu.add_command(label="New", command=newFile)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_command(label="Save", command=saveFile)
filemenu.add_command(label="Save As...", command=saveAs)
filemenu.add_separator()
filemenu.add_command(label="Quit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)



note=Notebook(root, width= 400, height =400, activefg = 'red', inactivefg = 'blue')
note.grid()
tab1 = note.add_tab(text = "Tab One")
text = Text(tab1, width=400, height=400 , undo = True)
text.insert('1.0', 'Welcome to the')
text.pack()
tab2 = note.add_tab(text = "Tab Two")
text = Text(tab2, width=400, height=400 , undo = True)
text.insert('1.0', 'Welcome to !')
text.pack()                                                
tab3 = note.add_tab(text = "Tab Three")
text = Text(tab3, width=400, height=400 , undo = True)
text.insert('1.0', 'Welcome to the Textre !!!')
text.pack()
root.config(menu=menubar)
root.mainloop()

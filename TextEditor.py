from Tkinter import *
from tkFileDialog import *
from tkSimpleDialog import askstring

import ttk, tkFileDialog
size=10
filename = "New Text Document"
mainText=""

recent_list=["New Text Document 1","New Text Document 2","New Text Document 3","New Text Document 4"]
FONT_OPTIONS = [
    "Times New Roman", "helvetika", "Calibri"
]

class MyDialog:

    def __init__(self, parent):
	global filename
        top = self.top = Toplevel(parent)
	top.title(filename)
	top.geometry("250x100")
        Label(top, text="\nAre you sure you want to quit ?").pack()

	b3 = Button(top, text="Save First", command=saveAs)
        b3.pack(side=LEFT)
        
	b2 = Button(top, text="Quit", command= self.dest)
        b2.pack(side=LEFT)

	b1 = Button(top, text="Cancel", command=self.ok)
        b1.pack(side=LEFT)
	
    def dest(self):

        root.destroy()

    def ok(self):


        self.top.destroy()

#Function for creating a new file
def newFile():
	textnew = Text(root, width=400, height=400 , undo = True)
	global filename
	global mainText
	filename = "Untitled"
	mainText=""
	text.delete(0.0, END)

#Function for saving a file
def saveFile():
	global filename
	global mainText
	#filename = asksaveasfilename()
	
        if filename:
            alltext = text.get(0.0, END)
	    mainText=alltext
            open(filename, 'w').write(alltext)

#Function for saving a new file as 
def saveAs():
	global mainText
	global filename
	filename = asksaveasfilename()
	global recent_list
	recent_list.pop()
	recentMenu.delete(recent_list[3])
	recent_list= [filename]+recent_list	
	recentMenu.add_command(label=recent_list[0],command=openRecent(0))
	file_recent=open("recent.txt","w+")
	myString = " ".join(recent_list)
	file_recent.write(myString)	
	file_recent.close()
	root.title("TEXT Editor " + filename)
        if filename:
            alltext = text.get(0.0, END)
	    mainText=alltext
            open(filename, 'w').write(alltext)

#Function for opening an existing file
def  openFile():
	global filename
	f = askopenfile(mode='r')
	filename=f.name
	global recent_list
	recent_list.pop()
	recentMenu.delete(recent_list[3])
	recent_list= [filename]+recent_list	
	recentMenu.add_command(label=recent_list[0])
	file_recent=open("recent.txt","w+")
	myString = " ".join(recent_list)
	file_recent.write(myString)	
	file_recent.close()
	root.title("TEXT Editor " + filename)
	t = f.read()
	global mainText
	mainText = t
	text.delete(0.0, END)
	text.insert(0.0, t)

def openRecent(ch):
	global filename
	print recent_list[ch]
	file_handle = open(recent_list[ch],"w+")
	filename= recent_list[ch]
	root.title("TEXT Editor " + filename)
	t = file_handle.read()
	global mainText
	mainText = t
	#text.delete(0.0, END)
	#text.insert(0.0, t)
	

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
	  
	text.tag_add('bt',SEL_FIRST,SEL_LAST)


def onCut():
        textdata = text.get(SEL_FIRST, SEL_LAST)
        text.delete(SEL_FIRST, SEL_LAST)
        root.clipboard_clear()
        root.clipboard_append(textdata)

def onCopy():
        textdata = text.get(SEL_FIRST, SEL_LAST)
        root.clipboard_clear()
        root.clipboard_append(textdata)

def onPaste():
        try:
            textdata = root.selection_get(selection='CLIPBOARD')
            text.insert(INSERT, textdata)
        except TclError:
            pass
#Function for Font INC
def OnBigger():
	global size
	size=size+2
	text.tag_configure('sel' ,font='helvetica %d ' %size)

def OnSmaller():
	global size
	size=size-2
	text.tag_configure('sel' ,font='helvetica %d ' %size) 

def doCheckSave() :
	
	global mainText
	alltext = text.get(0.0, END)
    	if mainText == alltext :
		root.destroy()
     	else :
    		d = MyDialog(root)
		root.wait_window(d.top)
	 
def onFind():
        target = askstring('Find', 'Enter string to search' )
        if target:
            where = text.search(target, INSERT, END)
            if where:
                print where
                pastit = where + ('+%dc' % len(target))
               #self.text.tag_remove(SEL, '1.0', END)
                text.tag_add(SEL, where, pastit)
                text.mark_set(INSERT, pastit)
                text.see(INSERT)
                text.focus()

#Function for Italics

def italic():
	text.tag_configure('sel' ,font='helvetica 14 italic') 	
	

def add_changes(root, event=None):
	if root.get() != root.changes[-1]:
		root.changes.append(root.get())
		root.steps += 1

def changefonts(value):
	if value is FONT_OPTIONS[0] :
		text.tag_configure('sel' ,font='Times')
	elif value is FONT_OPTIONS[1] :
		text.tag_configure('sel' ,font='helvetika')
	elif value is FONT_OPTIONS[2] :
		text.tag_configure('sel' ,font='calibri')


#Creating a T-Kinter object 
root = Tk()
#root.wm_state('iconic')
root.protocol('WM_DELETE_WINDOW', doCheckSave)
pad = 3
size=10
root.title("TEXT Editor " + filename)
root.minsize(width=400, height=400)
root.maxsize(width=root.winfo_screenwidth()-pad,height=root.winfo_screenheight()-pad)
root.bind("<Control-z>",undo)
#root.bind("<Control-y>",redo)
#root.bind("<Key>", add_changes)
#root.steps = int()

#Creating the menu bar
menubar = Menu(root)



#1st drop down menu: File
filemenu = Menu(menubar,tearoff=0)
recentMenu = Menu()
filemenu.add_command(label="New", command=newFile)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_command(label="Save", command=saveFile)
filemenu.add_command(label="Save As...", command=saveAs)
filemenu.add_separator()
filemenu.add_cascade(label="Recent Files",menu=recentMenu)
file_recent=open("recent.txt","r")
recent=file_recent.read()
recent=recent.strip(' ')
recent_list= recent.split(' ')
recentMenu.add_command(label=recent_list[0],command=openRecent(0))
recentMenu.add_command(label=recent_list[1],command=openRecent(0))
recentMenu.add_command(label=recent_list[2],command=openRecent(0))
recentMenu.add_command(label=recent_list[3],command=openRecent(0))

filemenu.add_command(label="Quit", command=doCheckSave)
menubar.add_cascade(label="File", menu=filemenu)
file_recent.close()


#2nd drop down menu: Edit
editmenu = Menu(menubar,tearoff=0)
editmenu.add_command(label="Undo", command=undo)
editmenu.add_command(label="Redo", command=redo)
editmenu.add_separator()
editmenu.add_command(label="Cut", command=onCut)
editmenu.add_command(label="Copy", command=onCopy)
editmenu.add_command(label="Paste", command=onPaste)
menubar.add_cascade(label="Edit", menu=editmenu)


#Creating the toolbar
toolBar = Frame(root,bd=1,relief=RAISED)

#1st button:newFile
pic_new=PhotoImage(file="new.png" )
pic_new=pic_new.subsample(10)
newFileButton = Button(toolBar,relief=FLAT, command = newFile)
newFileButton.config(image=pic_new, compound=RIGHT, height='40',width='40')
newFileButton.pack(side=LEFT)

#2nd button:openFile
pic_open=PhotoImage(file="open.png" )
pic_open=pic_open.subsample(10)
openButton = Button(toolBar,relief=FLAT, command = openFile)
openButton.config(image=pic_open, compound=RIGHT, height='40',width='40')
openButton.pack(side=LEFT)

#3rd button:saveFile
pic_save=PhotoImage(file="save.png" )
pic_save=pic_save.subsample(10)
saveFileButton = Button(toolBar,relief=FLAT, command = saveAs)
saveFileButton.config(image=pic_save, compound=RIGHT, height='40',width='40')
saveFileButton.pack(side=LEFT)

#4th button:undo
pic_undo=PhotoImage(file="undo.png" )
pic_undo=pic_undo.subsample(10)
undoButton = Button(toolBar,relief=FLAT, command = undo)
undoButton.config(image=pic_undo, compound=RIGHT, height='40',width='40')
undoButton.pack(side=LEFT)

#5th button:redo
pic_redo=PhotoImage(file="redo.png" )
pic_redo=pic_redo.subsample(10)
redoButton = Button(toolBar,relief=FLAT, command = redo)
redoButton.config(image=pic_redo, compound=RIGHT, height='40',width='40')
redoButton.pack(side=LEFT)

#6th button:bold
pic_bold=PhotoImage(file="bold.png" )
pic_bold=pic_bold.subsample(25)
boldButton = Button(toolBar,relief=FLAT, command = bold)
boldButton.config(image=pic_bold, compound=RIGHT, height='40',width='40')
boldButton.pack(side=LEFT)

#7th button:italics
pic_italic=PhotoImage(file="italic.png" )
pic_italic=pic_italic.subsample(25)
italicButton = Button(toolBar,relief=FLAT, command = italic)
italicButton.config(image=pic_italic, compound=RIGHT, height='40',width='40')
italicButton.pack(side=LEFT)

#Drop Down for font family
variable = StringVar(root)
variable.set("Choose Fonts") # default value
w = OptionMenu(toolBar, variable ,FONT_OPTIONS[0],FONT_OPTIONS[1],FONT_OPTIONS[2], command=changefonts)
w.pack(side=LEFT)
toolBar.pack(side=TOP, fill=BOTH,expand= 1)
size=10
#8th button for font increase
pic_inc=PhotoImage(file="inc.png" )
pic_inc=pic_inc.subsample(25)
incButton = Button(toolBar,relief=FLAT, command = OnBigger)
incButton.config(image=pic_inc, compound=RIGHT, height='40',width='40')
incButton.pack(side=LEFT)

#9th button for font increase
pic_dec=PhotoImage(file="de.png" )
pic_dec=pic_dec.subsample(25)
decButton = Button(toolBar,relief=FLAT, command = OnSmaller)
decButton.config(image=pic_dec, compound=RIGHT, height='40',width='40')
decButton.pack(side=LEFT)

#10th button for find
pic_find=PhotoImage(file="find.png" )
pic_find=pic_find.subsample(12)
findButton = Button(toolBar,relief=FLAT, command = onFind)
findButton.config(image=pic_find, compound=RIGHT, height='40',width='40')
findButton.pack(side=LEFT)

#Creating the text frame
text = Text(root, width=400, height=400 , undo = True)
text.tag_configure('bt' ,font='helvetica 14 bold')
text.insert('1.0', 'Welcome to the Text Editor by Group 7\nStart Typing here !!!')
text.pack()

root.config(menu=menubar)
root.mainloop()





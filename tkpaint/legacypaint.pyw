#!/usr/bin/env python3


# imports
import tkinter as tk
import sys
from PIL import ImageTk,Image
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.messagebox as tkmb
from tkinter.colorchooser import askcolor
import tkinter.ttk as ttk




# paint variables
DEFAULT_COLOR = 'black'
DEFAULT_BG_COLOR = 'white'
DEFAULT_PEN_SIZE = 1
DEFAULT_DRAWMODE = ["pointer",  "eraser", "pen", "brush", "line", "stamp", "circle"]

bgcolor = DEFAULT_BG_COLOR
color = DEFAULT_COLOR
drawmode = DEFAULT_DRAWMODE[2]




# make window and images
logo = "./asset/logo.png"
window = tk.Tk()
logoimage = tk.PhotoImage(file=logo)
OGlogopillow = Image.open(logo)
logopillow = OGlogopillow.resize((38 * DEFAULT_PEN_SIZE, 110 * DEFAULT_PEN_SIZE))
logoTk = ImageTk.PhotoImage(logopillow)

# window setup
window.title("Tk paint")
window.iconphoto(True, logoimage)
window.geometry("580x640")
window.resizable(False,False)









# tk canvas functions
def pstopng(filePost, fileName):
    # use PIL to convert to PNG 
    img = Image.open(filePost) 
    img.save(fileName, 'png', lossless = True)

def paint(event):
    global logopillow
    global logoTk
    global ps
    # get x1, y1, x2, y2 co-ordinates
    x1, y1 = (event.x-3), (event.y-3)
    x2, y2 = (event.x+3), (event.y+3)
    x, y = event.x, event.y
    stampllow = OGlogopillow.resize((38 * DEFAULT_PEN_SIZE, 110 * DEFAULT_PEN_SIZE))
    stampK = ImageTk.PhotoImage(stampllow)
    global color
    if drawmode == DEFAULT_DRAWMODE[0]:
        cnv.old_coords = x, y
    elif drawmode == DEFAULT_DRAWMODE[1]:
            # display the mouse movement inside canvas
            cnv.old_coords = x, y
            cnv.create_oval(x1, y1, x2, y2, width=ps.get(), fill="white", outline="white", tag="eraser")
    elif drawmode == DEFAULT_DRAWMODE[2]:
            # display the mouse movement inside canvas
            cnv.old_coords = x, y
            cnv.create_oval(x1, y1, x2, y2, width=ps.get(), fill=color, outline=color, tag="pen")
    elif drawmode == DEFAULT_DRAWMODE[3]:
        cnv.old_coords = x, y
        cnv.create_oval(x1, y1, x2, y2, width=ps.get() + 10, fill=color, outline=color, tag="brush")
    elif drawmode == DEFAULT_DRAWMODE[4]:
        if cnv.old_coords:
            xc, yc = cnv.old_coords
            cnv.create_line(x, y, xc, yc, capstyle=tk.ROUND,smooth=True, width=ps.get(), tag="line")
        cnv.old_coords = x, y
    elif drawmode == DEFAULT_DRAWMODE[5]:
        cnv.old_coords = x, y
        cnv.create_image(x, y, anchor=tk.NW, image=stampK, tag="logo")
    elif drawmode == DEFAULT_DRAWMODE[6]:
        if cnv.old_coords:
            xc, yc = cnv.old_coords
            cnv.create_oval(x, y, xc, yc, width=ps.get(), tag="circle")
        cnv.old_coords = x, y
    else:
        pass


def stamp(event):
    x1, y1 = (event.x-3), (event.y-3)
    x2, y2 = (event.x+3), (event.y+3)

def cleancanvas():
    cnv.delete("all")

def savecanvas():
    global ststxt
    global stspg
    filepath = asksaveasfilename(
        defaultextension=".eps",
        filetypes=[("POST-scripts", "*.eps *.ps"), ("All Files","*.*")]
    )
    if not filepath:
        return
    stspg.start()
    try:
        ststxt["text"] = " Exporting Postscript"
        cnv.postscript(file = filepath)
        ststxt["text"] = "Canvas has been saved to a postscript named " + filepath
        stspg.stop()
        tkmb.showinfo(title='Canvas Save', message='Canvas has been saved to a postscript')
    except:
        stspg.stop()
        simpe = sys.exc_info()[1]
        ststxt["text"] = 'Failed to make postscript with error ' + str(simpe)
        tkmb.showerror(title="Failure", message=str("Failed to make postscript, Postscript error with \n\n" + str(sys.exc_info()) + " \n\nSimplified Error: \n" + str(simpe)))




def exportpostscript():
    global ststxt
    global stspg
    filepost = askopenfilename(
        defaultextension=".eps",
        filetypes=[("POST-scripts", "*.eps *.ps"), ("All Files","*.*")]
    )
    if not filepost:
        return
    filepath = asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG image", "*.png")]
    )
    if not filepath:
        return
    stspg.start()
    try:
        ststxt["text"] = "Exporting PNG"
        pstopng(filepost, filepath)
        ststxt["text"] = "Postscript has been exported to a PNG named " + filepath
        stspg.stop()
        tkmb.showinfo(title='Postscript Export', message='Postscript has been exported to PNG')
    except:
        stspg.stop()
        simpe = sys.exc_info()[1]
        ststxt["text"] = 'Failed to export PNG with error ' + str(simpe)
        tkmb.showerror(title="Failure", message=str("Failed to export to png, Export error with \n\n" + str(sys.exc_info()) + " \n\nSimplified Error: \n" + str(simpe)))


def changecanvasfg():
    global color
    color = askcolor(color=color)[1]


def changecanvasbg():
    global bgcolor
    bgcolor = askcolor(color=bgcolor)[1]
    cnv.configure(bg=bgcolor)


def changepen(tape):
    global drawmode
    drawmode = tape
    stspen["text"] = drawmode



def redraw():
    if(len(self.corde)):
        for i in range(len(self.corde)):
            cnv.create_line(self.cords[i],self.corde[i],width=4, fill="black")
    if (len(self.ocorde)):
        for i in range(len(self.ocorde)):
            cnv.create_oval(self.ocords[i], self.ocorde[i], width=4, outline="black")






# non tk canvas functions
def sysexit(code = 0):
    try:
        window.quit()
        window.destroy()
    except:
        pass
    sys.exit(code)
    raise SystemExit(code)









# create menu bar
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
colormenu = tk.Menu(menubar, tearoff=0)
drawmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Color", menu=colormenu)
menubar.add_cascade(label="Draw", menu=drawmenu)

filemenu.add_command(label="Save", command=savecanvas)
filemenu.add_command(label="Export", command=exportpostscript)
filemenu.add_separator()
filemenu.add_command(label="Exit",command=sysexit)

colormenu.add_command(label="Pen Color", command=changecanvasfg)
colormenu.add_command(label="Background Color", command=changecanvasbg)

drawmenu.add_command(label=DEFAULT_DRAWMODE[0], command=lambda: changepen(DEFAULT_DRAWMODE[0]))
drawmenu.add_command(label=DEFAULT_DRAWMODE[1], command=lambda: changepen(DEFAULT_DRAWMODE[1]))
drawmenu.add_command(label=DEFAULT_DRAWMODE[2], command=lambda: changepen(DEFAULT_DRAWMODE[2]))
drawmenu.add_command(label=DEFAULT_DRAWMODE[3], command=lambda: changepen(DEFAULT_DRAWMODE[3]))
drawmenu.add_command(label=DEFAULT_DRAWMODE[4], command=lambda: changepen(DEFAULT_DRAWMODE[4]))
drawmenu.add_command(label=DEFAULT_DRAWMODE[5], command=lambda: changepen(DEFAULT_DRAWMODE[5]))
drawmenu.add_command(label=DEFAULT_DRAWMODE[6], command=lambda: changepen(DEFAULT_DRAWMODE[6]))



# create draw widget
fm = tk.Frame(window, relief=tk.SUNKEN)
fm.pack()


img = Image.open(logo)
img = img.resize((19, 55))
tkimage = ImageTk.PhotoImage(img)
logoimage = tk.Label(fm, image=tkimage, relief=tk.SUNKEN)
logoimage.grid(row = 0, column = 0)


cnv=tk.Canvas(fm, bg=bgcolor, width=500,height=500)
cnv.grid(row=1,column=0, columnspan=4)
cnv.old_coords = None

clsb=tk.Button(fm, text="Clear", command=cleancanvas)
clsb.grid(row=0,column=1)

# sveb=tk.Button(fm,text="S",command=savecanvas)
# sveb.grid(row=0,column=2)

psfm = tk.Frame(fm, relief=tk.SUNKEN)
psfm.grid(row = 0, column = 2)
ps = tk.Scale(psfm, orient=tk.HORIZONTAL, from_=1, to=40)
ps.grid(row = 0, column = 0)
ps.set(DEFAULT_PEN_SIZE)
pslbl = tk.Label(psfm,text="Pen Size")
pslbl.grid(row=1,column=0)



stsfm = tk.Frame(fm)
stsfm.grid(row = 2, column = 0, columnspan = 4)
stspen = tk.Label(stsfm, text=drawmode)
stspen.pack()
ststxt = tk.Label(stsfm, text="")
ststxt.pack()
stspg = ttk.Progressbar(stsfm, orient = tk.HORIZONTAL, length=280, mode = 'indeterminate')
stspg.pack()







# bind mouse event with canvas(cnv)

cnv.bind('<B1-Motion>', paint)
cnv.bind("<ButtonPress-1>", paint)
# cnv.bind('<Motion>', paintline)
window.config(menu=menubar)
window.mainloop()

sysexit()

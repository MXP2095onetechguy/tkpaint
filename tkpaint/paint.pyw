import tkinter as tk
import sys
import copy
import threading
import os
from PIL import ImageTk,Image, ImageGrab
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.messagebox as tkmb
import tkinter.commondialog as tkcd
import tkinter.dialog as tkd
from tkinter.colorchooser import askcolor
import tkinter.ttk as ttk
import tooltip as tp
import tk_tools as tktools

class Paint:
    def redraw(self):
        if(len(self.corde)):
            for i in range(len(self.corde)):
                self.cnv.create_line(self.cords[i],self.corde[i],width=4, fill="black")
        if (len(self.ocorde)):
            for i in range(len(self.ocorde)):
                self.cnv.create_oval(self.ocords[i], self.ocorde[i], width=4, outline="black")

    def button_released(self,event):
        self.x.extend([self.current_x,self.current_y])
        self.y.extend([event.x,event.y])
        if(self.t=="l"):
            self.cords.append(self.x)
            self.corde.append(self.y)
        elif(self.t=="c"):
            self.ocords.append(self.x)
            self.ocorde.append(self.y)
        self.exist=1
        self.current_x, self.current_y,self.n,self.oldx,self.oldy,self.x,self.y,self.t=0,0,0,0,0,list(),list(),""

    
    def button_click(self,event):
            self.cnv.create_oval(event.x,event.y,event.x,event.y,fill=self.color_fg,width=self.PS.get(), outline=self.color_outline, tag="pen")

    def brush_click(self,event):
            self.cnv.create_oval(event.x,event.y,event.x,event.y,fill=self.color_fg,width=self.PS.get() + 10, outline=self.color_outline, tag="brush")

    def erase_click(self,event):
        self.cnv.create_oval(event.x,event.y,event.x,event.y,fill="white", width=self.PS.get() + 10, outline="white", tag="eraser")

    def stamp_click(self, event):
        GrepTk = self.OGlogopillow.resize((38 * self.PS.get(), 110 * self.PS.get()))
        self.cnv.stampTk.append(ImageTk.PhotoImage(GrepTk))
        self.cnv.create_image(event.x, event.y, anchor=tk.CENTER, image=self.cnv.stampTk[self.cnv.stampTkIndex], tag="logo")
        self.cnv.stampTkIndex += 1

    def stampgirl_click(self, event):
        GrepTk = self.OGgirlpillow.resize((38 * self.PS.get(), 110 * self.PS.get()))
        self.cnv.girlstampTk.append(ImageTk.PhotoImage(GrepTk))
        self.cnv.create_image(event.x, event.y, anchor=tk.CENTER, image=self.cnv.girlstampTk[self.cnv.girlstampTkIndex], tag="logo")
        self.cnv.girlstampTkIndex += 1

    def pengirl_click(self, event):
        GrepTk = self.OGpengirlpillow.resize((38 * self.PS.get(), 110 * self.PS.get()))
        self.cnv.girlstampTk.append(ImageTk.PhotoImage(GrepTk))
        self.cnv.create_image(event.x , event.y, anchor=tk.CENTER, image=self.cnv.girlstampTk[self.cnv.girlstampTkIndex], tag="logo")
        self.cnv.girlstampTkIndex += 1

    def line_click(self,event):
        self.cnv.delete("line")
        if(self.exist==1):
            self.redraw()
        if(self.n==0):
            self.current_x, self.current_y = event.x, event.y
            self.n=1
        self.cnv.create_line(self.current_x,self.current_y,event.x,event.y,width=self.PS.get(), fill=self.color_fg, tag="line")
        self.oldx=event.x
        self.oldy=event.y
        self.t="l"
        self.cnv.bind("<ButtonRelease-1>",self.button_released)

    
    def clear_screen(self):
        self.cnv.delete("all")
        self.current_x, self.current_y,self.n,self.oldx,self.oldy,self.x,self.y,self.t=0,0,0,0,0,list(),list(),""
        self.ocords,self.ocorde,self.corde,self.cords=list(),list(),list(),list()
        self.cnv.stampTk = []
        self.cnv.stampTkIndex = 0
        self.cnv.girlstampTk = []
        self.cnv.girlstampTkIndex = 0

        
    def create_circle(self,event):
        self.cnv.delete("circle")
        if(self.exist==1):
            self.redraw()
        if(self.n==0):
            self.current_x, self.current_y = event.x, event.y
            self.n=1
        self.cnv.create_oval(self.current_x,self.current_y,event.x,event.y,width=self.PS.get(), outline=self.color_fg, tag="circle")
        self.oldx=event.x
        self.oldy=event.y
        self.t="c"
        self.cnv.bind("<ButtonRelease-1>",self.button_released)

    def nobind(self, event):
        pass

    # draw dots with pen
    def pen_selected(self):
        self.cnv.bind("<B1-Motion>",self.button_click)
        self.cnv.bind("<ButtonPress-1>", self.button_click)
        self.drawmode = "Pen"
        self.stspen["text"] = self.drawmode

    # brush
    def brush_selected(self):
        self.cnv.bind("<B1-Motion>", self.brush_click)
        self.cnv.bind("<ButtonPress-1>", self.brush_click)
        self.drawmode = "Brush"
        self.stspen["text"] = self.drawmode

    # draw line
    def line_selected(self):
        self.cnv.bind("<B1-Motion>",self.line_click)
        self.cnv.bind("<ButtonPress-1>", self.nobind)
        self.drawmode = "Line"
        self.stspen["text"] = self.drawmode

    # draw circle
    def circle_selected(self):
        self.cnv.bind("<B1-Motion>",self.create_circle)
        self.cnv.bind("<ButtonPress-1>", self.nobind)
        self.drawmode = "Circle"
        self.stspen["text"] = self.drawmode

    # eraser
    def eraser_selected(self):
        self.cnv.bind("<B1-Motion>", self.erase_click)
        self.cnv.bind("<ButtonPress-1>", self.erase_click)
        self.drawmode = "Eraser"
        self.stspen["text"] = self.drawmode

    # logo stamp
    def stamp_selected(self):
        self.cnv.bind("<B1-Motion>", self.stamp_click)
        self.cnv.bind("<ButtonPress-1>", self.stamp_click)
        self.drawmode = "Logo Stamp"
        self.stspen["text"] = self.drawmode

    # girl stamp
    def stampgirl_selected(self):
        self.cnv.bind("<B1-Motion>", self.stampgirl_click)
        self.cnv.bind("<ButtonPress-1>", self.stampgirl_click)
        self.drawmode = "Girl Stamp"
        self.stspen["text"] = self.drawmode

    # pen girl stamp
    def penstamp_selected(self):
        self.cnv.bind("<B1-Motion>", self.pengirl_click)
        self.cnv.bind("<ButtonPress-1>", self.pengirl_click)
        self.drawmode = "Pen Girl Stamp"
        self.stspen["text"] = self.drawmode


    def changecanvasfg(self, event=None):
        self.color_fg = askcolor(color=self.color_fg)[1]


    def changecanvasbg(self, event=None):
        self.color_bg = askcolor(color=self.color_bg)[1]
        self.cnv.configure(bg=self.color_bg)

    def changecanvasoutline(self, event=None):
        self.color_outline = askcolor(color=self.color_outline)[1]

    def pstopng(self, filePost, fileName):
        # use PIL to convert to PNG 
        img = Image.open(filePost) 
        img.save(fileName, 'png', lossless = True)

    def exportpostscript(self):
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
        self.stspg.start()
        try:
            self.ststxt["text"] = "Exporting PNG"
            self.pstopng(filepost, filepath)
            self.ststxt["text"] = "Postscript has been exported to a PNG named " + filepath
            self.stspg.stop()
            tkmb.showinfo(title='Postscript Export', message='Postscript has been exported to PNG')
        except:
            self.stspg.stop()
            simpe = sys.exc_info()[1]
            self.ststxt["text"] = 'Failed to export PNG with error ' + str(simpe)
            tkmb.showerror(title="Failure", message=str("Failed to export to png, Export error with \n\n" + str(sys.exc_info()) + " \n\nSimplified Error: \n" + str(simpe)))

    def exportpng(self):
        file =  asksaveasfilename(filetypes=[('PNG image','*.png')])
        if file:
            x = self.cnv.winfo_rootx() + self.cnv.winfo_x()
            y = self.cnv.master.winfo_rooty() + self.cnv.winfo_y()
            x1 = x + self.cnv.winfo_width()
            y1 = y + self.cnv.winfo_height()

            ImageGrab.grab().crop((x,y,x1,y1)).save(file)
        else:
            return
        pass

    def exportpostscriptng(self):
        filepost = asksaveasfilename(
            defaultextension=".eps",
            filetypes=[("POST-scripts", "*.eps *.ps"), ("All Files","*.*")]
        )
        if not filepath:
            return
        self.stspg.start()
        try:
            self.ststxt["text"] = " Exporting Postscript"
            self.cnv.postscript(file = filepost)
            filepath = asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG image", "*.png")]
            )
            if not filepath:
                return
            self.ststxt["text"] = "Converting Postscript to PNG"
            self.pstopng(filepost, filepath)
            self.ststxt["text"] = "Canvas has been saved to a postscript and converted to a PNG named " + filepath
            self.stspg.stop()
            tkmb.showinfo(title='Canvas Save', message='Canvas has been saved to a postscript and converted to PNG')
        except:
            self.stspg.stop()
            simpe = sys.exc_info()[1]
            self.ststxt["text"] = 'Failed to make postscript with error ' + str(simpe)
            tkmb.showerror(title="Failure", message=str("Failed to make postscript to png, PNG error with \n\n" + str(sys.exc_info()) + " \n\nSimplified Error: \n" + str(simpe)))


    def savecanvas(self):
        filepath = asksaveasfilename(
            defaultextension=".eps",
            filetypes=[("POST-scripts", "*.eps *.ps"), ("All Files","*.*")]
        )
        if not filepath:
            return
        self.stspg.start()
        try:
            self.ststxt["text"] = " Exporting Postscript"
            self.cnv.postscript(file = filepath)
            self.ststxt["text"] = "Canvas has been saved to a postscript named " + filepath
            self.stspg.stop()
            tkmb.showinfo(title='Canvas Save', message='Canvas has been saved to a postscript')
        except:
            self.stspg.stop()
            simpe = sys.exc_info()[1]
            self.ststxt["text"] = 'Failed to make postscript with error ' + str(simpe)
            tkmb.showerror(title="Failure", message=str("Failed to make postscript, Postscript error with \n\n" + str(sys.exc_info()) + " \n\nSimplified Error: \n" + str(simpe)))


    def sysexit(self, code = 0):
        try:
            self.window.quit()
            self.window.destroy()
        except:
            pass
        
        sys.exit()
        raise SystemExit()

    def updateGaugeAndLed(self):
        self.rs.set_value(self.PS.get())
        # print(self.PS.get())
        self.winfm.timer.after(20, self.updateGaugeAndLed)

        if self.PS.get() > 32:
            self.led.to_red(on=True)
        elif self.PS.get() <= 0:
            self.led.to_red(on=False)
        else:
            self.led.to_grey(on=True)

    def openiMage(self):
        filepen = askopenfilename(
            defaultextension=".eps",
            filetypes=[("PNG", "*.png"), ("All Files","*.*")]
        )

        if not filepen:
            return

        openimg = Image.open(filepen)
        openimgTk = ImageTk.PhotoImage(openimg)

        self.cnv.create_image(self.cnv.winfo_width(), self.cnv.winfo_height(), image=openimgTk, anchor=tk.CENTER, tag="open")
        # print("a")

    # new window
    def newWin(self):
        exec(__file__)
        # os.execv(sys.executable, ['python'] + sys.argv)
        



    # init
    def __init__(self, win):
        self.window=win
        self.window.title("Tk paint")
        self.logo = "./asset/logo.png"
        self.girl="./asset/bootyfaintingwoman.png"
        self.pengirl = "./asset/penwoman.png"
        try:
            self.window.iconphoto(True, tk.PhotoImage(file=self.logo))
        except:
            self.sysexit(1)
        
        self.x, self.y = list(),list()
        self.current_y,self.current_x,self.n=0,0,0
        self.exist = 0
        self.cords,self.corde,self.ocords,self.ocorde=list(),list(),list(),list()
        self.oldx,self.oldy,self.t=0,0,""
        self.DEFAULT_COLOR = 'black'
        self.DEFAULT_OUTLINE_COLOR = 'black'
        self.DEFAULT_BG_COLOR = 'white'
        self.DEFAULT_PEN_SIZE = 4
        self.color_fg = self.DEFAULT_COLOR
        self.color_outline = self.DEFAULT_OUTLINE_COLOR
        self.color_bg = self.DEFAULT_BG_COLOR


        try:
                    self.logoimage = tk.PhotoImage(file=self.logo)
                    self.girlimage = tk.PhotoImage(file=self.girl)
                    self.pengirlimage = tk.PhotoImage(file = self.pengirl)
                    self.OGlogopillow = Image.open(self.logo)
                    self.OGgirlpillow = Image.open(self.girl)
                    self.OGpengirlpillow = Image.open(self.pengirl)
        except:
            self.sysexit(1)
        self.logopillow = self.OGlogopillow.resize((38 * self.DEFAULT_PEN_SIZE, 110 * self.DEFAULT_PEN_SIZE))
        self.girlpillow = self.OGgirlpillow.resize((38 * self.DEFAULT_PEN_SIZE, 110 * self.DEFAULT_PEN_SIZE))
        self.pengirlpillow = self.OGgirlpillow.resize((38 * self.DEFAULT_PEN_SIZE, 110 * self.DEFAULT_PEN_SIZE))
        self.girlTk = ImageTk.PhotoImage(self.girlpillow)
        self.logoTk = ImageTk.PhotoImage(self.logopillow)
        self.pengirlTk = ImageTk.PhotoImage(self.pengirlpillow)
        
        self.drawmode = ""
        self.winsize = ["886", "700"]

        self.winfm = tk.Frame(self.window)
        self.winfm.pack(fill=tk.BOTH)

        self.winfm.timer = tk.Frame(self.winfm)

        fm=tk.Frame(self.winfm, relief=tk.SUNKEN, bd=10)
        fm.pack(side=tk.BOTTOM)

        self.toolbar = tk.Frame(self.winfm, bd=1, relief=tk.RAISED)
        self.toolbar.pack(fill=tk.X, side=tk.TOP)

        self.toolbar.quit = tk.Button(self.toolbar, relief=tk.FLAT, text="Quit", command=self.window.quit)
        self.toolbar.quit.pack(side=tk.LEFT)

        self.toolbar.save = tk.Button(self.toolbar, relief=tk.FLAT, text="Export as PNG", command=self.exportpng)
        self.toolbar.save.pack(side=tk.LEFT)

        self.toolbar.penColor = tk.Button(self.toolbar, relief=tk.FLAT, text="Pen Color", command=self.changecanvasfg)
        self.toolbar.penColor.pack(side=tk.LEFT)

        self.toolbar.penOutlineColor = tk.Button(self.toolbar, relief=tk.FLAT, text="Pen Outline Color", command=self.changecanvasoutline)
        self.toolbar.penOutlineColor.pack(side=tk.LEFT)




        ButtonFrame = tk.Frame(fm, relief=tk.SUNKEN, bd=5)
        ButtonFrame.grid(row = 0, column = 0)

        CanvasFrame = tk.Frame(fm)
        CanvasFrame.grid(row = 0, column = 1)
        
        self.window.geometry(self.winsize[0] + "x" + self.winsize[1])



        logoFrame = tk.Frame(ButtonFrame, relief=tk.SUNKEN, bd=5)
        logoFrame.grid(row = 0, column = 0)
        img = self.OGlogopillow
        img = img.resize((19, 55))
        tkimage = ImageTk.PhotoImage(img)
        del img
        self.logoimg = tk.Label(logoFrame, image=tkimage)
        self.logoimg.tooltip = tp.CreateToolTip(self.logoimg, text="Logo wahoo")
        self.logoimg.grid(row = 0, column = 0)
        self.logotxt = tk.Label(logoFrame, text="Tk Paint")
        self.logotxt.grid(row = 0, column = 1)
        
        
        pen=tk.Button(ButtonFrame,text=" PEN ",command=self.pen_selected)
        pen.grid(row = 1, column = 0)
        circle_button=tk.Button(ButtonFrame,text="  O  ",command=self.circle_selected)
        circle_button.tooltip = tp.CreateToolTip(circle_button, text="Draw circle if you cannot tell")
        circle_button.grid(row = 2, column = 0)
        brush_button=tk.Button(ButtonFrame,text="  BRUSH  ",command=self.brush_selected)
        brush_button.grid(row = 3, column = 0)
        self.line=tk.Button(ButtonFrame,text="  /  ",command=self.line_selected)
        self.line.tooltip = tp.CreateToolTip(self.line, text="Draw a line if you cannot tell")
        self.line.grid(row = 4, column = 0)
        logostamp = tk.Button(ButtonFrame, text=" LS  ", command=self.stamp_selected)
        logostamp.grid(row = 5, column = 0)
        girlstamp = tk.Button(ButtonFrame, text=" GS  ", command=self.stampgirl_selected)
        girlstamp.grid(row = 6, column = 0)
        self.penstamp = ttk.Button(ButtonFrame, text=" PS  ", command=self.penstamp_selected)
        self.penstamp.tooltip = tp.CreateToolTip(self.penstamp, text="The Creator's favorite stamp")
        self.penstamp.grid(row = 7, column = 0)
        eraser = tk.Button(ButtonFrame, text="  E  ", command=self.eraser_selected)
        eraser.tooltip = tp.CreateToolTip(eraser, text="Erases things")
        eraser.grid(row = 8, column = 0)
        clear_button=tk.Button(ButtonFrame,text="  C  ", command=self.clear_screen)
        clear_button.tooltip = tp.CreateToolTip(clear_button, text="Clear the canvas")
        clear_button.grid(row = 9, column = 0)



        PenFrame = tk.Frame(ButtonFrame, bd=5, relief=tk.SUNKEN)
        PenFrame.grid(row = 10, column = 0)
        self.PS = tk.Scale(PenFrame, orient=tk.HORIZONTAL, from_=0, to=40, showvalue = 0)
        self.PS.pack()
        self.PS.set(self.DEFAULT_PEN_SIZE)
        self.rs = tktools.RotaryScale(PenFrame, max_value=40)
        self.rs.pack()
        self.winfm.timer.after(20, self.updateGaugeAndLed)
        PSlbl = tk.Label(PenFrame, text="Pen Size")
        PSlbl.pack()
        self.led = tktools.Led(PenFrame, size=50)
        self.led.pack()
        
        self.cnv=tk.Canvas(CanvasFrame, width=586,height=586,background=self.color_bg)
        self.cnv.pack()


        menubar = tk.Menu(self.window)
        filemenu = tk.Menu(menubar, tearoff=0)
        colormenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Color", menu=colormenu)

        filemenu.add_command(label="New window", command=self.newWin)
        filemenu.add_separator()
        filemenu.add_command(label="Open Image", command=self.openiMage)
        filemenu.add_command(label="Save as postscript", command=self.savecanvas)
        filemenu.add_command(label="Convert to png from postscript", command=self.exportpostscript)
        filemenu.add_command(label="Export as Ghostscript", command=self.exportpostscriptng)
        filemenu.add_command(label="Export as Png", command=self.exportpng)
        filemenu.add_separator()
        filemenu.add_command(label="Exit",command=self.sysexit)

        colormenu.add_command(label="Pen Color", command=self.changecanvasfg)
        colormenu.add_command(label="Pen Outline Color", command=self.changecanvasoutline)
        colormenu.add_command(label="Background Color", command=self.changecanvasbg)



        stsfm = tk.Frame(fm)
        stsfm.grid(row = 4, column = 0, columnspan = 2)
        self.stspen = tk.Label(stsfm, text=self.drawmode)
        self.stspen.pack()
        self.ststxt = tk.Label(stsfm, text="")
        self.ststxt.pack()
        self.stspg = ttk.Progressbar(stsfm, orient = tk.HORIZONTAL, length=280, mode = 'indeterminate')
        self.stspg.pack()


        # self.cnv.bind("<B1-Motion>",self.button_click)
        self.pen_selected()


        self.cnv.stampTkIndex = 0
        self.cnv.girlstampTkIndex = 0
        self.cnv.penstampTkIndex = 0
        self.cnv.stampTk = []
        self.cnv.girlstampTk = []
        self.cnv.penstampTk = []
        
        self.window.config(menu=menubar)
        self.window.mainloop()

        self.sysexit()


if __name__ == "__main__":
    win = tk.Tk()
    m = Paint(win=win)
    sys.exit()
    raise SystemExit()

else:
    sys.exit()
    raise SystemExit()

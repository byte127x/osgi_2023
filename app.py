from tkinter import *
from tkinter import ttk, messagebox
from io import StringIO
from contextlib import redirect_stdout
from pathlib import Path
from PIL import Image, ImageTk
from functools import partial
import os
#import tkinter as ttk

class LoginForm(Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        self.attributes('-alpha', 0.85)
        self.after(2, self.configure_myself)

    def configure_myself(self):
        resolution = self.geometry().split('x')
        resolution[0] = int(resolution[0])
        resolution[1] = int(resolution[1].split('+')[0])
        print(resolution)
        c = Canvas(self, width=resolution[0], height=resolution[1])
        c.pack(fill='both', expand=1)
        self.bg = ImageTk.PhotoImage(Image.open('Lib\\login_bg.jpg').resize((resolution[0], resolution[1]), Image.ANTIALIAS))
        c.create_image(0, 0, image=self.bg, anchor="nw")

        self.username = None
        self.stage = 'username'
        self.entered = {'uname': '', 'password': ''}

        main = ttk.Frame(self)
        self.title = ttk.Label(main, text='Login ...', font=(None, 18))
        self.title.grid(row=0, column=0, columnspan=2, pady=5)
        self.sub = ttk.Label(main, text='Username')
        self.sub.grid(row=1, column=0, columnspan=2, pady=5)
        self.stdin = ttk.Entry(main, width=25)
        self.stdin.grid(row=2, column=0, pady=0)
        ttk.Button(main, text='Next ...', command=self.next).grid(row=2, column=1)
        c.create_window(resolution[0]//2, resolution[1]//2, window=main)

    def next(self):
        if self.stage == 'username':
            self.dictview = {}
            for x in users:
                self.dictview[x[0]] = x[1]
            if not (self.stdin.get() in list(self.dictview.keys())):
                messagebox.showerror(None, 'Username entered is incorrect')
                return
            if (self.dictview[self.stdin.get()] == '') or (self.dictview[self.stdin.get()] == None):
                self.completed()
                return
            self.username = self.stdin.get()
            self.sub['text'] = 'Password'
            self.stage = 'password'
            self.stdin.delete(0, END)
            self.stdin['show'] = '*'
            self.title['text'] = f'Welcome {self.username}'
            return
        
        if self.dictview[self.username] == self.stdin.get():
            self.completed()
        else:
            messagebox.showerror(None, 'Wrong Password')
            return
    
    def completed(self):
        self.destroy()
        OSGI_Root()

class OSGI_Root(Tk):
    def __init__(self, *args):
        super().__init__()
        self.geometry('560x340')
        self.title('*O*pen *S*ource *G*raphical *I*nterface')

        self.apps = ttk.LabelFrame(self, text='Installed Apps')
        self.apps.pack(fill='both', expand=1, pady=10, padx=10)

        ttk.Button(self.apps, text='Calculator', command=Calc).pack(ipady=10, ipadx=10, pady=5)
        ttk.Button(self.apps, text='Paint Program', command=ShotoPhop).pack(ipady=10, ipadx=10)
        ttk.Button(self.apps, text='FileTabs!', command=FileTabs).pack(ipady=10, ipadx=10)
        ttk.Button(self.apps, text='Dev', command=Dev).pack(ipady=10, ipadx=10)

class Calc(Tk):
    def __init__(self):
        super().__init__()
        self.title('Calculator')
        self.geometry('225x400')
        self.clr = lambda: self.entry.delete(0, END)

        self.button1 = ttk.Button(self, text='1', command=lambda: self.write(1))
        self.button1.grid(row=1, column=0, sticky='nwes')
        self.button2 = ttk.Button(self, text='2', command=lambda: self.write(2))
        self.button2.grid(row=1, column=1, sticky='nwes')
        self.button3 = ttk.Button(self, text='3', command=lambda: self.write(3))
        self.button3.grid(row=1, column=2, sticky='nwes')
        self.button4 = ttk.Button(self, text='4', command=lambda: self.write(4))
        self.button4.grid(row=2, column=0, sticky='nwes')
        self.button5 = ttk.Button(self, text='5', command=lambda: self.write(5))
        self.button5.grid(row=2, column=1, sticky='nwes')
        self.button6 = ttk.Button(self, text='6', command=lambda: self.write(6))
        self.button6.grid(row=2, column=2, sticky='nwes')
        self.button7 = ttk.Button(self, text='7', command=lambda: self.write(7))
        self.button7.grid(row=3, column=0, sticky='nwes')
        self.button8 = ttk.Button(self, text='8', command=lambda: self.write(8))
        self.button8.grid(row=3, column=1, sticky='nwes')
        self.button9 = ttk.Button(self, text='9', command=lambda: self.write(9))
        self.button9.grid(row=3, column=2, sticky='nwes')

        self.button0 = ttk.Button(self, text='0', command=lambda: self.write(0))
        self.button0.grid(row=4, column=0, sticky='nwes')
        self.buttonplus = ttk.Button(self, text='Clear', command=self.cls)
        self.buttonplus.grid(row=4, column=1, sticky='nwes')
        self.buttonequal = ttk.Button(self, text='=', command=self.equals)
        self.buttonequal.grid(row=4, column=2, sticky='nwes')
        
        self.buttonplus = ttk.Button(self, text='+', command=self.start_add)
        self.buttonplus.grid(row=5, column=0, sticky='nwes')
        self.buttonplus = ttk.Button(self, text='-', command=self.start_sub)
        self.buttonplus.grid(row=5, column=1, sticky='nwes')
        self.buttonplus = ttk.Button(self, text='x', command=self.start_mul)
        self.buttonplus.grid(row=5, column=2, sticky='nwes')

        self.entry = ttk.Entry(self, justify=RIGHT)
        self.entry.grid(row=0, column=0, columnspan=3, sticky='nwes', padx=5, pady=5)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=5)
        self.grid_rowconfigure(1, weight=6)
        self.grid_rowconfigure(2, weight=6)
        self.grid_rowconfigure(3, weight=6)
        self.grid_rowconfigure(4, weight=6)
        self.grid_rowconfigure(5, weight=6)
        self.bind('<Configure>', self.update_entry)

        self.first_number = None
        self.operation = '+'

    def cls(self):
        self.first_number = None
        self.clr()
        self.entry.insert(END, 'Memory Cleared')
        self.after(1000, self.clr)

    def start_operation(self):
        if self.entry.get() == 'Memory Cleared':
            return False
        self.first_number = float(self.entry.get())
        self.clr()

    def start_add(self):
        self.start_operation()
        self.operation = '+'

    def start_sub(self):
        self.start_operation()
        self.operation = '-'

    def start_mul(self):
        self.start_operation()
        self.operation = 'x'

    def equals(self):
        if self.first_number == None:
            return
        if self.operation == '+':
            ans = self.first_number + float(self.entry.get())
        elif self.operation == '-':
            ans = self.first_number - float(self.entry.get())
        elif self.operation == 'x':
            ans = self.first_number * float(self.entry.get())
        
        self.clr()
        self.entry.insert(END, str(ans))
        self.first_number = None

    def update_entry(self, e):
        ioka = int(self.entry.winfo_height()//2.5)
        self.entry['font'] = (None, ioka)

    def write(self, num):
        self.entry.insert(END, num)

class ShotoPhop(Tk):
    def __init__(self):
        global brshsz
        super().__init__()
        self.title('Paint Program')
        self.geometry('620x480')
        self.stroke_size = IntVar(value=20)

        self.brushsizemenu = Menu(tearoff=0)
        self.brushsizemenu.add_command(label='Extra Large', command=lambda: self.stroke_size.set(30))
        self.brushsizemenu.add_command(label='Large', command=lambda: self.stroke_size.set(20))
        self.brushsizemenu.add_command(label='Medium', command=lambda: self.stroke_size.set(10))
        self.brushsizemenu.add_command(label='Small', command=lambda: self.stroke_size.set(5))

        self.control_panel = ttk.Frame(self)
        self.control_panel.pack(fill=X)

        brshsz = ImageTk.PhotoImage(Image.open('Lib/brush.webp').resize((45, 45), Image.ANTIALIAS), master=self)
        self.brshsz_btn = ttk.Button(self.control_panel, text='Brush Size', image=brshsz, compound=TOP)
        self.brshsz_btn.grid(row=0, column=0)

        self.colors = LabelFrame(self.control_panel, text='Colors')
        self.colorpallate = Canvas(self.colors, bg='white')
        size = 19
        padding = 8
        colors = [
            ['red', 'orange', 'yellow', 'green', 'blue', 'purple', '#FF00FF', 'black'],
            ['pink', '#FF5300', '#FFD200', '#00FF00', '#008080', '#4000C0', '#8080FF', 'white']
        ]
        self.clr = 'black'
        totalwidth = 0
        totalheight = 0
        in_a_row = [None]
        for rowidx, row in enumerate(colors):
            for columnidx, column in enumerate(row):
                in_a_row.append(column)
                lol = self.colorpallate.create_rectangle(size*columnidx+padding, size*rowidx+padding, size*(columnidx+1), size*(rowidx+1), fill=column)
                self.colorpallate.tag_bind(lol, '<Button-1>', partial(self.changecolor, in_a_row[lol]))
            totalwidth+=(size*(columnidx/2))
            totalheight+=(size+padding)
        totalheight-=size
        totalheight+=padding
        totalwidth+=size
        totalwidth+=padding
        self.colorpallate['width'] = totalwidth
        self.colorpallate['height'] = totalheight
        
        self.colors.grid(row=0, column=1, padx=(10, 0))
        self.colorpallate.pack(fill='both', expand=1, pady=5, padx=5)

        self.c = Canvas(self, bg='white', relief=GROOVE)
        self.c.pack(fill='both', expand=1)
        
        self.c.bind('<Button-1>', self.make_line)
        self.c.bind('<B1-Motion>', self.make_line)
        self.brshsz_btn.bind('<Button-1>', lambda e: self.brushsizemenu.tk_popup(e.x_root, e.y_root))

    def changecolor(self, newclr, e):
        self.clr = newclr

    def settings(self):
        setwin = Toplevel(self)

    def make_line(self, e):
        sz = self.stroke_size.get()
        self.c.create_oval(e.x-sz, e.y-sz, e.x+sz, e.y+sz, fill=self.clr, outline=self.clr)

class FileTabs(Tk):
    def __init__(self):
        super().__init__()
        self.title('FileTabs')
        self.directory = 'C:\\'
        self.dirtext = ttk.Label(self, text=self.directory)
        self.dirtext.grid(row=0, column=0)
        lb_frame = ttk.Frame(self)
        lb_frame.grid(row=1, column=0, sticky='nwes')
        self.lb = Listbox(lb_frame)
        self.lb.pack(fill='both', expand=1)

        ttk.Button(self, text='Open', command=self.open).grid(row=2, column=0, pady=10)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.render_currentdir()

    def render_currentdir(self):
        self.lb.delete(0, END)
        files = os.listdir(self.directory)
        self.lb.insert(END, '...')
        for x in files:
            self.lb.insert(END, x)
        self.dirtext['text'] = self.directory

    def open(self):
        for i in self.lb.curselection():
            active = self.directory+self.lb.get(i)
            print(active)
            if self.lb.get(i) == '...':
                starter = str(Path(self.directory).parent.absolute())
                self.directory = starter
                if not ((len(starter) == 3) and (starter[2] == '\\')):
                    self.directory += '\\'
                self.render_currentdir()
            elif os.path.isfile(active):
                os.startfile(active)
            else:
                self.directory = active+'\\'
                self.render_currentdir()

class Dev(Tk):
    def __init__(self):
        super().__init__()
        self.externalpython = ''
        self.title('Dev')
        self.geometry('420x450')

        menu = ttk.Menubutton(self, text='Python')
        menu.pack(pady=5)

        pymenu = Menu(menu, tearoff=0)
        pymenu.add_command(label='Run with Integrated Python', command=self.pyrun)
        pymenu.add_command(label='Run with External Python', command=self.externalpyrun)
        menu['menu'] = pymenu

        code = ttk.LabelFrame(self, text='Code')
        code.pack(fill='both', expand=1, pady=5, padx=5)
        self.txt = Text(code, width=1, height=1)
        self.txt.pack(fill='both', expand=1, pady=5, padx=5)
        console = ttk.LabelFrame(self, text='Output')
        console.pack(fill='both', expand=1, pady=5, padx=5)
        self.console = Text(console, width=1, height=1)
        self.console.pack(fill='both', expand=1, pady=5, padx=5)
        self.console['state'] = 'disabled'

    def externalpyrun(self):
        if not self.externalpython:
            self.externalpython = 'C:\\Windows\\py.exe'
        
        with open('temporary_file.py', 'w+') as f:
            f.write(self.txt.get('1.0', END))
        os.system(f'py "temporary_file.py" & echo: & echo Operation was completed & pause')

    def pyrun(self):
        f = StringIO()
        madeit = True
        with redirect_stdout(f):
            try:
                exec(self.txt.get('1.0', END), {}, {})
            except Exception as e:
                madeit = False
                lol = repr(e)+'\n'
        if madeit:  
            lol = f.getvalue()

        self.console['state'] = 'normal'
        self.console.insert(INSERT, str(lol))
        if not madeit:
            self.highlight_error(lol)
        self.console['state'] = 'disabled'

    def highlight_error(self, error):
        if error:
            idx = '1.0' 
            while True:
                idx = self.console.search(error, idx, nocase=1,
                        stopindex=END)
                if not idx:
                    break
                lastidx = '%s+%dc' % (idx, len(error))
                self.console.tag_add('found', idx, lastidx)
                idx = lastidx

            self.console.tag_config('found', foreground='red')

users = [
    ('*Default', ''),
    ('*Admin', 'adminpass'),
    ('Joe', 'joelikesdonuts')
]

LoginForm().mainloop()

'''
r = Tk()
ShotoPhop()
r.mainloop()
'''
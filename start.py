import copy
import time
from Tkinter import *
import tkMessageBox

import gamelife

init_filled = [
               (4,5),(4,6),(4,7),
               (5,5),(5,6),(5,7),
               (6,5),(6,6),(6,7),
                              
               (7,8),(7,9),(7,10),
               (8,8),(8,9),(8,10),
               (9,8),(9,9),(9,10),
               ]

init_filled = [
               (7,7),(8,7),(9,7),(9,8),(9,9),(8,9),(7,9)
               ]

init_filled = [
               (6,6),(6,7),(6,8),(7,8),(8,8),(8,9),(8,10)
               ]
#
#init_filled = [
#               (7,9),(8,8),(8,9),(8,10)
#               ]


class App:

    def __init__(self, master):
        matrixframe = Frame(master)
        matrixframe.pack(side=LEFT, fill=BOTH, expand=1)
        self.canvas = Canvas(matrixframe, background='#ffffff', width=600, height=600)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.canvas.bind('<Button-1>', self.user_update_cell)
        
        sideframe = Frame(master)
        sideframe.pack()
                
        delay_frame = Frame(sideframe)
        delay_frame.pack(side=TOP)
        
        dealy_label = Label(delay_frame, text="Delay (ms)")
        dealy_label.pack(side=LEFT)        
        self.delay_field = Entry(delay_frame, width="5")
        self.delay_field.pack(side=LEFT)
        set_delay_button = Button(delay_frame, text="Set delay", command=self.set_delay)
        set_delay_button.pack(side=LEFT)
        
        config_frame = Frame(sideframe)
        config_frame.pack(side=TOP)
        
        n_label = Label(config_frame, text="N")
        n_label.pack(side=LEFT)        
        self.n_field = Entry(config_frame, width="3")
        self.n_field.pack(side=LEFT)
        m_label = Label(config_frame, text="M")
        m_label.pack(side=LEFT)        
        self.m_field = Entry(config_frame, width="3")
        self.m_field.pack(side=LEFT)
        self.set_nm_button = Button(config_frame, text="Set dimensions", command=self.set_dimensions)
        self.set_nm_button.pack(side=LEFT)
                
        buttons_frame = Frame(sideframe)
        buttons_frame.pack(side=BOTTOM)
        
        self.start_button = Button(buttons_frame, text="Start", command=self.start)
        self.start_button.pack(side=LEFT)
        self.stop_button = Button(buttons_frame, text="Stop", command=self.stop, state=DISABLED)
        self.stop_button.pack(side=LEFT)
        
        self.do_turn_button = Button(buttons_frame, text="Next step", command=self.do_turn)
        self.do_turn_button.pack(side=RIGHT)
        
        self.clear_button = Button(buttons_frame, text="Clear", command=self.clear)
        self.clear_button.pack(side=RIGHT)
                
        
        self.currtime = ''
        self.run = False
        self.delay = 100
        
        self.N=20
        self.M=20
        self.canvas_items = {}
        self.canvas_lines = []
        self.draw_grid()
        
    
    def user_update_cell(self, event):
        if self.run:
            return
        j = event.x / self.cell_size
        i = event.y / self.cell_size
        if (i,j) in self.canvas_items.keys():
            self.canvas.delete(self.canvas_items[(i,j)])
            del self.canvas_items[(i,j)]
        else:
            self.canvas_items[(i, j)] = self.drow_cell_entry((i, j))
    
    def do_turn(self):        
        matrix = self.game_life.do_turn()
        self.vizualize_turn(matrix)
    
    def timer(self):
        if not self.run:
            return
        newtime = time.strftime('%H:%M:%S')
        if newtime != self.currtime:
            self.currtime = newtime
            self.do_turn()           
        self.start_button.after(self.delay, self.timer)        
        
    def vizualize_turn(self, matrix):
        for k in self.canvas_items.keys():
            self.canvas.delete(self.canvas_items[k])
        self.canvas_items = {}
        for i in xrange(self.N):
            for j in xrange(self.M):
                if matrix[i][j]:
                    self.drow_cell_entry((i, j))    
    
    def drow_cell_entry(self, (x,y)):
        entry = self.canvas.create_rectangle(
                    y*self.cell_size+3, x*self.cell_size+3, 
                    (y+1)*self.cell_size-3, (x+1)*self.cell_size-3, 
                    fill="#ff0000")
        self.canvas_items[(x,y)] = entry
        return entry
        
    def draw_grid(self):
        self.clear_canvas()        
        self.width = int(self.canvas.cget("width"))
        self.height = int(self.canvas.cget("height"))        
        width = self.width/self.N
        height = self.height/self.M
        self.cell_size = min(width, height)
        for i in xrange(1, self.N):
            self.canvas_lines.append(self.canvas.create_line(0, i*self.cell_size, self.width, i*self.cell_size))
        for i in xrange(1, self.M):
            self.canvas_lines.append(self.canvas.create_line(i*self.cell_size, 0, i*self.cell_size, self.height))
    
    def clear_canvas(self):
        for k in self.canvas_items.keys():
            self.canvas.delete(self.canvas_items[k])
        self.canvas_items = {}
        for v in self.canvas_lines:
            self.canvas.delete(v)
        self.canvas_lines = []

    def clear(self):
        for k in self.canvas_items.keys():
            self.canvas.delete(self.canvas_items[k])
        self.canvas_items = {}
    

    def start(self):
        self.start_button.configure(state=DISABLED)
        self.stop_button.configure(state=NORMAL)
        self.set_nm_button.configure(state=DISABLED)
        
        self.game_life = gamelife.GameLife(self.N, self.M, self.canvas_items.keys())
        
        self.run = True        
        self.timer()

    def stop(self):
        self.start_button.configure(state=NORMAL)
        self.stop_button.configure(state=DISABLED)
        self.set_nm_button.configure(state=NORMAL)
        self.run = False
    
    def set_delay(self):
        try:
            delay = int(self.delay_field.get())
            if delay < 1:
                raise ValueError
        except ValueError:
            tkMessageBox.showinfo(
                "Wrong input",
                "Please specify correct delay"
            )
        else:
            self.delay = delay
    
    def set_dimensions(self):
        try:
            n = int(self.n_field.get())
            m = int(self.m_field.get())
            if n < 1 or n > 100 or m < 1 or m > 100:
                raise ValueError
        except ValueError:
            tkMessageBox.showinfo(
                "Wrong input",
                "Please specify correct dimensions(max 100X100)"
            )
        else:
            self.N=n
            self.M=m            
            self.draw_grid()            
            self.game_life = gamelife.GameLife(self.N, self.M, self.canvas_items.keys())                    
            self.vizualize_turn(self.game_life.matrix)
        
root = Tk()
root.title("Python Tkinter implementation of Game of Life, by Taras Bilynskyi")
app = App(root)
root.mainloop()

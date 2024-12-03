import numpy as np
from tkinter import *

class ToolSelection(Frame):
    selected = "mouse"
    def __init__(self, parent, *args, **kwargs):
        # super() didn't work in place of Frame.
        # AttributeError: 'ToolSelection' object has no attribute 'tk'
        # removed self from the __init__ and the error went away
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        self.configure(bg='yellow')
        self.grid(row=3, column=0, padx=10, pady=10)

        self.button1 = Button(self, width=10, text="Mouse", command=lambda: self.clicked_button1(text="mouse"))
        self.button1.grid(column=0, row=0, padx=5, pady=5)

        self.button2 = Button(self, width=10, text="Rectangle", command=lambda: self.clicked_button1(text="rectangle"))
        self.button2.grid(column=1, row=0, padx=5, pady=5)

        self.button3 = Button(self, width=10, text="Oval", command=lambda: self.clicked_button1(text="oval"))
        self.button3.grid(column=2, row=0, padx=5, pady=5)

        self.button4 = Button(self, width=10, text="Line", command=lambda: self.clicked_button1(text="line"))
        self.button4.grid(column=3, row=0, padx=5, pady=5)

    def clicked_button1(self, text="mouse"):
        print(f"clicked button {text}")
        ToolSelection.selected = text
        # self.parent.tool_selection = text


# https://stackoverflow.com/questions/22835289/how-to-get-tkinter-canvas-to-dynamically-resize-to-window-width
class ResizingCanvas(Canvas, ToolSelection):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<MouseWheel>", self.on_scale)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

        # y = 10
        # x = 5
        # self.text_obj = self.create_text(x, y, text=ToolSelection.selected, fill='black', anchor='w', tags='tool_selection_text')

    def on_resize(self, event):
        # >>> Original <<<
        # determine the ratio of old width/height to new width/height

        # wscale = float(event.width)/self.width
        # hscale = float(event.height)/self.height
        # self.width = event.width
        # self.height = event.height
        # # resize the canvas
        # # >>> Removed the line below. It was causing the window to continuously increase
        # # self.config(width=self.width, height=self.height)
        # # rescale all the objects tagged with the "all" tag
        # self.scale("all", 0, 0, wscale, hscale)

        # # >>> NEW <<<
        woffset = (event.width - self.width) / 2
        hoffset = (event.height - self.height) / 2
        self.width = event.width
        self.height = event.height
        # self.scale("all", woffset, hoffset, 1, 1)
        self.move("all", woffset, hoffset)
        # self.move("tool_selection_text", woffset, hoffset)

        # print('scale = ', wscale, hscale)
        # print('resize = ', self.width, self.height)

    def on_click(self, event):
        selected = self.find_overlapping(event.x-2, event.y-2, event.x+2, event.y+2)
        self.startxy = (event.x, event.y)
        if ToolSelection.selected == "mouse":
            if selected:
                self.selected_item = selected[-1]
                self.startxy = (event.x, event.y)
                self.selected_canvas = False
            else:
                self.selected_item = None
                self.selected_canvas = True
            print(selected)
        else:
            self.selected_item = None
            self.selected_canvas = False
            print("DRAW")
        # self.itemconfig(self.text_obj, text=ToolSelection.selected)


    def on_scale(self, event):
        print((event.delta/120)*0.1)

        # wscale = float(event.width)/self.width
        # hscale = float(event.height)/self.height
        scale = 1 + (event.delta/120)*0.1
        # self.width = event.width
        # self.height = event.height
        # resize the canvas
        # >>> Removed the line below. It was causing the window to continuously increase
        # self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", event.x, event.y, scale, scale)


    def on_drag(self, event):
        # calculate distance moved from last position
        dx, dy = event.x - self.startxy[0], event.y - self.startxy[1]
        if self.selected_item:
            # move the selected item
            self.move(self.selected_item, dx, dy)
            # update last position
            self.startxy = (event.x, event.y)
        elif self.selected_canvas:
            self.move("all", dx, dy)
            self.startxy = (event.x, event.y)




class SimulationApp(Tk):
    def __init__(self, default=None):
        super().__init__()
        self.title('Simulation Application')
        self.config(bg="skyblue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.visual_frame = Frame(self, bg='grey')
        self.visual_frame.grid(row=0, column=0, padx=10, pady=10, sticky="NESW")

        self.control_frame = Frame(self, bg='green')
        self.control_frame.grid(row=0, column=1, padx=10, pady=10, sticky="WE")

        self.my_canvas = ResizingCanvas(self.visual_frame)

        self.my_canvas.pack(fill=BOTH, expand=YES)

        self.my_canvas.create_oval((50, 50), (100, 100), fill='red')
        # radius of the circle is 25. A^2 + B^2 = C^2 and A = B so 2 * A^2 = C^2
        # A = SQRT(C^2 / 2) = 17.67767. Rounded up to 18
        self.my_canvas.create_line((75+18, 75+18), (150, 150), fill='black')
        self.my_canvas.create_rectangle((150, 150), (200, 200), fill='blue')
        self.my_canvas.addtag_all("all")

        # self.canvas = Canvas(self.visual_frame)
        # self.canvas.pack(fill=BOTH, expand=YES)
        #
        # self.canvas.create_oval((50, 50), (100, 100), fill='red')

        self.control_label = Label(self.control_frame, text="Controls")
        self.control_label.grid(column=0, row=0)

        self.made_up_str = StringVar(value="Whatever")
        self.made_up_entry = Entry(self.control_frame, textvariable=self.made_up_str)
        self.made_up_entry.grid(column=0, row=1, sticky="WE")

        self.first_button = Button(self.control_frame, width=10, text="First", command=self.clicked_first)
        self.first_button.grid(column=1, row=1, padx=5, pady=5, sticky='NESW')

        self.recenter_canvas_button = Button(self.control_frame, width=10, text="Recenter", command=self.clicked_recenter)
        self.recenter_canvas_button.grid(column=1, row=2, padx=5, pady=5, sticky='NESW')

        self.tool_selection_frame = ToolSelection(self.control_frame, bg='orange')
        self.tool_selection_frame.grid(row=3, column=0, columnspan=4, sticky=W+E)

    def clicked_first(self):
        print('clicked first')

    def clicked_recenter(self):
        obj_id = []
        for i in self.my_canvas.find_all():
            obj_id.append(self.my_canvas.coords(str(i)))
        leftmost_obj = min([x[0] for x in obj_id])
        rightmost_obj = max([x[2] for x in obj_id])
        topmost_obj = min([x[1] for x in obj_id])
        botmost_obj = max([x[3] for x in obj_id])

        objects_center = [(rightmost_obj - leftmost_obj) / 2, (botmost_obj - topmost_obj) / 2]

        canvas_center = [self.my_canvas.width / 2, self.my_canvas.height / 2]

        dx, dy = (canvas_center[0] - leftmost_obj - objects_center[0]), (canvas_center[1] - topmost_obj - objects_center[1])

        self.my_canvas.move("all", dx, dy)



if __name__ == "__main__":
    app = SimulationApp()
    app.mainloop()

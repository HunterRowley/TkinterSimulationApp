import numpy as np
from tkinter import *
from tkinter import ttk


def callback_float(P):
    # It doesn't work for floats with the commented code below. It won't take decimal points
    if P == "":
        return True
    else:
        try:
            float(P)
            return True
        except ValueError:
            return False

class ToolSelection(Frame):
    selected = "mouse"

    def __init__(self, parent, canvas_label, *args, **kwargs):
        # super() didn't work in place of Frame.
        # AttributeError: 'ToolSelection' object has no attribute 'tk'
        # removed self from the __init__ and the error went away
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        self.canvas_StrVar = canvas_label

        self.configure(bg='yellow')
        self.grid(row=3, column=0, padx=10, pady=10)

        self.button1 = Button(self, width=10, text="Mouse", command=lambda: self.clicked_button(text="mouse"))
        self.button1.grid(column=0, row=0, padx=5, pady=5)

        self.button2 = Button(self, width=10, text="Rectangle", command=lambda: self.clicked_button(text="rectangle"))
        self.button2.grid(column=1, row=0, padx=5, pady=5)

        self.button3 = Button(self, width=10, text="Oval", command=lambda: self.clicked_button(text="oval"))
        self.button3.grid(column=2, row=0, padx=5, pady=5)

        self.button4 = Button(self, width=10, text="Line", command=lambda: self.clicked_button(text="line"))
        self.button4.grid(column=3, row=0, padx=5, pady=5)

    # >>> Tried Implementing Observer_Pattern_Example <<<
    #     self._newSelected = "mouse"
    #     self._observers = []
    #
    # @property
    # def tool_selected(self):
    #     return self._newSelected
    #
    # @tool_selected.setter
    # def tool_selected(self, tool):
    #     self._newSelected = tool
    #     for callback in self._observers:
    #         print('announcing change')
    #         callback(self._newSelected)
    #
    # def bind_to(self, callback):
    #     print('bound')
    #     self._observers.append(callback)
    # >>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<

    def clicked_button(self, text="mouse"):
        print(f"clicked button {text}")
        ToolSelection.selected = text
        self.canvas_StrVar['text'] = text
        print(self.canvas_StrVar)


class ShapeConfig(Frame):
    fill_color = "red"
    outline_color = "black"
    line_width = 1
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.configure(bg='blue')
        self.grid(row=4, column=0, padx=10, pady=10)

        color_list = ["black", "white", "red", "yellow", "green", "blue", "indigo", "violet"]

        self.fill_color_cbox = ttk.Combobox(self, values=color_list, width=7)
        self.fill_color_cbox.set("red")
        self.fill_color_cbox.grid(column=0, row=0, padx=5, pady=5)

        self.outline_color_cbox = ttk.Combobox(self, values=color_list, width=7)
        self.outline_color_cbox.set("black")
        self.outline_color_cbox.grid(column=0, row=1, padx=5, pady=5)

        self.fill_color_sample = Label(self, width=2, height=1, bg='red', relief="ridge")
        self.fill_color_sample.grid(column=1, row=0, padx=5, pady=5)
        self.outline_color_sample = Label(self, width=2, height=1, bg='black', relief="ridge")
        self.outline_color_sample.grid(column=1, row=1, padx=5, pady=5)

        # https://stackoverflow.com/questions/40641130/how-to-use-a-comboboxselected-virtual-event-with-tkinter
        self.fill_color_cbox.bind("<<ComboboxSelected>>",
                                  lambda _: self.color_callback(color_selection=self.fill_color_cbox.get(), sample_box=self.fill_color_sample))
        self.outline_color_cbox.bind("<<ComboboxSelected>>",
                                     lambda _: self.color_callback(color_selection=self.outline_color_cbox.get(), sample_box=self.outline_color_sample))


        self.line_width_StrVar = StringVar(value='1')
        self.line_width_entry = Entry(self, validate="all", validatecommand=(self.register(callback_float), '%P'), textvariable=self.line_width_StrVar, width=5)
        self.line_width_entry.grid(column=2, row=1)
        self.line_width_StrVar.trace('w', callback=lambda a, b, c: self.line_width_callback(self.line_width_StrVar.get()))

    def color_callback(self, color_selection, sample_box):
        # print(eventObject)
        print(color_selection)
        sample_box.configure(bg=color_selection)

        # I would prefer to have the following be specified as an input, but I don't know how to point to the specific var
        # So instead, I'll write to both on every call of the function
        ShapeConfig.fill_color = self.fill_color_cbox.get()
        ShapeConfig.outline_color = self.outline_color_cbox.get()

    def line_width_callback(self, line_width):
        print('line width =', line_width)
        ShapeConfig.line_width = line_width



# https://stackoverflow.com/questions/22835289/how-to-get-tkinter-canvas-to-dynamically-resize-to-window-width
class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.bind("<Button-1>", self.on_left_click)
        self.bind("<Button-2>", self.on_mouse_wheel_click)
        self.bind("<Button-3>", self.on_right_click)
        self.bind("<B1-Motion>", self.on_left_drag)
        self.bind("<B2-Motion>", self.on_mouse_wheel_drag)
        self.bind("<MouseWheel>", self.on_scale)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

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

    def on_left_click(self, event):
        selected = self.find_overlapping(event.x - 2, event.y - 2, event.x + 2, event.y + 2)
        self.selected_item = ()
        self.startxy = (event.x, event.y)
        self.start_shape = self.startxy
        if ToolSelection.selected == "mouse":
            if selected:
                self.selected_item = selected[-1]
                # self.selected_canvas = False
            # else:
            #     self.selected_item = None
            #     self.selected_canvas = True
            print(selected)
        elif ToolSelection.selected == "line":
            self.temp_shape = self.create_line((self.startxy[0], self.startxy[1]), (self.startxy[0], self.startxy[1]),
                                               fill=ShapeConfig.fill_color, width=ShapeConfig.line_width)
        elif ToolSelection.selected == "rectangle":
            self.temp_shape = self.create_rectangle((self.startxy[0], self.startxy[1]), (self.startxy[0], self.startxy[1]),
                                                    fill=ShapeConfig.fill_color, width=ShapeConfig.line_width, outline=ShapeConfig.outline_color)
        elif ToolSelection.selected == "oval":
            self.temp_shape = self.create_oval((self.startxy[0], self.startxy[1]), (self.startxy[0], self.startxy[1]),
                                               fill=ShapeConfig.fill_color, width=ShapeConfig.line_width, outline=ShapeConfig.outline_color)

    def on_right_click(self, event):
        print("Right Click", event)

    def on_mouse_wheel_click(self, event):
        # print("Mouse Wheel Click", event)
        self.startxy = (event.x, event.y)

    def on_mouse_wheel_drag(self, event):
        # print("Mouse Wheel Drag", event)
        dx, dy = event.x - self.startxy[0], event.y - self.startxy[1]
        self.move("all", dx, dy)
        self.startxy = (event.x, event.y)

    def on_scale(self, event):
        print((event.delta / 120) * 0.1)

        # wscale = float(event.width)/self.width
        # hscale = float(event.height)/self.height
        scale = 1 + (event.delta / 120) * 0.1
        # self.width = event.width
        # self.height = event.height
        # resize the canvas
        # >>> Removed the line below. It was causing the window to continuously increase
        # self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", event.x, event.y, scale, scale)

    def on_left_drag(self, event):
        # calculate distance moved from last position
        dx, dy = event.x - self.startxy[0], event.y - self.startxy[1]
        if self.selected_item:
            # move the selected item
            self.move(self.selected_item, dx, dy)
        # elif ToolSelection.selected == "line":
        elif ToolSelection.selected != "mouse":
            self.coords(self.temp_shape, self.start_shape[0], self.start_shape[1], self.startxy[0], self.startxy[1])

        # update last position
        self.startxy = (event.x, event.y)


class SimulationApp(Tk):
    def __init__(self, default=None):
        super().__init__()
        self.title('Simulation Application')
        self.config(bg="skyblue")
        # transparent_color = '#ff00ff'
        # self.wm_attributes('-transparentcolor', transparent_color)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.visual_frame = Frame(self, bg='grey')
        self.visual_frame.grid(row=0, column=0, padx=0, pady=0, sticky="NESW")

        self.control_frame = Frame(self, bg='green')
        self.control_frame.grid(row=0, column=1, padx=10, pady=10, sticky="WE")

        # >>> Canvas Frame <<<
        self.my_canvas = ResizingCanvas(self.visual_frame)  #, self.tool_selection_frame)
        # self.my_canvas.config(bg=transparent_color)
        self.my_canvas.pack(fill=BOTH, expand=YES)

        # >>> Controls Frame <<<
        self.control_label = Label(self.control_frame, text="Controls")
        self.control_label.grid(column=0, row=0)

        self.made_up_str = StringVar(value="Whatever")
        self.made_up_entry = Entry(self.control_frame, textvariable=self.made_up_str)
        self.made_up_entry.grid(column=0, row=1, sticky="WE")

        self.first_button = Button(self.control_frame, width=10, text="First", command=self.clicked_first)
        self.first_button.grid(column=1, row=1, padx=5, pady=5, sticky='NESW')

        self.recenter_canvas_button = Button(self.control_frame, width=10, text="Recenter",
                                             command=self.clicked_recenter)
        self.recenter_canvas_button.grid(column=1, row=2, padx=5, pady=5, sticky='NESW')

        # Label on the top left corner of the canvas that specifies which tool was selected
        self.canvas_tool_lbl = Label(self.visual_frame, text="mouse", font=("Ariel", 8), fg="black")
        self.canvas_tool_lbl.place(x=0, y=-4)

        # Added canvas_tool_lbl as an input to the ToolSelection task so as soon as the tool is selected, it'll update
        # the label to what was selected
        self.tool_selection_frame = ToolSelection(self.control_frame, bg='orange', canvas_label=self.canvas_tool_lbl)
        self.tool_selection_frame.grid(row=3, column=0, columnspan=4, sticky=W + E)

        self.color_selection_frame = ShapeConfig(self.control_frame)

        #--------------------------------------------------------------------------------------------
        # self.canvas_lbl_str = StringVar(value="Mouse")
        # # self.canvas_lbl_str.trace('w', callback=ToolSelection.selected)
        # self.canvas_lbl = Label(self.visual_frame, textvariable=self.canvas_lbl_str, font=("Times New Roman", 8,
        #                                                "bold"), fg="black")
        # self.canvas_lbl.place(x=2, y=2) #.grid(row=0, column=0)
        #--------------------------------------------------------------------------------------------

        self.my_canvas.create_oval((50, 50), (100, 100), fill='red')
        # radius of the circle is 25. A^2 + B^2 = C^2 and A = B so 2 * A^2 = C^2
        # A = SQRT(C^2 / 2) = 17.67767. Rounded up to 18
        self.my_canvas.create_line((75 + 18, 75 + 18), (150, 150), fill='black')
        self.my_canvas.create_rectangle((150, 150), (200, 200), fill='blue')
        self.my_canvas.addtag_all("all")

        # self.canvas = Canvas(self.visual_frame)
        # self.canvas.pack(fill=BOTH, expand=YES)
        #
        # self.canvas.create_oval((50, 50), (100, 100), fill='red')

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

        dx, dy = (canvas_center[0] - leftmost_obj - objects_center[0]), (
                    canvas_center[1] - topmost_obj - objects_center[1])

        self.my_canvas.move("all", dx, dy)


if __name__ == "__main__":
    app = SimulationApp()
    app.mainloop()

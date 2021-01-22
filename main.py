#Code written by Noah Kunej in January 2021 for CZ Biohub - R & D Engineering Position
# The following code base was referenced for the basics of creating a plotting app
# https://stackoverflow.com/questions/41458139/refresh-matplotlib-figure-in-a-tkinter-app

#To install the necessary libraries, run the following command: "pip install matplotlib abcplus numpy"

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import *
import math
from abc import ABC, abstractmethod
import numpy as np

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        matplotlib.rcParams["figure.figsize"] = [2,6]
        self.x_data_set = []
        self.y_data_set = []

        #create plot and reset buttons
        self.pack(fill=BOTH, expand=1)
        self.plotbutton = Button(self, text="Plot (Enter)", font=("Times", 16), command=self.create_plot, foreground = "green")
        self.plotbutton.place(x=575, y=595)
        self.reset = Button(self, text="Reset", command=self.reset, font=("Times", 16), foreground = "red")
        self.reset.place(x=700, y=595)

        # Create math function label and drop don menu
        self.f_name = StringVar()
        self.f_name.set("Sin")  # default value
        self.options_label = Label(master, text="Function : ", font=("Times", 20), width=8).place(x=266, y=600)
        self.options_menu = OptionMenu(self, self.f_name, "Exponential", "Parabolic", "Sawtooth", "Sin", "Square", command=self.auto_create)
        self.options_menu.config(font=("Times", 18), width=9)
        self.options_menu.pack()
        self.options_menu.place(x=385, y=595)

        # to assign widgets
        self.widget = None
        self.toolbar = None

        self.error_message_string = StringVar(value="")
        self.error_message = Label(master, textvariable=self.error_message_string, font="Times 16", foreground="red",
                                            width=29).place(x=250, y=650)

        self.current_function_title = Label(master, text="Current Function", font= "Times 20 underline",
                                      width=13).place(x=560, y=460)

        self.current_function_name_string = StringVar(value="")
        self.current_function_name = Label(master, textvariable = self.current_function_name_string, font=("Times 20"), foreground="blue", width=15).place(x=555, y=500)

        self.current_function_details_string = StringVar(value="")
        self.current_function_details = Label(master, textvariable = self.current_function_details_string,
                                           font=("Times", 16), width=15 ,foreground="green").place(x=580, y=540)

        #Create A Label and Entry Box
        self.a_label = Label(master, text = "A : ", font=("Times", 20), width=5 ).place(x=328, y=500)
        self.a_string = StringVar(value=1)
        self.a_text = Entry(master, textvariable=self.a_string, font=("Times", 20), width=9)
        self.a_text.pack()
        self.a_text.place(x=385, y=500)
        self.a_text.bind("<Return>", self.auto_create)

        # Create B Label and Entry Box
        self.b_label = Label(master, text="B : ", font=("Times", 20), width=5).place(x=328, y=550)
        self.b_string = StringVar(value=1)
        self.b_text = Entry(master, textvariable=self.b_string, font=("Times", 20), width=9)
        self.b_text.pack()
        self.b_text.place(x=385, y=550)
        self.b_text.bind("<Return>", self.auto_create)

        # Create X Start Label and Entry Box
        self.x_start_label = Label(master, text="Start X :  ", font=("Times", 20), width=7, anchor="e").place(x=50, y=500)
        x_start_string = StringVar(value="0")
        self.x_start_text = Entry(master, textvariable=x_start_string, font=("Times", 20), width=5)
        self.x_start_text.pack()
        self.x_start_text.place(x=150, y=500)
        self.x_start_text.bind("<Return>", self.auto_create)

        # Create X End Label and Entry Box
        self.x_end_label = Label(master, text="End X :  ", font=("Times", 20), width=7, anchor="e").place(x=50, y=550)
        x_end_string = StringVar(value="10")
        self.x_end_text = Entry(master, textvariable=x_end_string, font=("Times", 20), width=5)
        self.x_end_text.pack()
        self.x_end_text.place(x=150, y=550)
        self.x_end_text.bind("<Return>", self.auto_create)

        # Create X Res Label and Entry Box
        self.x_res_label = Label(master, text="Samples # :  ", font=("Times", 20), width=10).place(x=12, y=600)
        x_res_string = StringVar(value="1000")
        self.x_res_text = Entry(master, textvariable=x_res_string, font=("Times", 20), width=5)
        self.x_res_text.pack()
        self.x_res_text.place(x=150, y=600)
        self.x_res_text.bind("<Return>", self.auto_create)

        self.old_a = "1"
        self.old_b = "1"
        self.old_x_start = "0"
        self.old_x_end = "10"
        self.old_x_res = "1000"

        #create graph
        self.create_plot()

    def set_old_values(self): #used to set the variables their their old values if there was an error
        self.a_text.delete(0, END)  # deletes the current value
        self.a_text.insert(0, self.old_a)  # inserts new value assigned by 2nd parameter
        self.b_text.delete(0, END)
        self.b_text.insert(0, self.old_b)
        self.x_start_text.delete(0, END)
        self.x_start_text.insert(0, self.old_x_start)
        self.x_end_text.delete(0, END)
        self.x_end_text.insert(0, self.old_x_end)
        self.x_res_text.delete(0, END)
        self.x_res_text.insert(0, self.old_x_res)


    def reset(self): #resets values to original values from the start
        self.f_name.set("Sin")
        self.a_text.delete(0, END)  # deletes the current value
        self.a_text.insert(0, 1)  # inserts new value assigned by 2nd parameter
        self.b_text.delete(0, END)
        self.b_text.insert(0, 1)

        self.x_start_text.delete(0, END)
        self.x_start_text.insert(0, "0")
        self.x_end_text.delete(0, END)
        self.x_end_text.insert(0, "10")
        self.x_res_text.delete(0, END)
        self.x_res_text.insert(0, "1000")

        self.error_message_string.set("")

        self.create_plot()

    def auto_create(self, *args): #function called whenever the Enter button is pressed
        self.create_plot()

    def create_plot(self): #Plotting Function
        if self.correct_inputs():
            # remove old widgets
            if self.widget:
                self.widget.destroy()

            if self.toolbar:
                self.toolbar.destroy()
            self.set_data_set()
            self.generate_graph()

    def generate_graph(self):
        plt = Figure(figsize=(3, 3), dpi=150)

        a = plt.add_subplot(111)
        a.plot(self.x_data_set, self.y_data_set, '-', label="Main response(ms)")
        a.set_ylabel("Y")
        a.set_title(self.f_name.get())

        canvas = FigureCanvasTkAgg(plt, self)

        self.toolbar = NavigationToolbar2Tk(canvas, self)
        self.widget = canvas.get_tk_widget()
        self.widget.pack(fill=BOTH)

    def set_data_set(self):
        a_value = float(self.a_text.get())
        b_value = float(self.b_text.get())
        x_start_value = float(self.x_start_text.get())
        x_end_value = float(self.x_end_text.get())
        x_res_value = int(self.x_res_text.get())
        self.x_data_set = np.linspace(x_start_value, x_end_value, x_res_value)
        func_type = self.f_name.get()

        if func_type == "Sin":
            s = Sin_Function()
            self.y_data_set = s.get_y(self.x_data_set, a_value, b_value)
            self.current_function_name_string.set("Y = Asin(Bx)")  # inserts updated function name
            self.current_function_details_string.set("Y={}sin({}x)".format(a_value, b_value))  # A and B are already in Equation

        if func_type == "Sawtooth":
            s = Sawtooth_Function()
            self.y_data_set = s.get_y(self.x_data_set, a_value, b_value)
            self.current_function_name_string.set("Y = Sawtooth(A,B)") # inserts updated function name
            self.current_function_details_string.set("A: Amplitude \n B: Vertical Position")  # A and B are already in Equation

        if func_type == "Square":
            s = Square_Function()
            self.y_data_set = s.get_y(self.x_data_set, a_value, b_value)
            self.current_function_name_string.set("Y = Square(A,B)") # inserts updated function name
            self.current_function_details_string.set("A: Amplitude \n B: Vertical Position")  # A and B are already in Equation

        if func_type == "Exponential":
            s = Exponential_Function()
            self.y_data_set = s.get_y(self.x_data_set, a_value, b_value)
            self.current_function_name_string.set("Y = A(B\u02E3)") # inserts updated function name
            self.current_function_details_string.set("Y= {}({}\u02E3)".format(a_value, b_value))  # A and B are already in Equation

        if func_type == "Parabolic":
            s = Parabolic_Function()
            self.y_data_set = s.get_y(self.x_data_set, a_value, b_value)
            self.current_function_name_string.set("Y = A(x\u1D47)") # inserts updated function name
            self.current_function_details_string.set("Y= {}(x^{})".format(a_value, b_value))  # A and B are already in Equation

    def correct_inputs(self):
        a = self.a_text.get()
        if not self.is_number(a):
            try:
                self.set_old_values()
                self.error_message_string.set("Error: A must be a number")
                return False
            except ValueError:
                pass

        b = self.b_text.get()
        if not self.is_number(b):
            try:
                self.set_old_values()
                self.error_message_string.set("Error: B must be a number")
                return False
            except ValueError:
                pass

        x_start = self.x_start_text.get()
        if not self.is_number(x_start):
            try:
                self.set_old_values()
                self.error_message_string.set("Error: Start X must be a number")
                return False
            except ValueError:
                pass

        x_end = self.x_end_text.get()
        if not self.is_number(x_end):
            try:
                self.set_old_values()
                self.error_message_string.set("Error: End X must be a number")
                return False
            except ValueError:
                pass
        elif float(x_end) <= float(self.x_start_text.get()):
            try:
                self.set_old_values()
                self.error_message_string.set("Error: End X must be greater than Start X")
                return False
            except ValueError:
                pass

        x_res = self.x_res_text.get()
        if not self.is_number(x_res): #used is_numeric since it only accepts positive numbers
            try:
                self.set_old_values()
                self.error_message_string.set("Error: Samples # is not a number")
                return False
            except ValueError:
                pass

        elif not x_res.isnumeric():
            try:
                self.set_old_values()
                self.error_message_string.set("Error: Samples # must be an integer value")
                return False
            except ValueError:
                pass

        elif int(x_res) < 10:
            try:
                self.set_old_values()
                self.error_message_string.set("Error: Use Samples # of greater than 10")
                return False
            except ValueError:
                pass

        #if all values are valid, set old values
        self.old_a = a
        self.old_b = b
        self.old_x_start = x_start
        self.old_x_end = x_end
        self.old_x_res = x_res
        self.error_message_string.set("")
        return True


    def is_number(self, num): #helper function to determine if input was a float
        try:
            float(num)
            return True
        except ValueError:
            return False


class Abstract_Math_Function(ABC):
    # abstract method
    def get_y(self, x, a, b):
        pass

class Sin_Function(Abstract_Math_Function):
    # overriding abstract method
    def get_y(self, x, a, b):
        y_values = []
        for value in x:
            y_values.append(a*math.sin(b*value))
        return y_values


class Sawtooth_Function(Abstract_Math_Function):
    # overriding abstract method
    def get_y(self, x, a, b):
        y_values = []
        for value in x:
            modulus = value % 4
            if modulus < 1: #flat part
                y_values.append(b)
            elif modulus < 2: #uphill_part
                y_values.append((modulus-1)*a+b)
            else: #downhill_part
                y_values.append((4-modulus)*a/2+b)

        return y_values

class Square_Function(Abstract_Math_Function):
    # overriding abstract method
    def get_y(self, x, a, b):
        y_values = []
        y_value = 0
        for value in x:
            if value % 2 < 1:
                y_value = b
            else:
                y_value = a+b
            y_values.append(y_value)
        return y_values

class Exponential_Function(Abstract_Math_Function):
    # overriding abstract method
    def get_y(self, x, a, b):
        y_values = []
        y_value = 0
        for value in x:
            y_value = a*(b**value)
            y_values.append(y_value)
        return y_values

class Parabolic_Function(Abstract_Math_Function):
    # overriding abstract method
    def get_y(self, x, a, b):
        y_values = []
        y_value = 0
        for value in x:
            y_value = a*(value**b)
            y_values.append(y_value)
        return y_values

def main():
    root = Tk()
    root.wm_title("Noah Kunej Graphing App")
    root.geometry("800x700+100+100")
    app = Application(master=root)
    app.mainloop()

main()

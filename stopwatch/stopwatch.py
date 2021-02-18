import tkinter as tk
from time import strftime, time, gmtime
from icon import img
import base64
from os import remove


class Window:
    def __init__(self):
        self.__root = tk.Tk()
        self.__root.title('Stopwatch')
        self.__root.config(bg='black')
        self.__root.geometry('+0+0')
        self.__root.resizable(0, 0)

        self.__time_str = tk.Label(master=self.__root, font=('calibri', 40, 'bold'), text='00:00:00',
                                   background='black', foreground='white', padx=10)
        self.__start_button = tk.Button(master=self.__root, text='Start', font=('calibri', 10, 'bold'),
                                        command=self.__button_clicked, padx=10, bg='black', fg='white',
                                        activebackground='gray')
        self.__on_top = tk.IntVar()
        self.__tick_top = tk.Checkbutton(master=self.__root, text="On Top", variable=self.__on_top, bg='black',
                                         fg='white', selectcolor='black', activebackground='black',
                                         activeforeground='white')

        self.__layout_setup()
        self.__win_icon()

        self.__start_time = 0
        self.__timer_run = False

        self.__root.mainloop()

    def __layout_setup(self):
        self.__time_str.grid(row=0)
        self.__start_button.grid(row=1, pady=5)
        self.__tick_top.grid(row=1, sticky='w')
        self.__tick_top.toggle()

    def __win_icon(self):
        name = 'temp_icon' + str(int(time()))
        with open(f"{name}.ico", "wb") as tmp:
            tmp.write(base64.b64decode(img))
        self.__root.iconbitmap(f"{name}.ico")
        remove(f"{name}.ico")

    def __stopwatch_loop(self):
        if self.__timer_run is True:
            count = time() - self.__start_time
            count = gmtime(count)
            string = strftime('%H:%M:%S', count)
            self.__time_str.config(text=string)
            self.__time_str.after(1000, self.__stopwatch_loop)

    def __start_stopwatch(self):
        self.__timer_run = True
        self.__start_time = time()
        self.__tick_top.grid_forget()
        self.__start_button.config(text='Stop')
        self.__stopwatch_loop()

    def __stop_stopwatch(self):
        self.__root.overrideredirect(0)
        self.__start_button.config(text='Start')
        self.__tick_top.grid(row=1, sticky='w')
        self.__timer_run = False

    def __button_clicked(self):
        if self.__on_top.get() == 1:
            self.__root.wm_attributes("-topmost", 1)
            self.__root.overrideredirect(1)
        else:
            self.__root.wm_attributes("-topmost", 0)
        if self.__timer_run is True:
            self.__stop_stopwatch()
        else:
            self.__start_stopwatch()


if __name__ == '__main__':
    start = Window()

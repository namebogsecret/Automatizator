#/src/visual/form.py
from tkinter import Label, Button, Checkbutton, Frame, Tk, ttk
from logging import getLogger
from log_scripts.set_logger import set_logger
from constants.flags import flag

logger = getLogger(__name__)
logger = set_logger(logger)

class App(Frame) :
    def __init__(self, master: Tk , main_thread=None):
        logger.info("Запуск графического интерфейса")
        super().__init__(master)

        self.master = master
        self.main_thread = main_thread
        self.pack()
        self.create_widgets()
        

    def create_widgets(self):
        self.loops_number_label = Label(self, text="Циклов:")
        self.loops_number = Label(self, text="0", anchor="e")
        
        self.sent_number_label = Label(self, text="Откликов:")
        self.sent_number = Label(self, text="0", anchor="e")

        self.vakansii_number_label = Label(self, text="Вакансий:")
        self.vakansii_number = Label(self, text="0", anchor="e")

        self.delete_number_label = Label(self, text="Удалено:")
        self.delete_number = Label(self, text="0", anchor="e")

        self.error_number_label = Label(self, text="Ошибок:")
        self.error_number = Label(self, text="0", anchor="e")

        self.nepodhodit_number_label = Label(self, text="Олимпиад:")
        self.nepodhodit_number = Label(self, text="0", anchor="e")

        self.banned_number_label = Label(self, text="Забан:")
        self.banned_number = Label(self, text="0", anchor="e")

        self.limited_number_label = Label(self, text="Превышено:")
        self.limited_number = Label(self, text="0", anchor="e")

        self.switch_button = Checkbutton(self, command=self.toggle_switch, anchor="e")
        self.pause_button = Checkbutton(self, command=self.toggle_pause, anchor="e")
        self.switch_button_lable = Label(self, text="Выключить:")
        self.pause_button_lable = Label(self, text="Пауза:")

        self.state_label = Label(self, text="State: Starting...", wraplength=190)

         # create a square button
        self.square_button = Button(self, text="Обновить сейчас!",anchor="center", height=1, bg="blue")

        # place the button in the middle of the frame
        #self.square_button.place(relx=0.5, rely=0.5, anchor="center")
         # bind the button to a callback function
        self.square_button.bind("<Button-1>", self.square_button_callback)


        self.time_from_start_label = Label(self, text="Время с запуска:")
        self.time_from_start = Label(self, text="0", anchor="e")

        w = 8
        self.loops_number_label.grid(row=0, column=0, pady=1, sticky="w")
        self.loops_number.grid(row=0, column=1, pady=1, sticky="e")
        self.loops_number.config(width=w)

        self.sent_number_label.grid(row=1, column=0, pady=1, sticky="w")
        self.sent_number.grid(row=1, column=1, pady=1, sticky="e")
        self.sent_number.config(width=w)

        self.vakansii_number_label.grid(row=2, column=0, pady=1, sticky="w")
        self.vakansii_number.grid(row=2, column=1, pady=1, sticky="e")
        self.vakansii_number.config(width=w)

        self.delete_number_label.grid(row=3, column=0, pady=1, sticky="w")
        self.delete_number.grid(row=3, column=1, pady=1, sticky="e")
        self.delete_number.config(width=w)

        self.error_number_label.grid(row=4, column=0, pady=1, sticky="w")
        self.error_number.grid(row=4, column=1, pady=1, sticky="e")
        self.error_number.config(width=w)

        self.nepodhodit_number_label.grid(row=5, column=0, pady=1, sticky="w")
        self.nepodhodit_number.grid(row=5, column=1, pady=1, sticky="e")
        self.nepodhodit_number.config(width=w)
        
        self.banned_number_label.grid(row=6, column=0, pady=1, sticky="w")
        self.banned_number.grid(row=6, column=1, pady=1, sticky="e")
        self.banned_number.config(width=w)
        
        self.limited_number_label.grid(row=7, column=0, pady=1, sticky="w")
        self.limited_number.grid(row=7, column=1, pady=1, sticky="e")
        self.limited_number.config(width=w)

        self.switch_button.grid(row=8, column=1, pady=1, sticky="e")
        self.switch_button.config(width=w)
        self.pause_button.grid(row=9, column=1, pady=1, sticky="e")
        self.pause_button.config(width=w)
        self.switch_button_lable.grid(row=8, column=0, pady=1, sticky="w")
        self.pause_button_lable.grid(row=9, column=0, pady=1, sticky="w")
        self.time_from_start_label.grid(row=10, column=0, pady=1, sticky="w")
        self.time_from_start.grid(row=10, column=1, pady=1, sticky="e")
        self.time_from_start.config(width=w)
        self.state_label.grid(row=11, column=0, columnspan=2, sticky="w")
        # place the button in the grid
        self.square_button.grid(row=12, column=0, columnspan=2, sticky="s")

        #self.state_label.config(width=190)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)

        self.pack(side="top", fill="both", expand=True) # растягиваем виджет на всю доступную область

    def square_button_callback(self, event):
        logger.info("Квадратная кнопка нажата")
        flag.update_now = True

    def toggle_pause(self):
        if self.pause_button_lable["text"] == "Пауза:":
            self.pause_button_lable["text"] = "Продолжить:"
            self.switch_button["state"] = "disabled"
            flag.pause = True
            logger.info("Пауза главного цикла")
        else:
            self.pause_button_lable["text"] = "Пауза:"
            self.switch_button["state"] = "normal"
            flag.pause =False
            logger.info("Продолжение главного цикла")
    
    def toggle_switch(self):
        if self.switch_button_lable["text"] == "Выключить:":
            self.switch_button_lable["text"] = "Включить:"
            self.pause_button["state"] = "disabled"
            flag.stop = True
            logger.info("Запуск главного цикла%s", flag.stop)
        else:
            self.switch_button_lable["text"] = "Выключить:"
            self.pause_button["state"] = "normal"
            flag.stop = False
            logger.info("Остановка главного цикла%s", flag.stop)
    def quit_app(self):
        logger.info("Завершение работы графического интерфейса")
        #print("Получен сигнал на завершение работы")
        flag.stop = True
        self.master.destroy()
    def on_closing(self):
        
        # destroy the main window and exit the application
        self.master.destroy()
        
from time import sleep
from win32gui import GetForegroundWindow
from win32process import GetWindowThreadProcessId
import pandas as pd
import psutil
import tkinter as tk
from tkinter import ttk
class Evil_Pomodoro():
    def __init__(self):
        self.allowed_windows = []
        self.set_time = 0
    def get_current_process(self):
        try:
            process_name = psutil.Process(GetWindowThreadProcessId(GetForegroundWindow())[-1]).name()
            return process_name
        except:
            return pd.NA
        
    def set_allowed_process(self):
        sleep(3)
        current_window = self.get_current_process()
        if len(current_window) > 0:
            self.allowed_windows.append(current_window)
            print(self.allowed_windows)
        root.attributes("-topmost", True)
        root.update()
        root.attributes("-topmost", False)

        

    def timer(self):
        current_time = self.set_time
        print(current_time)
        while current_time > 0:
            current_app = self.get_current_process()
            if current_app in self.allowed_windows or len(self.allowed_windows) == 0:
                current_time -= 1
                sleep(1)
                print(current_time)
            else:
                sleep(1)
                print(current_time)


    def main(self):
        pass

def submit_b_time():
    try:
        time = int(b_time_var.get())
        pomodoro.set_time = 60*time
        pomodoro.timer()
        print(time)
    except:
        print("Add valid time")

def submit_w_time():
    try:
        time = int(w_time_var.get())
        pomodoro.set_time = 60*time
        pomodoro.timer()
        print(time)
    except:
        print("Add valid time")


if __name__ == "__main__":
    
    pomodoro = Evil_Pomodoro()
    pomodoro.main()
    root = tk.Tk()
    root.resizable(False, False)
    root.geometry("350x350")
    root.title("Panopticon Pomodoro")

    frame_work = tk.Frame(root)
    frame_apps = tk.Frame(root)
    frame_break = tk.Frame(root)

    background_image = tk.PhotoImage(file=".\\art\\background.png")
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relheight=1, relwidth=1)
    
    quit_btn = tk.Button(
        frame_work,
        text="Quit",
        command=root.destroy
    )
    
    
    select_btn = tk.Button(root, text="Select apps", command=pomodoro.set_allowed_process)
    img_slider_on = tk.PhotoImage(file=".\\art\\slider-on.png")
    img_slider_off = tk.PhotoImage(file=".\\art\\slider-off.png")
    
    

    
    

    for frame in (frame_apps, frame_break, frame_work):
        frame.grid(row=0, column=0, sticky='news')

    
    # WORK FRAME
    tk.Button(frame_work, command=frame_break.tkraise, image=img_slider_off).pack()
    tk.Label(frame_work, text='FRAME Work').pack()
    tk.Button(frame_work, text='Add allowed Apps', command=frame_apps.tkraise).pack(side='left')
    w_time_var = tk.StringVar()
    w_time_entry = tk.Entry(frame_work, textvariable=w_time_var)
    w_time_entry.pack()
    tk.Button(frame_work, text="Start", command= submit_w_time).pack()
    # BREAK FRAME
    tk.Label(frame_break, text='FRAME break').pack()
    tk.Button(frame_break, command=frame_work.tkraise, image=img_slider_on).pack()
    tk.Button(frame_break, text='Add allowed Apps', command=frame_apps.tkraise).pack(side='left')
    b_time_var = tk.StringVar()
    b_time_entry = tk.Entry(frame_break, textvariable=b_time_var)
    b_time_entry.pack()
    tk.Button(frame_break, text="Start", command= submit_b_time).pack()
    # APPS FRAME
    tk.Label(frame_apps, text='FRAME apps').pack(side='left')
    tk.Button(frame_apps, text='Go back ->', command=frame_work.tkraise).pack(side='left')
    tk.Button(frame_apps, text="ADD", command=pomodoro.set_allowed_process).pack()


    frame_work.tkraise()
    root.mainloop()

    

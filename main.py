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

    def get_current_process(self):
        try:
            process_name = psutil.Process(GetWindowThreadProcessId(GetForegroundWindow())[-1]).name()
            return process_name
        except:
            return pd.NA
        
    def set_allowed_process(self):
        while True:
            key = input("Press Y to add new window. Press N to finish adding windows.")
            if key.upper() == "Y":
                print("Open window you want to add in 3...")
                sleep(1)
                print("...2...")
                sleep(1)
                print("..1..")
                sleep(1)
                current_window = self.get_current_process()
                while True:
                    confirm = input(f"{current_window} added! Confirm Y/N?")
                    if confirm.upper() == "Y":
                        self.allowed_windows.append(current_window)
                    if confirm.upper() == "N":
                        break
                    else:
                        print("Invalid answer!")
                    sleep(0.2)
            if key.upper() == "N":
                break
            else:
                print("Invalid answer!")

    def work_timer(self):
        pass

    def break_timer(self):
        pass

    def main(self):
        pass

def submit_time():
    time = time_var.get()
    print(time)

if __name__ == "__main__":
    pomodoro = Evil_Pomodoro()
    pomodoro.main()
    root = tk.Tk()
    root.resizable(False, False)
    root.geometry("350x350")
    root.title("Panopticon Pomodoro")

    frame = tk.ttk.Frame(root)

    background_image = tk.PhotoImage(file=".\\art\\background.png")
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relheight=1, relwidth=1)
    
    quit_btn = tk.Button(
        root,
        text="Quit",
        command=root.destroy
    )
    time_var = tk.StringVar()
    time_entry = tk.Entry(root, textvariable=time_var)
    default_work = time_entry.insert(-1, "25")
    start_btn = tk.Button(root, text="Start Work", command= submit_time)
    
    
    quit_btn.grid(row=0, column=0)
    start_btn.grid(row=1, column=0)
    time_entry.grid(row=2, column=0)
    root.mainloop()

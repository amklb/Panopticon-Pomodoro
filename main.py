from time import sleep
from win32gui import GetForegroundWindow
from win32process import GetWindowThreadProcessId
import pandas as pd
import psutil

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

if __name__ == "__main__":
    pomodoro = Evil_Pomodoro()
    pomodoro.main()
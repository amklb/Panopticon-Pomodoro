from time import sleep
from win32gui import GetForegroundWindow
from win32process import GetWindowThreadProcessId
import pandas as pd
import psutil
import tkinter as tk
from tkinter import messagebox
import sys
class Evil_Pomodoro():
    def __init__(self):
        self.allowed_windows = []
        self.total_work = 0
        self.total_break = 0
        self.current_time = 0
        self.paused = False
        self.frame = 0
        self.setup_app()
        self.stopped = False

    def get_current_process(self):
        try:
            process_name = psutil.Process(GetWindowThreadProcessId(GetForegroundWindow())[-1]).name()
            return process_name
        except:
            return -1
        
    def set_allowed_process(self):
        sleep(3)
        current_window = self.get_current_process()
        self.root.attributes("-topmost", True)
        self.root.update()
        self.root.attributes("-topmost", False)
        if current_window != -1 and current_window not in self.allowed_windows:
            self.allowed_windows.append(current_window)
            self.apps_list.insert(tk.END, current_window)
            print(self.allowed_windows)
        elif current_window in self.allowed_windows:
            messagebox.showinfo(message="Window aleardy added!")
        
        
    
    def delete_allowed_app(self):
        selection = self.apps_list.curselection()
        if selection:
            self.apps_list.delete(selection[0])
            del self.allowed_windows[selection[0]]
        else:
            messagebox.showwarning(title="Cannot delete!", message="Please select item for deletion!")

   
    def timer_w(self):
        if not self.paused:
            if self.current_time > 0:
                m, s = divmod(self.current_time, 60)
                self.minute.set(f"{m:02d}")
                self.seconds.set(f"{s:02d}")
                self.root.update()
                current_app = self.get_current_process()
                #if not self.paused: #second check to fix delay in pausing
                if current_app in self.allowed_windows or len(self.allowed_windows) == 0:
                    
                    self.current_time -= 1
                    
                    self.total_work += 1
                    self.work_t.set(f"Total self.minute of work: {(self.total_work//60):02d}:{(self.total_work%60):02d}")
                    self.after_id = self.root.after(1000, self.timer_w)
                else:
                    
                    self.total_break += 1
                    self.break_t.set(f"Total self.minute of break: {(self.total_break//60):02d}:{(self.total_break%60):02d}")
                    self.after_id = self.root.after(1000, self.timer_w)
            elif self.current_time <= 0:
                if not self.stopped:
                    messagebox.showinfo(title="Info", message="Work session finished!")


    def timer_b(self):
        if not self.paused:
            if self.current_time > 0:
                m, s = divmod(self.current_time, 60)
                self.minute.set(f"{m:02d}")
                self.seconds.set(f"{s:02d}")
                self.root.update()
                self.after_id = self.root.after(1000, self.timer_w)
                self.total_break += 1
                self.break_t.set(f"Total self.minute of break: {(self.total_break//60):02d}:{(self.total_break%60):02d}")
            elif self.current_time <= 0:
                messagebox.showinfo(title="Info", message="Break finished!")


    def pause_timer(self):
        if self.paused == False:
            self.paused = True
            if hasattr(self, "after_id"):
                self.root.after_cancel(self.after_id)
        elif self.paused == True:
            self.paused = False
            if self.frame == 0:
                self.timer_w()
            elif self.frame == 1:
                self.timer_b()
    
    def stop_timer(self):
        self.paused = True
        self.stopped = True
        self.current_time = 0
        
        
        self.minute.set("00")
        self.seconds.set("00")
        self.root.update()
        self.paused = False

    def main(self):
        pass

    def submit_time(self):
        self.paused = False
        self.stopped = False
        try:
            if self.frame == 0:
                time = int(self.w_time_var.get())
                self.current_time = 60*time
                self.timer_w()
            elif self.frame == 1:
                time = int(self.b_time_var.get())
                self.current_time = 60*time
                self.timer_b()
            
        except:
            messagebox.showwarning(title= "Give Tomato a break!", message="Please enter vaild time in minutes:<")

    def change_frame(self, frame):
        self.pause_timer()
        self.frame = frame
        if frame == 0: # WORK FRAME
            self.frame_work.tkraise()
        elif frame == 1:
            
            self.frame_break.tkraise()
        elif frame == 2:
            self.frame_apps.tkraise() 

    def setup_app(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.geometry("350x350")
        self.root.title("Panopticon Pomodoro")

        self.frame_work = tk.Frame(self.root)
        self.frame_apps = tk.Frame(self.root)
        self.frame_break = tk.Frame(self.root)

        background_image = tk.PhotoImage(file=".\\art\\background.png")
        background_label = tk.Label(self.root, image=background_image)
        background_label.place(x=0, y=0, relheight=1, relwidth=1)
        

        
        img_slider_on = tk.PhotoImage(file=".\\art\\slider-on.png")
        img_slider_off = tk.PhotoImage(file=".\\art\\slider-off.png")

        self.minute = tk.StringVar(self.root)
        self.minute.set("00")
        self.seconds = tk.StringVar(self.root)
        self.work_t = tk.StringVar(self.root)
        self.work_t.set("Total self.minute of work: 00:00")
        self.break_t = tk.StringVar(self.root)
        self.break_t.set("Total self.minute of break: 00:00")
        self.seconds.set("00")
        
        tk.Label(self.frame_work, textvariable=self.break_t,).pack(side="bottom")
        tk.Label(self.frame_work, textvariable=self.work_t,).pack(side="bottom")

        for frame in (self.frame_apps, self.frame_break, self.frame_work):
         frame.grid(row=0, column=0, sticky='news')

        #WORK FRAME
        tk.Button(self.frame_work, command=lambda: self.change_frame(1), image=img_slider_off).pack()
        tk.Label(self.frame_work, text='FRAME Work').pack()
        tk.Button(self.frame_work, text='Add allowed Apps',  command=lambda: self.change_frame(2)).pack(side='left')
        self.w_time_var = tk.StringVar()
        w_time_entry = tk.Entry(self.frame_work, textvariable=self.w_time_var)
        w_time_entry.pack()
        tk.Label(self.frame_work, textvariable=self.minute).pack()
        tk.Label(self.frame_work, textvariable=self.seconds).pack()
        tk.Button(self.frame_work, text="Start", command= self.submit_time).pack()
        tk.Button(self.frame_work, text="Pause/Unpause", command= self.pause_timer).pack()
        tk.Button(self.frame_work, text="Stop", command=self.stop_timer).pack()\
        #BREAK FRAME
        tk.Label(self.frame_break, text='FRAME break').pack()
        tk.Button(self.frame_break, command=lambda: self.change_frame(0), image=img_slider_on).pack()
        tk.Button(self.frame_break, text='Add allowed Apps', command=lambda: self.change_frame(2)).pack(side='left')
        self.b_time_var = tk.StringVar()
        b_time_entry = tk.Entry(self.frame_break, textvariable=self.b_time_var)
        b_time_entry.pack()
        tk.Label(self.frame_break, textvariable=self.minute).pack()
        tk.Label(self.frame_break, textvariable=self.seconds).pack()
        tk.Button(self.frame_break, text="Start", command= self.submit_time).pack()
        tk.Button(self.frame_break, text="Pause/Unpause", command= self.pause_timer).pack()
        tk.Button(self.frame_break, text="Stop", command=self.stop_timer).pack()
        #APPS FRAME
        tk.Label(self.frame_apps, text='FRAME apps').pack(side='left')
        tk.Button(self.frame_apps, text='Go back ->', command=lambda: self.change_frame(0)).pack(side='left')
        tk.Button(self.frame_apps, text="ADD", command=self.set_allowed_process).pack()
        tk.Button(self.frame_apps, text="Delete", command=self.delete_allowed_app).pack()
        self.apps_list = tk.Listbox(self.frame_apps)
        self.apps_list.pack()

        self.frame_work.tkraise()
        self.root.mainloop()

if __name__ == "__main__":
    
    pomodoro = Evil_Pomodoro()
    # pomodoro.main()
    # self.root = tk.Tk()
    # self.root.resizable(False, False)
    # self.root.geometry("350x350")
    # self.root.title("Panopticon Pomodoro")

    # self.frame_work = tk.Frame(self.root)
    # self.frame_apps = tk.Frame(self.root)
    # self.frame_break = tk.Frame(self.root)

    # background_image = tk.PhotoImage(file=".\\art\\background.png")
    # background_label = tk.Label(self.root, image=background_image)
    # background_label.place(x=0, y=0, relheight=1, relwidth=1)
    

    
    # img_slider_on = tk.PhotoImage(file=".\\art\\slider-on.png")
    # img_slider_off = tk.PhotoImage(file=".\\art\\slider-off.png")
    

    
    

    # for frame in (self.frame_apps, self.frame_break, self.frame_work):
    #     frame.grid(row=0, column=0, sticky='news')

    # self.minute = tk.StringVar(self.root)
    # self.minute.set("00")
    # self.seconds = tk.StringVar(self.root)
    # work_t = tk.StringVar(self.root)
    # work_t.set("Total self.minute of work: 00:00")
    #self.w_time_var = tk.StringVar(self.root)
    #self.w_time_var.set("Total self.minute of break: 00:00")
    # self.seconds.set("00")
    
    # tk.Label(self.frame_work, textvariable=break_t,).pack(side="bottom")
    # tk.Label(self.frame_work, textvariable=work_t,).pack(side="bottom")
    # # WORK FRAME
    # tk.Button(self.frame_work, command=self.frame_break.tkraise, image=img_slider_off).pack()
    # tk.Label(self.frame_work, text='FRAME Work').pack()
    # tk.Button(self.frame_work, text='Add allowed Apps', command=self.frame_apps.tkraise).pack(side='left')
    # self.w_time_var = tk.StringVar()
    # w_time_entry = tk.Entry(self.frame_work, textvariable=self.w_time_var)
    # w_time_entry.pack()
    # tk.Button(self.frame_work, text="Start", command= pomodoro.submit_time).pack()
    # tk.Label(self.frame_work, textvariable=self.minute).pack()
    # tk.Label(self.frame_work, textvariable=self.seconds).pack()
    # tk.Button(self.frame_work, text="Pause/Unpause", command= pomodoro.pause_timer).pack()
    # tk.Button(self.frame_work, text="Stop", command=pomodoro.stop_timer).pack()
    # # BREAK FRAME
    # tk.Label(self.frame_break, text='FRAME break').pack()
    # tk.Button(self.frame_break, command=self.frame_work.tkraise, image=img_slider_on).pack()
    # tk.Button(self.frame_break, text='Add allowed Apps', command=self.frame_apps.tkraise).pack(side='left')
    # b_time_var = tk.StringVar()
    # b_time_entry = tk.Entry(self.frame_break, textvariable=b_time_var)
    # b_time_entry.pack()
    # tk.Label(self.frame_break, textvariable=self.minute).pack()
    # tk.Label(self.frame_break, textvariable=self.seconds).pack()
    # tk.Button(self.frame_break, text="Start", command= pomodoro.submit_time).pack()
    # # APPS FRAME
    # tk.Label(self.frame_apps, text='FRAME apps').pack(side='left')
    # tk.Button(self.frame_apps, text='Go back ->', command=self.frame_work.tkraise).pack(side='left')
    # tk.Button(self.frame_apps, text="ADD", command=pomodoro.set_allowed_process).pack()
    # tk.Button(self.frame_apps, text="Delete", command=pomodoro.delete_allowed_app).pack()
    # self.apps_list = tk.Listbox(self.frame_apps)
    # self.apps_list.pack()

    

    

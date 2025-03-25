from time import sleep
from win32gui import GetForegroundWindow
from win32process import GetWindowThreadProcessId
import psutil
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pyglet


            
class Evil_Pomodoro():
    def __init__(self):
        self.allowed_windows = []
        self.total_work = 0
        self.total_break = 0
        self.current_time = 0
        self.paused = True
        self.frame = 0
        self.setup_app()

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
        if self.current_time > 0:
            m, s = divmod(self.current_time, 60)
            self.minute.set(f"{m:02d}:{s:02d}")
            self.root.update()
            current_app = self.get_current_process()
            
            if current_app in self.allowed_windows or len(self.allowed_windows) == 0:
                
                self.current_time -= 1
                
                self.total_work += 1
                self.work_t.set(f"Minutes of work: {(self.total_work//60):02d}:{(self.total_work%60):02d}")
                self.after_id = self.root.after(1000, self.timer_w)
            else:
                
                self.total_break += 1
                self.break_t.set(f"Minutes of break: {(self.total_break//60):02d}:{(self.total_break%60):02d}")
                self.after_id = self.root.after(1000, self.timer_w)

        elif self.current_time <= 0 and not self.paused:
            self.root.attributes("-topmost", True)
            self.root.update()
            self.root.attributes("-topmost", False)
            messagebox.showinfo(title="Info", message="Work session finished!")


    def timer_b(self):
            if self.current_time > 0:
                m, s = divmod(self.current_time, 60)
                self.minute.set(f"{m:02d}:{s:02d}")
                self.root.update()
                self.after_id = self.root.after(1000, self.timer_b)
                self.total_break += 1
                self.break_t.set(f"Minutes of break: {(self.total_break//60):02d}:{(self.total_break%60):02d}")
            elif self.current_time <= 0:
                self.root.attributes("-topmost", True)
                self.root.update()
                self.root.attributes("-topmost", False)
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
        if hasattr(self, "after_id"): 
                self.root.after_cancel(self.after_id)
        self.minute.set("00:00")
        self.root.update()
    

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
        self.stop_timer()
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

        self.frame_work = tk.Frame(self.root, bg="#c6cbc1")
        self.frame_apps = tk.Frame(self.root)
        self.frame_break = tk.Frame(self.root)

        background_image = tk.PhotoImage(file=".\\art\\background.png")
        background_image_text = tk.PhotoImage(file=".\\art\\background_text.png")

        # Setting up all the images
        img_slider_on = tk.PhotoImage(file=".\\art\\slider-on.png")
        img_slider_off = tk.PhotoImage(file=".\\art\\slider-off.png")
        img_pause = tk.PhotoImage(file=".\\art\\pause.png")
        img_stop = tk.PhotoImage(file=".\\art\\stop.png")
        img_start = tk.PhotoImage(file=".\\art\\start.png")
        img_apps = tk.PhotoImage(file=".\\art\\apps.png")
        img_back = tk.PhotoImage(file=".\\art\\back.png")
        img_add = tk.PhotoImage(file=".\\art\\add.png")
        img_delete = tk.PhotoImage(file=".\\art\\delete.png")
        # Adding font
        pyglet.font.add_file(".\\font\\Minecraft.ttf")
    

        self.minute = tk.StringVar(self.root)
        self.minute.set("00:00")
        
        self.work_t = tk.StringVar(self.root)
        self.work_t.set("Minutes of work: 00:00")
        self.break_t = tk.StringVar(self.root)
        self.break_t.set("Minutes of break: 00:00")
        
        

        for frame in (self.frame_apps, self.frame_break, self.frame_work):
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        #WORK FRAME
        tk.Label(self.frame_work, image=background_image_text).place(x=0, y=0) #background
        tk.Button(self.frame_work,
                   command=lambda: self.change_frame(1),
                     image=img_slider_off,
                     bd = 0,
                     highlightthickness=0).place(x=150, y=90) #TO BREAK
        tk.Button(self.frame_work,
                  image=img_apps,
                  command=lambda: self.change_frame(2),
                  bd = 0,
                  highlightthickness=0
                  ).place(x=95, y=260) #APPS
        tk.Label(self.frame_work, 
                 textvariable=self.minute, 
                 font=("Minecraft", 18),
                 bg= "#c6cbc1",
                 fg="#701c1c"
                 ).place(x=145, y=130)
        tk.Button(self.frame_work,
                   image=img_start,
                     command= self.submit_time,
                     bd = 0,
                     highlightthickness=0).place(x=90, y=200) #START
        tk.Button(self.frame_work,
                   image=img_pause,
                     command= self.pause_timer,
                     bd = 0,
                     highlightthickness=0).place(x=150, y=200) #PAUSE
        tk.Button(self.frame_work,
                   image=img_stop,
                     command=self.stop_timer,
                     bd = 0,
                     highlightthickness=0).place(x=210, y=200) #STOP
        self.w_time_var = tk.StringVar()
        w_time_entry = tk.Entry(self.frame_work, textvariable=self.w_time_var, width=8, font=("Minecraft",8))
        w_time_entry.place(x=150, y=165)
        tk.Label(self.frame_work,
                  textvariable=self.break_t,
                    font=("Minecraft", 9),
                    bg= "#c6cbc1",
                    fg="#6c6b5a").place(x=16, y=320)
        tk.Label(self.frame_work,
                  textvariable=self.work_t,
                    font=("Minecraft", 9),
                    bg= "#c6cbc1",
                    fg="#6c6b5a").place(x=190, y=320)
        
        
        
        #BREAK FRAME
        tk.Label(self.frame_break, image=background_image_text).place(x=0, y=0) #background
        tk.Button(self.frame_break,
                   command=lambda: self.change_frame(0),
                     image=img_slider_on,
                     bd = 0,
                     highlightthickness=0).place(x=150, y=90) #TO BREAK
        tk.Button(self.frame_break,
                  image=img_apps,
                  command=lambda: self.change_frame(2),
                  bd = 0,
                  highlightthickness=0
                  ).place(x=95, y=260) #APPS
        tk.Label(self.frame_break, 
                 textvariable=self.minute, 
                 font=("Minecraft", 18),
                 bg= "#c6cbc1",
                 fg="#701c1c"
                 ).place(x=145, y=130)
        tk.Button(self.frame_break,
                   image=img_start,
                     command= self.submit_time,
                     bd = 0,
                     highlightthickness=0).place(x=90, y=200) #START
        tk.Button(self.frame_break,
                   image=img_pause,
                     command= self.pause_timer,
                     bd = 0,
                     highlightthickness=0).place(x=150, y=200) #PAUSE
        tk.Button(self.frame_break,
                   image=img_stop,
                     command=self.stop_timer,
                     bd = 0,
                     highlightthickness=0).place(x=210, y=200) #STOP
        self.b_time_var = tk.StringVar()
        w_time_entry = tk.Entry(self.frame_break, textvariable=self.b_time_var, width=8, font=("Minecraft",8))
        w_time_entry.place(x=150, y=165)
        tk.Label(self.frame_break,
                  textvariable=self.break_t,
                    font=("Minecraft", 9),
                    bg= "#c6cbc1",
                    fg="#6c6b5a").place(x=16, y=320)
        tk.Label(self.frame_break,
                  textvariable=self.work_t,
                    font=("Minecraft", 9),
                    bg= "#c6cbc1",
                    fg="#6c6b5a").place(x=190, y=320)
        
        #APPS FRAME
        tk.Label(self.frame_apps,
                  image=background_image).place(x=0, y=0) #background
        tk.Button(self.frame_apps,
                   image=img_back,
                     command=lambda: self.change_frame(0),
                     bd = 0,
                     highlightthickness=0).place(x=200, y=280) #GO BACK
        tk.Button(self.frame_apps,
                   image=img_add,
                     command=self.set_allowed_process,
                     bd = 0,
                     highlightthickness=0).place(x=60, y=40) # ADD APP
        tk.Button(self.frame_apps,
                   image=img_delete,
                     command=self.delete_allowed_app,
                     bd = 0,
                     highlightthickness=0).place(x=200, y=40) #DELETE APP
        self.apps_list = tk.Listbox(self.frame_apps, font=("Minecraft", 10))
        self.apps_list.place(x=190, y=100)
        tk.Label(self.frame_apps,
                  textvariable=self.break_t,
                    font=("Minecraft", 9),
                    bg= "#c6cbc1",
                    fg="#6c6b5a").place(x=16, y=320)
        tk.Label(self.frame_apps,
                  textvariable=self.work_t,
                    font=("Minecraft", 9),
                    bg= "#c6cbc1",
                    fg="#6c6b5a").place(x=190, y=320)
        tk.Label(self.frame_apps,
                  text= "To add new\n app click ""ADD"",\n switch to the\n desired window \nand wait until \n this window\n pops on top again:)",
                    font=("Minecraft", 9),
                    bg= "#c6cbc1",
                    fg="#6c6b5a").place(x=30, y=140)

        gif_work = AnimatedGIF(self.frame_work, ".\\art\\work_tomat.gif")
        gif_work.place(x=147, y=20)
        gif_break = AnimatedGIF(self.frame_break, ".\\art\\break_tomat.gif")
        gif_break.place(x=147, y=20)
        
        self.frame_work.tkraise()
       
        self.root.mainloop()

class AnimatedGIF(tk.Label):
    def __init__(self, master, gif_path):
        tk.Label.__init__(self, master)
        self.gif_frames = []
        self.current_frame = 0

       
        gif = Image.open(gif_path)
        try:
            while True:
                frame = ImageTk.PhotoImage(gif.copy())
                self.gif_frames.append(frame)
                gif.seek(len(self.gif_frames))  
        except EOFError:
            pass  

        self.update_animation()

    def update_animation(self):
        if self.gif_frames:
            self.configure(image=self.gif_frames[self.current_frame], bg= "#c6cbc1")
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            self.after(600, self.update_animation) 

if __name__ == "__main__":
    
    pomodoro = Evil_Pomodoro()
    

    

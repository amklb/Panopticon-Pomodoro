
# Panopticon Pomodoro
### 1. Overview
The idea for this app came from doing a 100daysofcode challenge – I wasn’t aware if I actually coded for an hour or if I just spent 45 minutes out of that to read documentation.
So this simple Pomodoro App checks if you are actually working in the window that you’re supposed to. If not, it will count this time towards a break, not working. 


### 2. Features
* simple work/break timer with a space to insert desired time
* adding allowed apps – the working clock will go forward only if you have one of them open
* total time spent during work and break sessions – working session will count towards a total break time if appropriate window is not opened and active
* cute pixel tomato drawn by me

![podoroapp](https://github.com/user-attachments/assets/30442685-f94d-427a-bade-249cf034d1b2)

### 3. Running the project
1. Clone repository locally
2. `cd` to the project directory
3. Install the dependencies if needed `pip install Pillow`, `pip install pyglet`, `pip install psutil`
4. Run the project in commandline `py -m main`

#### 3.1. Dependencies 
* [psutil](https://psutil.readthedocs.io/en/latest/)
* [Pillow](https://pillow.readthedocs.io/en/stable/)
* [pyglet](https://pyglet.org/)

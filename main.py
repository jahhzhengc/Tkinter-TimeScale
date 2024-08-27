import tkinter as tk 
from tkcalendar import DateEntry
from datetime import datetime, timedelta 
import time
import CalendarWidget
class DateApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Date Countdown App")
        self.geometry("400x300")

        self.playBtn_Img = tk.PhotoImage(file = "play.png")
        # Start Page
        self.start = 0
        self.start_page = StartPage(self)
        self.start_page.pack()

    def show_countdown_page(self, start_date, end_date, duration):
        self.start_page.pack_forget()
        self.countdown_page = CountdownPage(self, start_date, end_date, duration)
        self.countdown_page.pack()

    def show_start_page(self):
        self.countdown_page.pack_forget()
        self.start_page = StartPage(self)
        self.start_page.pack()


class StartPage(tk.Frame):
     
        # tk.Button(self, text="Start date",  command)

    def open_calendar(self): 
        self.calendar_window = tk.Toplevel(self)
        self.calendar_window.title("Calendar")

        self.startDateBtn["state"] = "disabled"
        today = datetime.today()  
        c = CalendarWidget.CalendarWidget(self.calendar_window, today=today, set_date_callback= self.update_button_text, relief="groove")
        c.pack(padx=4, pady=4) 

    def update_button_text(self, btn, selected_date:datetime):
        self.open_calendar_button.config(text=selected_date.strftime("%Y-%m-%d"))
        self.calendar_window.destroy()
        self.calendar_window.update()
        self.open_calendar_button["state"] = "normal"

    def __init__(self, master):
        super().__init__(master)
        
        self.calendar_window = None
        
        self.startDateBtn = tk.Button(self, text="Start Date", command= self.open_calendar)
        self.startDateBtn.grid(row=0, column=1, padx=10, pady=10)


        # tk.Label(self, text="Start Date").grid(row=0, column=0, padx=10, pady=10)
        # self.start_date_entry = DateEntry(self, date_pattern="yyyy-mm-dd")
        # self.start_date_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="End Date").grid(row=1, column=0, padx=10, pady=10)
        self.end_date_entry = DateEntry(self, date_pattern="yyyy-mm-dd")
        self.end_date_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self, text="Duration (minutes)").grid(row=2, column=0, padx=10, pady=10)
        self.duration_entry = tk.Entry(self)
        self.duration_entry.grid(row=2, column=1, padx=10, pady=10)

        self.play_button = tk.Button(self, image= self.master.playBtn_Img, #text="Play", 
                                     command=self.start_countdown)
        self.play_button.config(fg='red', bg ='blue')
        self.play_button.grid(row=3, columnspan=2, pady=20)

    def start_countdown(self):
        self.master.start = time.time()
        self.start_date = datetime.today()# datetime.strptime(self.start_date_entry.get(), "%Y-%m-%d")
        self.end_date = datetime.strptime(self.end_date_entry.get(), "%Y-%m-%d")
        duration = int(self.duration_entry.get()) * 60  # Convert to seconds
        print(f"start date {self.start_date}, end date {self.end_date}")
        self.master.show_countdown_page(self.start_date, self.end_date, duration)
class CountdownPage(tk.Frame):
    def __init__(self, master, start_date, end_date, duration):
        super().__init__(master)

        self.start_date = start_date
        self.end_date = end_date
        self.duration = duration
        self.is_paused = False

        self.total_days = (end_date - start_date).days
        
        self.elapsed_time = 0
        self.current_date = self.start_date
        self.seconds_per_day = self.duration / self.total_days

        self.pauseBtn_Img = tk.PhotoImage(file ="pause.png")
        self.restartBtn_Img = tk.PhotoImage(file ="restart.png")

        self.date_label = tk.Label(self, text=self.current_date.strftime("%Y-%m-%d"), font=("Helvetica", 72))
        self.date_label.pack(pady=20)

        self.back_button = tk.Button(self, text="Back", command=self.master.show_start_page)
        self.back_button.pack(side=tk.LEFT, padx= 10)

        self.play_pause_button = tk.Button(self, image = self.pauseBtn_Img, command=self.play_pause)
        self.play_pause_button.pack(side=tk.LEFT, padx= 10)

        self.restart_button = tk.Button(self,image=  self.restartBtn_Img, command=self.restart)
        self.restart_button.pack(side=tk.LEFT, padx= 10)

        self.update_date()

    def update_date(self):
        if not self.is_paused:
            if self.elapsed_time < self.duration: 
                days_passed = self.elapsed_time / self.seconds_per_day
                self.current_date = self.start_date + timedelta(days=days_passed) 
                self.elapsed_time += 1  # Increment by one second
            else:
                self.current_date = self.end_date
                print("OUT")
            
            self.date_label.config(text=self.current_date.strftime("%Y-%m-%d"))

            if self.current_date < self.end_date:
                self.after(1000, self.update_date)  
            else: 
                print("ITS OVER")
                end = time.time() 
                print(end - self.master.start)

    def play_pause(self):
        self.is_paused = not self.is_paused
        if not self.is_paused: 
            self.play_pause_button.config(image = self.pauseBtn_Img)
            self.update_date()
        else:
            self.play_pause_button.config(image = self.master.playBtn_Img) 

    def restart(self):
        self.current_date = self.start_date
        self.is_paused = False
        self.date_label.config(text=self.current_date.strftime("%Y-%m-%d"))
        self.play_pause_button.config(text="Pause")
        self.update_date()

if __name__ == "__main__":
    app = DateApp()
    app.resizable(False,False)
    app.mainloop()

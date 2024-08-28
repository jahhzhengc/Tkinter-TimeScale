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
    def __init__(self, master):
        super().__init__(master)
        
        self.calendar_window = None
        self.startBtnPressed = False
        self.startDateBtn = tk.Button(self, text="Start Date", command= lambda: self.open_calendar(startBtnPressed=True))

        self.startDateBtn.grid(row=0, column=0, padx=0, pady=10)
        self.endDateBtn = tk.Button(self, text="End Date",command= lambda: self.open_calendar(startBtnPressed=False))
        self.endDateBtn.grid(row=0, column=1, padx=0, pady=10)

        self.start_date = None
        self.end_date = None 

        tk.Label(self, text="Duration (minutes)").grid(row=2, column=0, padx=10, pady=10)
        self.duration_entry = tk.Entry(self)
        self.duration_entry.grid(row=2, column=1, padx=10, pady=10)

        self.play_button = tk.Button(self, text="Start counting down", command=self.start_countdown)
        # self.play_button = tk.Button(self, image= self.master.playBtn_Img, command=self.start_countdown)
        self.play_button.config()
        self.play_button.grid(row=3, columnspan=2, pady=20)

        self.error_label = tk.Label(self, text="", fg= "red") 

        self.error_label.grid(row=4, column=0, padx= 10)

    def open_calendar(self, startBtnPressed:bool): 
        if(self.calendar_window is not None):
            return
        
        self.calendar_window = tk.Toplevel(self)
        self.calendar_window.protocol("WM_DELETE_WINDOW", self.on_closing)
       
        self.startBtnPressed = startBtnPressed 
        self.calendar_window.title("Pick start date" if startBtnPressed else "Pick end date")
  
        today = datetime.today()  
        c = CalendarWidget.CalendarWidget(self.calendar_window, today=today, set_date_callback= self.update_button_text, relief="groove")
        c.pack(padx=4, pady=4) 
          
    def on_closing(self):
        self.calendar_window.destroy()
        self.calendar_window.update()
        self.calendar_window = None
        
    def update_button_text(self, selected_date:datetime):
        # just replace time to 0
        selected_date = selected_date.replace(minute =0, hour = 0, second = 0, microsecond=0)
        if self.startBtnPressed: 
            self.startDateBtn.config(text=selected_date.strftime("%Y-%m-%d"))
            self.start_date = selected_date
        else:
            self.endDateBtn.config(text=selected_date.strftime("%Y-%m-%d"))
            self.end_date = selected_date

        if(self.start_date != None and self.end_date != None):
            print(f"start date: {self.start_date}, end date: {self.end_date}")
            print(f"start date > end_date: {self.start_date >= self.end_date}")

        self.on_closing()

    def show_error_msg(self, msg:str):
        self.error_label.config(text= msg)
   
    def start_countdown(self): 
        if(not self.start_date):
            self.show_error_msg("Please specify start date")
            return
        if(not self.end_date):
            self.show_error_msg("Please specify end date")
            return

        if(self.start_date >= self.end_date):
            self.show_error_msg("Start date cannot be later or equals to End date")
            return
         
        if(not self.duration_entry.get()):
            self.show_error_msg("Please specify duration")
            return
        
        
        # print(len(self.duration_entry.get()) == 0)
        # print(not self.duration_entry.get())
        # if(self.duration_entry.get()
        # if(self.start_date > )
        self.master.start = time.time() 
        duration = int(self.duration_entry.get()) * 60  # Convert to seconds
        # print(f"start date {self.start_date}, end date {self.end_date}")
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

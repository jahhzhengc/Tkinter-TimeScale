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
        
        # Variables
        self.calendar_window = None
        self.startBtnPressed = False # to identify if its start or end date
        self.start_date = None
        self.end_date = None 

        stack0 = tk.Frame(self)
        stack0.pack(fill='x', padx=10,pady=20)

        self.startDateBtn = tk.Button(stack0, text="Start Date", command= lambda: self.open_calendar(startBtnPressed=True))
        self.startDateBtn.pack(side = tk.LEFT, anchor="w")
        tk.Label(stack0, text= " ~ ").pack(side= tk.LEFT)
        self.endDateBtn = tk.Button(stack0, text="End Date",command= lambda: self.open_calendar(startBtnPressed=False))
        self.endDateBtn.pack(side = tk.LEFT, anchor="w")

        stack1 = tk.Frame(self)
        stack1.pack(fill ='x')

        tk.Label(stack1, text="Duration (minutes)").pack(side= tk.LEFT, padx=10,pady=10)
        self.duration_entry = tk.Entry(stack1)
        self.duration_entry.pack(side= tk.LEFT, padx=10,pady=10)
  
        self.play_button = tk.Button(self, text="Start counting down", command=self.start_countdown)
        self.play_button.config() 
        self.play_button.pack(side= tk.TOP, padx=20, pady=20)

        self.error_label = tk.Label(self, text="", fg= "red") 
        self.error_label.pack() 

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
         
        self.master.start = time.time() 
        duration = int(self.duration_entry.get()) * 60  # Convert to seconds 
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
 

        self.date_label = tk.Label(self, text=self.current_date.strftime("%Y-%m-%d"), font=("Helvetica", 72), 
                                   borderwidth = 2, relief ="groove")
        self.date_label.pack(pady=20)

        self.back_button = tk.Button(self, text="Back", command=self.master.show_start_page)
        self.back_button.pack(side=tk.LEFT, padx= 10)

        self.play_pause_button = tk.Button(self, text="Pause", command=self.play_pause)
        self.play_pause_button.pack(side=tk.LEFT, padx= 10)

        self.restart_button = tk.Button(self,text ="Restart", command=self.restart)
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
                end = time.time() 
                print(end - self.master.start)

    def play_pause(self):
        self.is_paused = not self.is_paused
        if not self.is_paused: 
            self.play_pause_button.config(text ="Pause") 
            self.update_date()
        else: 
            self.play_pause_button.config(text="Play")

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

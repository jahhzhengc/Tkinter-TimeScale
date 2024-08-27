import tkinter as tk
import CalendarWidget  # Import your CalendarWidget
import datetime
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Application") 
        self.calendar_window = None

        # self.startDateBtn = tk.Button(self, text="Start Date", command=self.open_calendar(startBtnPressed=True))
        self.startDateBtn = tk.Button(self, text="Start Date", command= lambda: self.open_calendar(startBtnPressed=True))
        self.startDateBtn.pack(pady=20)

        self.endDateBtn = tk.Button(self, text="End Date",command= lambda: self.open_calendar(startBtnPressed=False))
        self.endDateBtn.pack(pady=20)

        self.startBtnPressed= False
        
    def open_calendar(self, startBtnPressed:bool): 
        self.calendar_window = tk.Toplevel(self)
        self.calendar_window.title("Calendar")

        self.startBtnPressed = startBtnPressed
        self.startDateBtn["state"] = "disabled"
        self.endDateBtn["state"] = "disabled"

        today = datetime.datetime.today()  
        c = CalendarWidget.CalendarWidget(self.calendar_window, today=today, set_date_callback= self.update_button_text, relief="groove")
        c.pack(padx=4, pady=4) 

    def update_button_text(self, selected_date:datetime):
        if self.startBtnPressed: 
            self.startDateBtn.config(text=selected_date.strftime("%Y-%m-%d"))
        else:
            self.endDateBtn.config(text=selected_date.strftime("%Y-%m-%d"))

        self.calendar_window.destroy()
        self.calendar_window.update()

        self.startDateBtn["state"] = "normal"
        self.endDateBtn["state"] = "normal"
        
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

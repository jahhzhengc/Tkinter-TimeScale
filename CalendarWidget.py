import tkinter as tk
import calendar 
import datetime 
from dateutil.relativedelta import relativedelta

class CalendarWidget(tk.Frame): 
    def __init__(self, parent, today, set_date_callback= None, **kwargs):
        super().__init__(parent, **kwargs)

        self.cal_frame = tk.Frame(self)
        self.top_frame = tk.Frame(self)

        self.top_frame.pack(fill='x', padx = 10, pady= 10)
        self.cal_frame.pack(fill="x")
        
        self.set_date_callback = set_date_callback

        self.top_left_frame = tk.Frame(self.top_frame)
        self.top_right_frame = tk.Frame(self.top_frame)

        self.top_left_frame.pack(side = tk.LEFT, anchor="w")
        self.top_right_frame.pack(side = tk.RIGHT, anchor="e")
 
        self.back_btn = tk.Button(self.top_right_frame, text ='<', command= self.prevBtn_pressed)
        self.next_btn = tk.Button(self.top_right_frame, text ='>', command= self.nextBtn_pressed)
        self.today_btn = tk.Button(self.top_right_frame, text ='Today', command= self.todayBtn_pressed)

        self.today = today
        
        year = self.today.year
        month = self.today.month
        self.date_label = tk.Label(self.top_left_frame, text= self.today.strftime("%b %Y") , font=("Helvetica", 24))
        self.date_label.pack(side= tk.LEFT)

        self.back_btn.pack(side= tk.LEFT)
        self.today_btn.pack(side= tk.LEFT)
        self.next_btn.pack(side= tk.LEFT)
  
        self.redraw(year, month)

    def todayBtn_pressed(self):
        self.today = datetime.datetime.today()
        self.date_label.config(text= self.today.strftime("%b %Y") )
        month = self.today.month
        year = self.today.year
        self.redraw(year, month)

    def nextBtn_pressed(self):
        month = self.today.month
        year = self.today.year
        addYear = month + 1 > 12
        month = 1 if addYear else month + 1
        year = year + 1 if addYear else year 

        self.today += relativedelta(months = 1) 
        self.date_label.config(text= self.today.strftime("%b %Y") ) 
        self.redraw(year, month)
    
    def prevBtn_pressed(self): 
        month = self.today.month
        year = self.today.year
        deductYear = month - 1 < 1
        month = 12 if deductYear else month - 1
        year = year - 1 if deductYear else year 
        
        self.today -= relativedelta(months = 1) 
        self.date_label.config(text= self.today.strftime("%b %Y") )

        self.redraw(year, month)
    
    def redraw(self, year, month):
        '''Redraws the calendar for the given year and month'''

        for child in self.cal_frame.winfo_children():
            child.destroy()

        calendar.setfirstweekday(calendar.SUNDAY)
 
        for col, day in enumerate(("Su", "Mo", "Tu", "We", "Th", "Fr", "Sa")):
            label = tk.Label(self.cal_frame, text=day, fg ="red")
            label.grid(row=0, column=col, sticky="nsew")
 
        cal = calendar.monthcalendar(year, month)
        for row, week in enumerate(cal):
            for col, day in enumerate(week):
                text = "" if day == 0 else day
                state = "normal" if day > 0 else "disabled"
                cell = tk.Button(self.cal_frame, text=text, state=state, command=lambda day=day: self.set_day(day))
                cell.grid(row=row+1, column=col, sticky="nsew")

    def set_day(self, num):
        self.today = self.today.replace(day = num) 
        print(self.today)
        if self.set_date_callback:
            self.set_date_callback(self.today)
        # return self.today

# root = tk.Tk()

# today = datetime.datetime.today() 
# c = CalendarWidget(root,today=today, relief="groove")
# c.pack(padx=4, pady=4)

# root.mainloop()
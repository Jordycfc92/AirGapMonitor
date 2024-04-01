import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
from traceback import clear_frames
import datetime

print(tk.Tcl().eval('info patchlevel'))

class AirGapMonitorApp:
    def __init__(self, root):
        self.root = root
        self.frames = {} 
        self.initialise_UI()

    def initialise_UI(self):
        #self.root.geometry('400x300') 
        self.root.title("AirGapMonitor")

        # firstPage
        frame1 = tk.Frame(self.root)
        self.frames["firstPage"] = frame1
        frame1.pack(fill="both", expand=True)

        tk.Label(frame1, text="Please input the Coordinates of the Jacking Location").pack()
        
        tk.Label(frame1, text="Jacking Operation Number:").pack()
        self.JackingOperationEntry = tk.Entry(frame1)
        self.JackingOperationEntry.pack() 

        tk.Label(frame1, text="Lowest Astronomical Tide for location:").pack()
        self.lowestTide = tk.Entry(frame1)
        self.lowestTide.pack()

        tk.Label(frame1, text="Latitude:").pack()
        self.latEntry = tk.Entry(frame1)
        self.latEntry.pack()
        
        tk.Label(frame1, text="Longitude:").pack()
        self.longEntry = tk.Entry(frame1)
        self.longEntry.pack()
        
        self.fetch_button = tk.Button(frame1, text="Fetch Data", command=self.fetch_data)
        self.fetch_button.pack()

        # secondPage
        frame2 = tk.Frame(self.root)
        self.frames["secondPage"] = frame2
        waterDepths = [("0100", 30.4), ("0200", 32.1), ("0300", 33.9)]
        ttk.Label(frame2, text="Water Depths").pack()
        tree = ttk.Treeview(frame2, columns=("Time", "Water Depth"), show="headings")
        tree.heading("Time", text="Time")
        tree.heading("Water Depth", text="Water Depth")
        for time, depth in waterDepths:
            tree.insert("", tk.END, values=(time, depth))
        tree.pack()
        next_button = tk.Button(frame2, text="Start Pre-Hold", command=self.start_third_page_timer)
        next_button.pack()

        # thirdPage
        frame3 = tk.Frame(self.root)
        self.frames["thirdPage"] = frame3
        ttk.Label(frame3, text="LiDAR Sensor Readout:").grid(row=0, column=0, sticky="W")
        self.lidar_readout = ttk.Label(frame3, text="Placeholder") 
        self.lidar_readout.grid(row=1, column=0, sticky="W")
        
        ttk.Label(frame3, text="Air Gap Readout:").grid(row=0, column=1, sticky="W")
        self.air_gap_readout = ttk.Label(frame3, text="Placeholder") 
        self.air_gap_readout.grid(row=1, column=1, sticky="W")
        
        ttk.Label(frame3, text="Difference:").grid(row=2, column=0, columnspan=2, sticky="W")
        self.difference_readout = ttk.Label(frame3, text="Calculating...", background="white")
        self.difference_readout.grid(row=3, column=0, columnspan=2, sticky="W")
        
        # Tide Table
        ttk.Label(frame3, text="Tide Table:").grid(row=4, column=0, sticky="W")
        self.tide_table = ttk.Treeview(frame3, columns=("Time", "Tide"), show="headings")
        self.tide_table.heading("Time", text="Time")
        self.tide_table.heading("Tide", text="Tide")
        
        # populate the tide table with actual data
        self.tide_table.grid(row=5, column=0, columnspan=2, sticky="W")

        ttk.Label(frame3, text="Countdown Timer:").grid(row=7, column=0, sticky="W")
        self.timer_label = ttk.Label(frame3, text="60:00")
        self.timer_label.grid(row=7, column=1, sticky="W")

        next_button = tk.Button(frame3, text="Next Hold", command=lambda: self.show_frame("thirdPage"))
        next_button.grid(row=8, column=0, sticky="W")

        self.update_difference()

    def start_third_page_timer(self):
        self.show_frame("thirdPage")
        self.start_timer(60 * 60)  # Start the timer for 60 minutes

    def start_timer(self, seconds):
        self.timer_seconds = seconds
        self.update_timer()

    def update_timer(self):
        if self.timer_seconds > 0:
            #Convert seconds to MM:SS format
            timer_text = str(datetime.timedelta(seconds=self.timer_seconds))
            # Update the timer label
            self.timer_label.config(text=timer_text.split(':')[1] + ":" + timer_text.split(':')[2][:2])
            self.timer_seconds -= 1
            # After 1 second, call update_timer again
            self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="End of hold")

    def update_difference(self):
        # call whenever LiDAR or Air Gap data is updated.
        
        lidar_value = 10  # Placeholder 
        air_gap_value = 9.6  # Placeholder 
        difference = abs(lidar_value - air_gap_value)
        self.difference_readout["text"] = f"{difference:.2f} meters"
        if difference < 0.5:
            self.difference_readout["background"] = "red"
        else:
            self.difference_readout["background"] = "green"


    def clear_frames(self):
        """Hide all frames."""
        for frame in self.frames.values():
            frame.pack_forget()
    
    def show_frame(self, pageName):
        """Clear all frames and show the specified one."""
        self.clear_frames()  # Hide all frames
        frame = self.frames.get(pageName)
        if frame:
            frame.pack(fill="both", expand=True)
            print(f"Showing frame: {pageName}")
        else:
            print(f"Frame not found: {pageName}")



    def fetch_data(self):
        try:
            latitude = float(self.latEntry.get())
            longitude = float(self.longEntry.get())
            if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
                raise ValueError("Latitude must be between -90 and 90 and Longitude must be between -180 and 180.")
            print(f"Fetching data for Latitude: {latitude}, Longitude: {longitude}")
            self.show_frame("secondPage")  # Transition to the secondPage after fetching data.
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def run(self):
        self.show_frame("firstPage") 
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = AirGapMonitorApp(root)
    app.run()

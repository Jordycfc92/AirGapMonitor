import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
from traceback import clear_frames
import datetime
import OperationMonitor

print(tk.Tcl().eval('info patchlevel'))

class AirGapMonitorApp:
    def __init__(self, root):
        self.root = root
        self.frames = {} 
        self.opsMonitor = OperationMonitor.OperationMonitor()
        self.initialise_UI()
        self.update_calculated_airgap_hourly()

    def initialise_UI(self):
        # Set window title and minimum size
        self.root.title("AirGapMonitor")
        self.root.minsize(600, 400)

        # Style configuration
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12))
        style.configure('TLabel', font=('Helvetica', 12), padding=(10, 5))
        style.configure('TEntry', padding=5)

        # firstPage
        frame1 = ttk.Frame(self.root)
        self.frames["firstPage"] = frame1
        frame1.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(frame1, text="Please input the Coordinates of the Jacking Location").pack()
        
        ttk.Label(frame1, text="Jacking Operation Number:").pack()
        self.JackingOperationEntry = ttk.Entry(frame1)
        self.JackingOperationEntry.pack(pady=(0, 10))
        
        ttk.Label(frame1, text="Lowest Astronomical Tide for location:").pack()
        self.lowestTide = ttk.Entry(frame1)
        self.lowestTide.pack(pady=(0, 10))

        ttk.Label(frame1, text="Latitude:").pack()
        self.latEntry = ttk.Entry(frame1)
        self.latEntry.pack(pady=(0, 10))
        
        ttk.Label(frame1, text="Longitude:").pack()
        self.longEntry = ttk.Entry(frame1)
        self.longEntry.pack(pady=(0, 10))
        
        self.fetch_button = ttk.Button(frame1, text="Fetch Data", command=self.fetch_data)
        self.fetch_button.pack()

        # secondPage
        frame2 = ttk.Frame(self.root)
        self.frames["secondPage"] = frame2

        ttk.Label(frame2, text="Leg 1 length:").pack()
        self.leg1_length_entry = ttk.Entry(frame2)
        self.leg1_length_entry.pack(pady=(0, 10))
        
        ttk.Label(frame2, text="Leg 1 penetration:").pack()
        self.leg1_penetration_entry = ttk.Entry(frame2)
        self.leg1_penetration_entry.pack(pady=(0, 10))

        next_button = ttk.Button(frame2, text="Start Pre-Hold", command=self.start_third_page_timer)
        next_button.pack()

        # thirdPage
        frame3 = ttk.Frame(self.root)
        self.frames["thirdPage"] = frame3

        ttk.Label(frame3, text="LiDAR Sensor Readout:").grid(row=0, column=0, sticky="W")
        self.lidar_readout = ttk.Label(frame3, text="Waiting for input")
        self.lidar_readout.grid(row=1, column=0, sticky="W")
        
        ttk.Label(frame3, text="Calculated Airgap:").grid(row=0, column=1, sticky="W")
        self.air_gap_readout = ttk.Label(frame3, text="Waiting")
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

        next_button = ttk.Button(frame3, text="Next Hold", command=self.reset_timer)
        next_button.grid(row=8, column=0, sticky="W")

        finish_button = ttk.Button(frame3, text="Finish Operation", command=self.finish_operation)
        finish_button.grid(row=8, column=1, sticky="W")


        self.update_difference()

    def store_leg1_length_and_pen(self):
        try: 
            leg1_length_input = float(self.leg1_length_entry.get())
            leg1_pen_input = float(self.leg1_penetration_entry.get())
            if not 1.8 < leg1_length_input < 70  or not 0< leg1_pen_input <25 :
                raise ValueError("Leg length must be between 1.8 and 70 and leg penetration must be between 0 and 25")
            self.opsMonitor.leg1length = leg1_length_input
            self.opsMonitor.leg1Penetration = leg1_pen_input
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))


    def update_tide_table(self, lat, lng):
        tide_data = self.collect_tide_data(lat, lng)
        for i in self.tide_table.get_children():
            self.tide_table.delete(i)
        # new tide information
        for time, sg in tide_data:
            self.tide_table.insert("", tk.END, values=(time, sg))

    def start_third_page_timer(self):
        self.store_leg1_length_and_pen()
        self.show_frame("thirdPage")
        self.opsMonitor.preHoldCondition = True
        self.start_timer(60 * 60, True)  # Start the timer for 60 minutes

        # Start updating the LiDAR readout on the GUI
        self.update_lidar_readout()

    def start_timer(self, seconds, reset):
        self.timer_seconds = seconds
        if reset:
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

    def reset_timer(self):
        self.start_timer(60 * 60, False)  # Resetting to 60 minutes
        

    def update_difference(self):
        # current values of the LiDAR airgap and the calculated airgap
        lidar_value = self.opsMonitor.currentLidarAirgap
        calculated_airgap_value = self.opsMonitor.calculatedAirgap

        # Calculate the absolute difference between the LiDAR airgap and the calculated airgap
        difference = abs(lidar_value - calculated_airgap_value)

        # Update the difference_readout label with the difference value
        self.difference_readout["text"] = f"{difference:.2f} meters"

        # Colour difference red is greater than 0.5m difference
        if difference < 0.5:
            self.difference_readout["background"] = "green"
        else:
            self.difference_readout["background"] = "red"


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
            lowest_tide_input = float(self.lowestTide.get())
            if not 0 < lowest_tide_input < 50 :
                raise ValueError("Lowest tide must be between 0 and 50")
            self.opsMonitor.lowesttide = lowest_tide_input
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

        try:
            latitude = float(self.latEntry.get())
            longitude = float(self.longEntry.get())
            if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
                raise ValueError("Latitude must be between -90 and 90 and Longitude must be between -180 and 180.")
            print(f"Fetching data for Latitude: {latitude}, Longitude: {longitude}")
            self.opsMonitor.latitude = latitude
            self.opsMonitor.longitude = longitude

            tide_data = self.opsMonitor.collect_tide_data(latitude, longitude)
            if tide_data:
                self.update_tide_table(tide_data)  # Update the tide table with fetched data
                self.show_frame("secondPage")
            else:
                messagebox.showerror("Data Error", "Failed to fetch tide data.")
            self.show_frame("secondPage")  # Transition to the secondPage after fetching data.
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def update_tide_table(self, tide_data):
        for i in self.tide_table.get_children():
            self.tide_table.delete(i)
        for time, sg in tide_data:
            self.tide_table.insert("", tk.END, values=(time, sg))

    def update_lidar_readout(self):
        if self.opsMonitor.preHoldCondition:
            # Fetch the current LiDAR distance
            self.opsMonitor.monitor_lidar_airgap()
            current_lidar_distance = self.opsMonitor.currentLidarAirgap
            # Update the lidar_readout label
            self.lidar_readout.config(text=f"{current_lidar_distance:.2f} meters")
            # Schedule the next update in 1 second (1000 milliseconds)
            self.root.after(1000, self.update_lidar_readout)
        else:
            # If not in pre-holdn the readout displays nothing
            self.lidar_readout.config(text="N/A")

    def update_calculated_airgap_hourly(self):
        # Example values for latitude, longitude, and lowest tide. Replace with actual values as needed.
        lat = self.opsMonitor.latitude
        lng = self.opsMonitor.longitude
        lowest_tide = self.opsMonitor.lowesttide

        calculated_airgap = self.opsMonitor.monitor_calculated_airgap(lat, lng, lowest_tide)
        if calculated_airgap is not None:
            self.air_gap_readout.config(text=f"{calculated_airgap:.2f} meters")
        else:
            self.air_gap_readout.config(text="Calculation failed")

        # 3600000 milliseconds = 1 hour
        self.root.after(3600000, self.update_calculated_airgap_hourly)

    def finish_operation(self):
        if hasattr(self, 'timer_event'):
            self.root.after_cancel(self.timer_event)
        # Perform any cleanup needed and close the application
        self.opsMonitor.preHoldCondition = False
        self.opsMonitor.lidar.disconnect()
        self.root.destroy()  # This will close the GUI window

    def run(self):
        self.show_frame("firstPage") 
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = AirGapMonitorApp(root)
    app.run()

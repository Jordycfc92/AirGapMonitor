import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
from traceback import clear_frames

print(tk.Tcl().eval('info patchlevel'))

class AirGapMonitorApp:
    def __init__(self, root):
        self.root = root
        self.frames = {} 
        self.initialiseUI()

    def initialiseUI(self):
        #self.root.geometry('400x300') 
        self.root.title("AirGapMonitor")

        # First page
        frame1 = tk.Frame(self.root)
        self.frames["First page"] = frame1
        frame1.pack(fill="both", expand=True)

        tk.Label(frame1, text="Please input the Coordinates of the Jacking Location").pack()
        tk.Label(frame1, text="Jacking Operation Number:").pack()
        self.JackingOperationEntry = tk.Entry(frame1)
        self.JackingOperationEntry.pack()
        tk.Label(frame1, text="Latitude:").pack()
        self.latEntry = tk.Entry(frame1)
        self.latEntry.pack()
        tk.Label(frame1, text="Longitude:").pack()
        self.longEntry = tk.Entry(frame1)
        self.longEntry.pack()
        self.fetch_button = tk.Button(frame1, text="Fetch Data", command=self.fetch_data)
        self.fetch_button.pack()

        # Second page
        frame2 = tk.Frame(self.root)
        self.frames["Second Page"] = frame2
        waterDepths = [("0100", 30.4), ("0200", 32.1), ("0300", 33.9)]
        ttk.Label(frame2, text="Water Depths").pack()
        tree = ttk.Treeview(frame2, columns=("Time", "Water Depth"), show="headings")
        tree.heading("Time", text="Time")
        tree.heading("Water Depth", text="Water Depth")
        for time, depth in waterDepths:
            tree.insert("", tk.END, values=(time, depth))
        tree.pack()
        next_button = tk.Button(frame2, text="Next Page", command=lambda: print("Navigate to next page"))
        next_button.pack()

    def clear_frames(self):
        """Hide all frames."""
        for frame in self.frames.values():
            frame.pack_forget()
    
    def showFrame(self, pageName):
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
            self.showFrame("Second Page")  # Transition to the second page after fetching data.
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def run(self):
        self.showFrame("First page")  # Corrected to match the key exactly
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = AirGapMonitorApp(root)
    app.run()

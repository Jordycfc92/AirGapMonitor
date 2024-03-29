import tkinter as tk
print(tk.Tcl().eval('info patchlevel'))

class AirGapMonitorApp:
    def __init__(self, root):
        self.root = root
        self.initialise_ui()

    def initialise_ui(self):
        # self.root.geometry('400x200') 
        self.root.title("AirGapMonitor")

        tk.Label(self.root, text="Latitude:").pack()
        self.lat_entry = tk.Entry(self.root)
        self.lat_entry.pack()

        tk.Label(self.root, text="Longitude:").pack()
        self.long_entry = tk.Entry(self.root)
        self.long_entry.pack()

        self.fetch_button = tk.Button(self.root, text="Fetch Data", command=self.fetch_data)
        self.fetch_button.pack()
        
    def fetch_data(self):
        
        pass
    

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = AirGapMonitorApp(root)
    app.run()

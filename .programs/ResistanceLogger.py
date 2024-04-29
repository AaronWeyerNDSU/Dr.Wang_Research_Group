import tkinter as tk
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from itertools import count
import pyvisa
import csv
import time
import datetime
import threading

class OhmMeter:
    running = False
    x_values = []
    y_values = []
    index = count()

    # Create an instance of Tkinter window
    master = tk.Tk()

    def __init__(self):
        # Setup Window Parameters
        self.master.title("Resistance Logger")
        self.master.config(background="gray")
        self.master.columnconfigure(0, weight=100)
        
        # Add Start Stop Button.
        self.button = tk.Button(self.master, text="Start", command=self.start_collection)
        self.button.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        # Add status message.
        self.message = tk.Label(self.master, text="Start measurement.")
        self.message.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        # Add FileName field.
        self.fileNameSelect = tk.Button(self.master, text="Save As", command=self.setResistanceFile)
        self.fileNameSelect.grid(column=1, row=0, sticky=tk.E, pady=5)
        self.fileName = tk.Label(self.master, text="Resistance.csv", background="gray")
        self.fileName.grid(column=1, row=1, sticky=tk.E, pady=5)

        # Create a frame to contain the Matplotlib plot
        self.plot_frame = tk.Frame(self.master)
        self.plot_frame.grid(column=0, row=2, columnspan=4)

        # Initialize Matplotlib figure and subplot
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create action for close window.
        self.master.protocol("WM_DELETE_WINDOW", self.__del__)

        # Start main loop.
        self.master.mainloop()

    def __del__(self):
        # self.master.destroy()
        quit()

    def start_collection(self):
        # Set button label.
        self.button.config(text="Stop", command=self.stop_collection)
        
        # Start data collection loop.
        self.running = True

        # Start the data collection thread.
        self.thread = threading.Thread(target=self.measure)
        self.thread.start()
    
    def stop_collection(self):
        # Set button label.
        self.button.config(text="Start", command=self.start_collection)

        # Stop data collection loop.
        self.running = False

    
    def measure(self):
        # Open Resource Manager.
        rm = pyvisa.ResourceManager()

        # List available devices.
        self.message.config(text=rm)
        self.message.config(text=rm.list_resources())

        # Try to connect to Keithley.
        try:
            keithley = rm.open_resource('GPIB0::3::INSTR')
            keithley.write("CONF:RES")
        except:
            # If Keithley cannot be reached, Show error message and stop logger.
            self.message.config(text="ERROR: Check connection with keithley.")
            self.stop_collection()
            return

        # Open file using filename from window.
        file = open(self.fileName.cget("text"), 'a', newline='')

        # Write header to the log file.
        writer = csv.DictWriter(file, fieldnames=['timestamp', 'resistance'])
        writer.writeheader()

        # Get current time in seconds.
        sampleTime = int(time.time())

        # Start data collection loop.
        while(self.running):
            # Wait for beginning of next second
            while(int(time.time()) == sampleTime):
                pass
            sampleTime = int(time.time())

            # Try to read resistance from Keithley ohm meter.
            try:
                resistance = keithley.query("READ?")
                resistance = resistance.split(',')[0]
                resistance = float(resistance)
            except:
                # If Keithley cannot be reached or other error occurs. display message and stop collection.
                self.message.config(text="ERROR: Check connection with keithley.")
                try:
                    keithley.close()
                except:
                    pass
                file.close()
                self.stop_collection()
                return
            
            # Get timestamp
            timeStamp = datetime.datetime.now().isoformat()
            
            # Write timestamp and measured resistance to file. 
            writer.writerow({'timestamp': timeStamp, 'resistance': resistance})

            # Print something to the terminal to verify operation.
            self.message.config(text=f"{timeStamp}\t{resistance}")
            
            # Update plot
            self.update_plot(resistance)
            
        # Cleanup. Close file and stop comms with Keithley.
        try:
            keithley.close()
        except:
            pass
        file.close()

    def update_plot(self, resistance):
        # Clear previous chart.
        self.ax.clear()

        # Append data to lists.
        self.x_values.append(next(self.index))
        self.y_values.append(resistance)

        # Trim old data from display list.
        MAX_DATA_POINTS = 100
        if len(self.x_values) > MAX_DATA_POINTS:
            self.x_values = self.x_values[-MAX_DATA_POINTS:]
            self.y_values = self.y_values[-MAX_DATA_POINTS:]

        # Plot the data.
        self.ax.plot(self.x_values, self.y_values, marker='o', linestyle='-')
        self.ax.set_xlabel('Seconds Elapsed')
        self.ax.set_ylabel('Resistance')
        self.ax.set_title('Resistance over Time')
        self.canvas.draw()

    # select resistance file location.
    def setResistanceFile(self):
        fileName = fd.asksaveasfilename(defaultextension='.csv', filetypes=[("Comma Separated Values", '*.csv')], title="Choose filename")
        self.fileName.config(text=fileName)



# Create an instance of logger class
app = OhmMeter()

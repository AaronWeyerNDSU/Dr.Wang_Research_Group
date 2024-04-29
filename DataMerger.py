from tkinter import filedialog as fd
import tkinter as tk
import pandas

# Define default file locations.
ResistanceFile = "Resistance.csv"
HumidityFile = "Humidity.csv"

# select resistance file location.
def getResistanceFile():
    global ResistanceFile
    ResistanceFile= fd.askopenfilename()
    global resistanceFilePath
    resistanceFilePath.config(text=ResistanceFile)

# select humidity file location.
def getHumidityFile():
    global HumidityFile
    HumidityFile = fd.askopenfilename()
    global HumidityFilePath
    HumidityFilePath.config(text=HumidityFile)

# Merge the files together.
def mergeFiles():
    global mergeStatus
    mergeStatus.config(text="Processing")

    try:
        # Load humidity and temperature data.
        humidity = pandas.read_csv(HumidityFile)
        humidity = humidity[["timestamp", "relative humidity [%RH]", "temperature [degC]"]]

        # Convert timestamp to datetime.
        humidity['timestamp'] = pandas.to_datetime(humidity['timestamp'], format='ISO8601').dt.floor('S')

        # Load resistance data
        resistance = pandas.read_csv(ResistanceFile)
        resistance['timestamp'] = pandas.to_datetime(resistance['timestamp'], format='ISO8601').dt.floor('S')

        # Merge data together based on timestamp.
        merged_df = pandas.merge(humidity, resistance, on='timestamp')

    except Exception as e:
        mergeStatus.config(text=e)
        return
    
    # Save merged data to file.
    merged_df.to_csv("data.csv", index=False)

    mergeStatus.config(text="Saved to 'data.csv'")

# Create window.
root = tk.Tk()
root.title("Data Merger")

# Resistance file select
resistanceButton = tk.Button(root, text="Resistance File", command=lambda: getResistanceFile())
resistanceButton.grid(column=0, row=0, padx=5, pady=5)
resistanceFilePath = tk.Label(root, text=ResistanceFile)
resistanceFilePath.grid(column=1, row=0, padx=5, pady=5)

# Humidity file select
HumidityButton = tk.Button(root, text="Humidity File", command=lambda: getHumidityFile())
HumidityButton.grid(column=0, row=1, padx=5, pady=5)
HumidityFilePath = tk.Label(root, text=HumidityFile)
HumidityFilePath.grid(column=1, row=1, padx=5, pady=5)

# Merge Button and message
mergeButton = tk.Button(root, text="Merge Files", command=lambda: mergeFiles())
mergeButton.grid(column=0, row=2, padx=5, pady=5)
mergeStatus = tk.Label(root, text="")
mergeStatus.grid(column=1, row=2, padx=5, pady=5)

# Start GUI
root.mainloop()

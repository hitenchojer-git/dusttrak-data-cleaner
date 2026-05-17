import pandas as pd
from datetime import datetime
from io import StringIO
from dateutil import parser
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def process_tsi_file(input_filename: str, output_csv: str, output_plot: str) -> None:
    with open(input_filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Extract datetime from metadata
    start_date_raw = next(line for line in lines if "Start Date" in line).split(",")[1].strip()
    start_time_raw = next(line for line in lines if "Start Time" in line).split(",")[1].strip()
    start_datetime = parser.parse(f"{start_date_raw} {start_time_raw}", dayfirst=True)

    # Extract data starting from header line
    header_line_index = next(i for i, line in enumerate(lines) if "Elapsed Time [s]" in line)
    data_str = "".join(lines[header_line_index:])
    df_raw = pd.read_csv(StringIO(data_str))

    expected_cols = ['Elapsed Time [s]', 'PM1 [mg/m3]', 'PM2.5 [mg/m3]', 'PM4 [mg/m3]', 'PM10 [mg/m3]', 'TOTAL [mg/m3]']
    if not all(col in df_raw.columns for col in expected_cols):
        raise ValueError("Expected PM columns not found in the file.")

    df = df_raw[expected_cols].copy()
    df = df.apply(pd.to_numeric, errors='coerce')
    df[expected_cols[1:]] *= 1000  # Convert to µg/m³
    df['Datetime'] = df['Elapsed Time [s]'].apply(lambda x: (start_datetime + pd.to_timedelta(x, unit='s')))

    df = df.rename(columns={
        'PM1 [mg/m3]': 'pm1',
        'PM2.5 [mg/m3]': 'pm2.5',
        'PM4 [mg/m3]': 'pm4',
        'PM10 [mg/m3]': 'pm10',
        'TOTAL [mg/m3]': 'pmt'
    })
    df = df[['Datetime', 'pm1', 'pm2.5', 'pm4', 'pm10', 'pmt']]
    df.to_csv(output_csv, index=False)

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(df['Datetime'], df['pm1'], label='PM₁')
    plt.plot(df['Datetime'], df['pm2.5'], label='PM₂.₅')
    plt.plot(df['Datetime'], df['pm10'], label='PM₁₀')
    plt.xlabel("Datetime")
    plt.ylabel("Concentration (µg/m³)")
    plt.title("Particulate Matter Over Time")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_plot)
    plt.close()

def main():
    root = tk.Tk()
    root.withdraw()

    input_files = filedialog.askopenfilenames(
        title="Select One or More TSI CSV Files",
        filetypes=[("CSV Files", "*.csv")]
    )

    if not input_files:
        return

    success_count = 0
    for file_path in input_files:
        try:
            folder = os.path.dirname(file_path)
            name = os.path.splitext(os.path.basename(file_path))[0]
            output_csv = os.path.join(folder, f"{name}_processed.csv")
            output_plot = os.path.join(folder, f"{name}_processed_plot.png")
            process_tsi_file(file_path, output_csv, output_plot)
            success_count += 1
        except Exception as e:
            messagebox.showerror("Error", f"{os.path.basename(file_path)}\n{str(e)}")

    messagebox.showinfo("Done", f"{success_count} file(s) processed and plotted.")

if __name__ == "__main__":
    main()

import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'flight_delays.csv')

class FlightAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Delay Analyzer v2.0")
        self.root.geometry("500x450")
        self.df = None
        
        self.label_style = {'padx': 10, 'pady': 5}
        
        self.create_widgets()
        
        self.auto_load_data()

    def create_widgets(self):
        tk.Label(self.root, text="Flight Analytics Dashboard", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.status_label = tk.Label(self.root, text="Waiting for Data...", fg="orange")
        self.status_label.pack()

        # Airline Selection
        tk.Label(self.root, text="Select Airline to Analyze:").pack(**self.label_style)
        self.airline_var = tk.StringVar()
        self.airline_dropdown = ttk.Combobox(self.root, textvariable=self.airline_var, state="disabled")
        self.airline_dropdown.pack(pady=5)

        # Action Buttons
        self.calc_button = tk.Button(self.root, text="Calculate Metrics", command=self.calculate_delays, state="disabled", width=20)
        self.calc_button.pack(pady=5)

        self.plot_button = tk.Button(self.root, text="Generate Visual Report", command=self.plot_delays, state="disabled", width=20)
        self.plot_button.pack(pady=5)

        # Results Display
        self.result_text = tk.StringVar()
        tk.Label(self.root, textvariable=self.result_text, justify="left", font=("Courier", 9)).pack(pady=15)

    def auto_load_data(self):
        """Finds the data folder automatically so the user doesn't have to browse."""
        if os.path.exists(DATA_PATH):
            try:
                self.df = pd.read_csv(DATA_PATH)
                self.status_label.config(text=f"CONNECTED: {os.path.basename(DATA_PATH)}", fg="green")
                
                # Unlock the App
                airlines = self.df['Airline'].dropna().unique()
                self.airline_dropdown['values'] = list(airlines)
                self.airline_dropdown.config(state="readonly")
                self.airline_dropdown.current(0)
                self.calc_button.config(state="normal")
                self.plot_button.config(state="normal")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read CSV: {e}")
        else:
            self.status_label.config(text="ERROR: data/flight_delays.csv not found!", fg="red")

    def calculate_delays(self):
        on_time = (self.df['Delay'] == 0).sum() / len(self.df) * 100
        avg_delay = self.df.groupby('Airline')['Delay'].mean().round(2)
        self.result_text.set(f"SYSTEM METRICS:\n---\nOn-Time Performance: {on_time:.2f}%\n\nAvg Delay (min):\n{avg_delay.to_string()}")

    def plot_delays(self):
        selected = self.airline_var.get()
        airline_data = self.df[self.df['Airline'] == selected]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot 1: Scatter
        ax1.scatter(airline_data['Flight Number'], airline_data['Delay'], alpha=0.6, color='#2c3e50')
        ax1.set_title(f"Patterns: {selected}")
        ax1.set_ylabel("Delay (Minutes)")
        
        # Plot 2: Bar
        avg_delays = self.df.groupby('Airline')['Delay'].mean()
        avg_delays.plot(kind='bar', ax=ax2, color='skyblue')
        ax2.set_title("Global Airline Comparison")
        ax2.set_ylabel("Avg Delay")
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = FlightAnalyzerApp(root)
    root.mainloop()
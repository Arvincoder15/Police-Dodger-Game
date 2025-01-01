import tkinter as tk

class TimerApp:
    def __init__(self, master):
        # Initialize the main window and set the title
        self.master = master
        self.master.title("Tkinter Timer")
        
        # Initialize the timer variables
        self.time_left = 0  # Time in seconds
        self.running = False  # Timer state
        
        # Create and pack the label to display the timer
        self.label = tk.Label(master, text="00:00:00", font=("Calibri", 48))
        self.label.pack()
        
        # Create and pack the start button
        self.start_button = tk.Button(master, text="Start", command=self.start_timer)
        self.start_button.pack()
        
        # Create and pack the stop button
        self.stop_button = tk.Button(master, text="Stop", command=self.stop_timer)
        self.stop_button.pack()
        
        # Create and pack the reset button
        self.reset_button = tk.Button(master, text="Reset", command=self.reset_timer)
        self.reset_button.pack()
        
    def start_timer(self):
        # Start the timer if it is not already running
        if not self.running:
            self.running = True
            self.update_timer()  # Start the update loop
    
    def stop_timer(self):
        # Stop the timer
        self.running = False
    
    def reset_timer(self):
        # Reset the timer to zero and update the label
        self.stop_timer()  # Ensure the timer is stopped
        self.time_left = 0  # Reset time
        self.label.config(text="00:00:00")  # Update label text
    
    def update_timer(self):
        # Update the timer display if the timer is running
        if self.running:
            # Calculate hours, minutes, and seconds manually
            hours = self.time_left // 3600
            minutes = (self.time_left % 3600) // 60
            seconds = self.time_left % 60
            
            # Update the label with the formatted time
            self.label.config(text="{:02}:{:02}:{:02}".format(hours, minutes, seconds))

            # Increment the time_left by one second
            self.time_left += 1
            
            # Schedule the next update in 1000 milliseconds (1 second)
            self.master.after(1000, self.update_timer)


# Create the main window and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
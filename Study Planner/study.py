import tkinter as tk
from tkinter import messagebox
import time
import threading
from datetime import datetime, timedelta
import pyttsx3

# Text-to-speech engine setup
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speech speed

# Global control for speech loop
stop_speaking = False

def speak_loop(message):
    global stop_speaking
    while not stop_speaking:
        engine.say(message)
        engine.runAndWait()
        time.sleep(1)

# Function to notify user with repeated voice and messagebox
def notify(subject):
    global stop_speaking
    stop_speaking = False
    message = f"It's time to {subject}"

    # Start speech in a separate thread
    t = threading.Thread(target=speak_loop, args=(message,))
    t.daemon = True
    t.start()

    # Show messagebox to stop speech
    messagebox.showinfo("Reminder", message)
    stop_speaking = True

# Schedule the task
def schedule_task(subject, start_time_str, duration_str):
    try:
        now = datetime.now()
        hour, minute = map(int, start_time_str.split(":"))
        start_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        if start_time < now:
            start_time += timedelta(days=1)

        wait_seconds = (start_time - now).total_seconds()
        duration_minutes = int(duration_str)

        threading.Timer(wait_seconds, lambda: notify(subject)).start()
        task_list.insert(tk.END, f"{subject} at {start_time.strftime('%H:%M')} for {duration_minutes} min")

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# Add a new task
def add_task():
    subject = subject_entry.get()
    time_str = time_entry.get()
    duration = duration_entry.get()

    if subject and time_str and duration:
        schedule_task(subject, time_str, duration)
        subject_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
        duration_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Missing Info", "Please fill all fields")

# Remove selected task
def remove_task():
    selected = task_list.curselection()
    if selected:
        task_list.delete(selected)
    else:
        messagebox.showinfo("Info", "Please select a task to remove.")

# GUI Setup
root = tk.Tk()
root.title("Study Planner with Voice Alert")

tk.Label(root, text="Subject:").grid(row=0, column=0)
tk.Label(root, text="Start Time (HH:MM):").grid(row=1, column=0)
tk.Label(root, text="Duration (minutes):").grid(row=2, column=0)

subject_entry = tk.Entry(root)
subject_entry.grid(row=0, column=1, padx=5, pady=5)

time_entry = tk.Entry(root)
time_entry.grid(row=1, column=1, padx=5, pady=5)

duration_entry = tk.Entry(root)
duration_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Button(root, text="Add Task", command=add_task).grid(row=3, column=0, columnspan=2, pady=5)
tk.Button(root, text="Remove Task", command=remove_task).grid(row=4, column=0, columnspan=2, pady=5)

task_list = tk.Listbox(root, width=40, height=10)
task_list.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()

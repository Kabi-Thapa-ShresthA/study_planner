import tkinter as tk
from tkinter import messagebox
import time
import threading
from datetime import datetime, timedelta
import pyttsx3


class StudyPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Planner with Voice Alert")

        # Text-to-speech engine setup
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)

        self.stop_speaking = False

        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.root, text="Subject:").grid(row=0, column=0)
        tk.Label(self.root, text="Start Time (HH:MM):").grid(row=1, column=0)
        tk.Label(self.root, text="Duration (minutes):").grid(row=2, column=0)

        self.subject_entry = tk.Entry(self.root)
        self.subject_entry.grid(row=0, column=1, padx=5, pady=5)

        self.time_entry = tk.Entry(self.root)
        self.time_entry.grid(row=1, column=1, padx=5, pady=5)

        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Add Task", command=self.add_task).grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(self.root, text="Remove Task", command=self.remove_task).grid(row=4, column=0, columnspan=2, pady=5)

        self.task_list = tk.Listbox(self.root, width=40, height=10)
        self.task_list.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def speak_loop(self, message):
        while not self.stop_speaking:
            self.engine.say(message)
            self.engine.runAndWait()
            time.sleep(1)

    def notify(self, subject):
        self.stop_speaking = False
        message = f"It's time to {subject}"

        t = threading.Thread(target=self.speak_loop, args=(message,))
        t.daemon = True
        t.start()

        messagebox.showinfo("Reminder", message)
        self.stop_speaking = True

    def schedule_task(self, subject, start_time_str, duration_str):
        try:
            now = datetime.now()
            hour, minute = map(int, start_time_str.split(":"))
            start_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

            if start_time < now:
                start_time += timedelta(days=1)

            wait_seconds = (start_time - now).total_seconds()
            duration_minutes = int(duration_str)

            threading.Timer(wait_seconds, lambda: self.notify(subject)).start()
            self.task_list.insert(tk.END, f"{subject} at {start_time.strftime('%H:%M')} for {duration_minutes} min")

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def add_task(self):
        subject = self.subject_entry.get()
        time_str = self.time_entry.get()
        duration = self.duration_entry.get()

        if subject and time_str and duration:
            self.schedule_task(subject, time_str, duration)
            self.subject_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)
            self.duration_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Missing Info", "Please fill all fields")

    def remove_task(self):
        selected = self.task_list.curselection()
        if selected:
            self.task_list.delete(selected)
        else:
            messagebox.showinfo("Info", "Please select a task to remove.")


if __name__ == "__main__":
    root = tk.Tk()
    app = StudyPlanner(root)
    root.mainloop()

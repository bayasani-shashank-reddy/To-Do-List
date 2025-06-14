import tkinter as tk
from tkinter import messagebox, simpledialog

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("400x600")
        self.root.configure(bg="#f0f0f0")  # Set a light background color
        self.tasks = []
        self.completed_tasks = set()
        self.load_tasks()

        # Title label
        title = tk.Label(root, text="To-Do List", font=("Helvetica", 20, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=10)

        # Frame for input
        input_frame = tk.Frame(root, bg="#f0f0f0")  # Match frame background with root
        input_frame.pack(pady=10)

        self.task_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=30, fg="grey", bg="#ffffff")
        self.task_entry.pack(side=tk.LEFT, padx=10)
        self.set_placeholder(self.task_entry, "Enter a task...")
        self.task_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(e, "Enter a task..."))
        self.task_entry.bind("<FocusOut>", lambda e: self.add_placeholder(e, "Enter a task..."))
        self.task_entry.bind('<Return>', lambda event: self.add_task())

        # Customize button colors
        add_btn = tk.Button(input_frame, text="Add Task", command=self.add_task, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        add_btn.pack(side=tk.LEFT)

        # Search bar for live filtering
        search_frame = tk.Frame(root, bg="#f0f0f0")  # Match frame background with root
        search_frame.pack(pady=(10, 0), fill=tk.X, padx=10)
        search_label = tk.Label(search_frame, text="Search:", font=("Helvetica", 14), bg="#f0f0f0", fg="#333")
        search_label.pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, font=("Helvetica", 14), bg="#ffffff")
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self.filter_tasks)

        # Listbox and scrollbar
        list_frame = tk.Frame(root)
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(list_frame, font=("Helvetica", 14), height=15, width=40, yscrollcommand=self.scrollbar.set, bg="#ffffff", fg="#333")
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind('<Double-Button-1>', self.toggle_complete)
        self.scrollbar.config(command=self.listbox.yview)

        # Buttons frame
        buttons_frame = tk.Frame(root, bg="#f0f0f0")  # Match frame background with root
        buttons_frame.pack(pady=10)

        delete_btn = tk.Button(buttons_frame, text="Delete Task", command=self.delete_task, font=("Helvetica", 12), bg="#f44336", fg="white")
        delete_btn.pack(side=tk.LEFT, padx=5)

        edit_btn = tk.Button(buttons_frame, text="Edit Task", command=self.edit_task, font=("Helvetica", 12), bg="#2196F3", fg="white")
        edit_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = tk.Button(buttons_frame, text="Clear All", command=self.clear_all, font=("Helvetica", 12), bg="#9E9E9E", fg="white")
        clear_btn.pack(side=tk.LEFT, padx=5)

        self.refresh_listbox()

    def set_placeholder(self, entry, placeholder):
        entry.delete(0, tk.END)
        entry.insert(0, placeholder)
        entry.config(fg="grey")

    def clear_placeholder(self, event, placeholder):
        entry = event.widget
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def add_placeholder(self, event, placeholder):
        entry = event.widget
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="grey")

    def add_task(self):
        task = self.task_entry.get().strip()
        if task == "" or task == "Enter a task...":
            messagebox.showwarning("Warning", "Please enter a task.")
            return
        self.tasks.append(task)
        self.task_entry.delete(0, tk.END)
        self.save_tasks()
        self.refresh_listbox()

    def delete_task(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to delete.")
            return
        index = selected[0]
        task = self.tasks[index]
        del self.tasks[index]
        if task in self.completed_tasks:
            self.completed_tasks.remove(task)
        self.save_tasks()
        self.refresh_listbox()

    def toggle_complete(self, event=None):
        selected = self.listbox.curselection()
        if not selected:
            return
        index = selected[0]
        task = self.tasks[index]
        if task in self.completed_tasks:
            self.completed_tasks.remove(task)
        else:
            self.completed_tasks.add(task)
        self.refresh_listbox()
        self.save_tasks()

    def edit_task(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to edit.")
            return
        index = selected[0]
        current_task = self.tasks[index]
        new_task = simpledialog.askstring("Edit Task", "Modify task:", initialvalue=current_task)
        if new_task is None:
            return
        new_task = new_task.strip()
        if new_task == "":
            messagebox.showwarning("Warning", "Task cannot be empty.")
            return
        self.tasks[index] = new_task
        if current_task in self.completed_tasks:
            self.completed_tasks.remove(current_task)
            self.completed_tasks.add(new_task)
        self.save_tasks()
        self.refresh_listbox()

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
            self.tasks.clear()
            self.completed_tasks.clear()
            self.save_tasks()
            self.refresh_listbox()

    def filter_tasks(self, event=None):
        search_term = self.search_entry.get().strip().lower()
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            if search_term in task.lower():
                display_task = task + " task is completed" if task in self.completed_tasks else task
                self.listbox.insert(tk.END, display_task)

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            display_task = task + " task is completed" if task in self.completed_tasks else task
            self.listbox.insert(tk.END, display_task)
            if task in self.completed_tasks:
                self.listbox.itemconfig(tk.END, fg="gray")

    def save_tasks(self):
        try:
            with open("tasks.txt", "w", encoding="utf-8") as f:
                for task in self.tasks:
                    status = "1" if task in self.completed_tasks else "0"
                    f.write(f"{status}|{task}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {e}")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        status, task = line.split("|", 1)
                        self.tasks.append(task)
                        if status == "1":
                            self.completed_tasks.add(task)
        except FileNotFoundError:
            pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()


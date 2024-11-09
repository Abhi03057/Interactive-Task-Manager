import psutil
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Task Manager")
        self.root.geometry("800x600")

        # Setup for process table
        self.process_tree = ttk.Treeview(root, columns=('PID', 'Name', 'Status', 'CPU', 'Memory'), show='headings')
        self.process_tree.heading('PID', text='PID')
        self.process_tree.heading('Name', text='Name')
        self.process_tree.heading('Status', text='Status')
        self.process_tree.heading('CPU', text='CPU (%)')
        self.process_tree.heading('Memory', text='Memory (MB)')
        self.process_tree.pack(fill=tk.BOTH, expand=True)

        # Buttons for process management
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill=tk.X)
        tk.Button(btn_frame, text="Kill Process", command=self.kill_process).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(btn_frame, text="Suspend Process", command=self.suspend_process).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(btn_frame, text="Resume Process", command=self.resume_process).pack(side=tk.LEFT, padx=5, pady=5)

        # Setup for resource usage graph
        fig, (self.ax_cpu, self.ax_mem) = plt.subplots(2, 1, figsize=(5, 4))
        fig.tight_layout(pad=2.0)
        self.cpu_usage = []
        self.mem_usage = []
        self.line_cpu, = self.ax_cpu.plot([], [], label='CPU Usage (%)')
        self.line_mem, = self.ax_mem.plot([], [], label='Memory Usage (%)')
        self.ax_cpu.set_ylim(0, 100)
        self.ax_mem.set_ylim(0, 100)
        self.ax_cpu.set_title("CPU Usage (%)")
        self.ax_mem.set_title("Memory Usage (%)")
        self.ax_cpu.set_xlim(0, 50)
        self.ax_mem.set_xlim(0, 50)
        self.canvas = FigureCanvasTkAgg(fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Start update threads
        self.update_process_list()
        self.update_usage_graph()
    
    def update_process_list(self):
        for i in self.process_tree.get_children():
            self.process_tree.delete(i)
        for process in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_info']):
            try:
                pid = process.info['pid']
                name = process.info['name']
                status = process.info['status']
                cpu = process.info['cpu_percent']
                memory = process.info['memory_info'].rss / (1024 * 1024)  # Convert bytes to MB
                self.process_tree.insert('', tk.END, values=(pid, name, status, cpu, memory))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        self.root.after(2000, self.update_process_list)  # Update every 2 seconds

    def update_usage_graph(self):
        self.cpu_usage.append(psutil.cpu_percent())
        self.mem_usage.append(psutil.virtual_memory().percent)
        if len(self.cpu_usage) > 50:
            self.cpu_usage.pop(0)
        if len(self.mem_usage) > 50:
            self.mem_usage.pop(0)
        self.line_cpu.set_xdata(range(len(self.cpu_usage)))
        self.line_cpu.set_ydata(self.cpu_usage)
        self.line_mem.set_xdata(range(len(self.mem_usage)))
        self.line_mem.set_ydata(self.mem_usage)
        self.ax_cpu.relim()
        self.ax_mem.relim()
        self.ax_cpu.autoscale_view()
        self.ax_mem.autoscale_view()
        self.canvas.draw()
        self.root.after(1000, self.update_usage_graph)  # Update every second

    def kill_process(self):
        selected_item = self.process_tree.selection()
        if selected_item:
            pid = self.process_tree.item(selected_item, 'values')[0]
            try:
                psutil.Process(int(pid)).terminate()
                messagebox.showinfo("Process Terminated", f"Process {pid} has been terminated.")
            except psutil.NoSuchProcess:
                messagebox.showwarning("Error", f"Process {pid} does not exist.")
        else:
            messagebox.showwarning("Select Process", "Please select a process to terminate.")

    def suspend_process(self):
        selected_item = self.process_tree.selection()
        if selected_item:
            pid = self.process_tree.item(selected_item, 'values')[0]
            try:
                psutil.Process(int(pid)).suspend()
                messagebox.showinfo("Process Suspended", f"Process {pid} has been suspended.")
            except psutil.NoSuchProcess:
                messagebox.showwarning("Error", f"Process {pid} does not exist.")
        else:
            messagebox.showwarning("Select Process", "Please select a process to suspend.")

    def resume_process(self):
        selected_item = self.process_tree.selection()
        if selected_item:
            pid = self.process_tree.item(selected_item, 'values')[0]
            try:
                psutil.Process(int(pid)).resume()
                messagebox.showinfo("Process Resumed", f"Process {pid} has been resumed.")
            except psutil.NoSuchProcess:
                messagebox.showwarning("Error", f"Process {pid} does not exist.")
        else:
            messagebox.showwarning("Select Process", "Please select a process to resume.")

# Run the Task Manager
if __name__ == "__main__":
    root = tk.Tk()
    task_manager = TaskManager(root)
    root.mainloop()

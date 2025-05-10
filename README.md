🧠 Interactive Task Manager
A graphical task manager application built using Python, Tkinter, and psutil that allows users to monitor and manage system processes and resource usage in real-time.

📌 Features
🪵 Live Process Viewer: Lists all running processes with real-time updates every 2 seconds.

📊 CPU and Memory Graphs: Displays live graphs of CPU and memory usage over time.

✋ Process Control:

Kill processes

Suspend/resume selected processes

🎨 Graphical Interface: Built using Tkinter and matplotlib for a clean and interactive GUI experience.

🛠️ Tech Stack
Python 🐍

Tkinter (GUI)

psutil (Process and system information)

matplotlib (Real-time plotting)

🚀 Getting Started
Prerequisites
Ensure you have Python 3.x installed. Then, install the required packages:

bash
pip install psutil matplotlib


Run the Application
bash
python task_manager.py

🖼️ Interface Overview
Top Panel: Live-updating process list with details: PID, name, status, CPU, and memory usage.

Middle Panel: Buttons to kill, suspend, or resume selected processes.

Bottom Panel: Real-time line graphs for CPU and memory usage over the past 50 seconds.

⚠️ Notes
Some operations (like killing or suspending system processes) may require administrative/root privileges.

Access to certain processes might be restricted depending on your system's permissions.

📄 License
This project is open source and available under the MIT License.

✨ Acknowledgments

psutil
matplotlib
Python’s awesome community ❤️


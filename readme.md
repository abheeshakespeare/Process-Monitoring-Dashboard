# 🖥️ Process Monitoring Dashboard

A lightweight real-time process monitoring dashboard built with Python and Flask. It provides detailed insights into your system’s performance, including CPU and memory usage, along with a list of currently running processes.

---

## 🚀 Features

- 🔄 Real-time updates of CPU and memory usage  
- 📋 List of active processes with details like PID, name, CPU%, memory%  
- ⚙️ Cross-Origin support with Flask-CORS  
- 🧠 Efficient system stats collection using `psutil`

---

## 📦 Tech Stack

- **Backend:** Python, Flask, Flask-CORS  
- **System Monitoring:** psutil  
- **Frontend:** HTML, CSS, JavaScript (inside `templates` and `static` directories)

---

## 🐍 Requirements

Install the following dependencies:

```txt
Flask==2.1.0  
Flask-Cors==3.0.10  
psutil==5.9.0  
```
---

Install Them Using

```bash
pip install -r requirements.txt
```
---
## 📂 Project Structure

```plaintext
  Process-Monitoring-Dashboard/
├── static/              # CSS/JS for frontend
├── templates/           # HTML files (Jinja templates)
├── run.py               # Main Flask application
├── requirements.txt     # Python dependencies
└── README.md
```
---
## ▶️ Running the App

1. Clone the repository
```bash
git clone https://github.com/nirajkr26/Process-Monitoring-Dashboard.git
cd Process-Monitoring-Dashboard
```
2. Set up a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Run the Flask app
```bash
python run.py
```
5. Open in your browser
```link
http://localhost:5000
```
---
## 🤝 Contributing
  ### Pull requests and feedback are welcome!
  ### Fork the repo, make your changes, and submit a PR.
---
## Made with ❤️ by Niraj

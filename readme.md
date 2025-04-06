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

Flask==2.1.0 Flask-Cors==3.0.10 psutil==5.9.0

cpp
Copy
Edit

Install them using:

```bash
pip install -r requirements.txt
📂 Project Structure
csharp
Copy
Edit
Process-Monitoring-Dashboard/
├── static/              # CSS/JS for frontend
├── templates/           # HTML files (Jinja templates)
├── app.py               # Main Flask application
├── requirements.txt     # Python dependencies
└── README.md
▶️ Running the App
Clone the repository

bash
Copy
Edit
git clone https://github.com/nirajkr26/Process-Monitoring-Dashboard.git
cd Process-Monitoring-Dashboard
Set up a virtual environment (recommended)

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the Flask app

bash
Copy
Edit
python app.py
Open in your browser

Go to: http://localhost:5000

📸 Screenshot

📝 Place your screenshot in an assets/ folder and update the filename accordingly.

🤝 Contributing
Pull requests and feedback are welcome! Fork the repo, make your changes, and submit a PR.

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

Made with ❤️ by Niraj

yaml
Copy
Edit

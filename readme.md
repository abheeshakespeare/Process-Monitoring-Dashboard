# 🖥️ Process Monitoring Dashboard

A lightweight real-time process monitoring dashboard built with Python and Flask. It provides detailed insights into your system’s performance, including CPU and memory usage, along with a list of currently running processes.

## 🚀 Features

- 🔄 Real-time updates of CPU and memory usage
- 📋 List of active processes with details like PID, name, CPU%, memory%
- ⚙️ Cross-Origin support with Flask-CORS
- 🧠 Efficient system stats collection using `psutil`

## 📦 Tech Stack

- **Backend:** Python, Flask, Flask-CORS
- **System Monitoring:** psutil
- **Frontend:** HTML, CSS, JavaScript (inside `templates` and `static` directories)

## 🐍 Requirements

Install the following dependencies:

```bash
Flask==2.1.0
Flask-Cors==3.0.10
psutil==5.9.0

You can install them using:

pip install -r requirements.txt

📂 Project Structure

Process-Monitoring-Dashboard/
├── static/              # CSS/JS for frontend
├── templates/           # HTML files (Jinja templates)
├── app.py               # Main Flask application
├── requirements.txt     # Python dependencies
└── README.md

▶️ Running the App
Clone the repository

bash
<code>
git clone https://github.com/nirajkr26/Process-Monitoring-Dashboard.git
cd Process-Monitoring-Dashboard
</code>
Set up virtual environment (optional but recommended)

bash
<code>
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
</code>

Install dependencies

bash
<code>
pip install -r requirements.txt
</code>
Run the Flask app

bash
<code>
python app.py
</code>

Open in your browser
Visit: http://localhost:5000


📸 Screenshot (Optional)
Add a screenshot or GIF here if available

🤝 Contributing
Pull requests and feedback are welcome! Fork the repo and create a PR.

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

Made with ❤️ by Niraj
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from app.system_metrics import SystemMonitor
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

system_monitor = SystemMonitor()

@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html')

@app.route('/api/system-info')
def system_info():
    """Endpoint to get comprehensive system information."""
    return jsonify(system_monitor.get_system_info())

@app.route('/api/performance')
def performance_metrics():
    """Endpoint to get real-time performance metrics."""
    return jsonify({
        'cpu': system_monitor.get_cpu_info(),
        'memory': system_monitor.get_memory_info(),
        'disk': system_monitor.get_disk_info(),
        'network': system_monitor.get_network_info(),
        'performance_history': system_monitor.get_performance_history()
    })

@app.route('/api/processes')
def running_processes():
    """Endpoint to get list of running processes."""
    return jsonify(system_monitor.get_running_processes())

@app.route('/api/process/kill', methods=['POST'])
def kill_process():
    """Endpoint to kill a specific process."""
    pid = request.json.get('pid')
    if not pid:
        return jsonify({'status': 'error', 'message': 'No PID provided'}), 400
    
    result = system_monitor.kill_process(int(pid))
    return jsonify(result)

@app.errorhandler(Exception)
def handle_error(e):
    """Global error handler."""
    return jsonify({
        'status': 'error',
        'message': str(e)
    }), 500

# ... [previous imports and setup remain the same]

@app.route('/api/process/priority', methods=['POST'])
def set_process_priority():
    """Endpoint to set process priority."""
    pid = request.json.get('pid')
    priority = request.json.get('priority')
    
    if not pid or not priority:
        return jsonify({
            'status': 'error', 
            'message': 'PID and priority are required'
        }), 400
    
    result = system_monitor.set_process_priority(int(pid), priority)
    return jsonify(result)
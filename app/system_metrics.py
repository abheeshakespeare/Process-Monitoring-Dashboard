import psutil
import time
import json
import platform
import threading
import subprocess
import logging
from typing import List, Dict, Any

class SystemMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        
        # Performance tracking
        self.performance_history = {
            'cpu': [],
            'memory': [],
            'disk': [],
            'network': []
        }
        self.max_history_length = 50

    def get_system_info(self) -> Dict[str, Any]:
        """Collect comprehensive system information."""
        return {
            'os': platform.system(),
            'release': platform.release(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'total_cores': psutil.cpu_count(logical=False),
            'total_threads': psutil.cpu_count(logical=True),
            'total_memory': psutil.virtual_memory().total / (1024 * 1024)  # MB
        }

    def get_cpu_info(self) -> Dict[str, float]:
        """Get current CPU usage details."""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_freq = psutil.cpu_freq()
        
        self._update_history('cpu', cpu_percent)
        
        return {
            'overall_usage': cpu_percent,
            'current_freq': cpu_freq.current if cpu_freq else 0,
            'min_freq': cpu_freq.min if cpu_freq else 0,
            'max_freq': cpu_freq.max if cpu_freq else 0
        }

    def get_memory_info(self) -> Dict[str, float]:
        """Get memory usage details."""
        memory = psutil.virtual_memory()
        
        self._update_history('memory', memory.percent)
        
        return {
            'total': memory.total / (1024 * 1024),  # Total memory in MB
            'available': memory.available / (1024 * 1024),  # Available memory in MB
            'used': memory.used / (1024 * 1024),  # Used memory in MB
            'percent': memory.percent
        }

    def get_disk_info(self) -> List[Dict[str, Any]]:
        """Get disk usage for all partitions."""
        disk_partitions = psutil.disk_partitions()
        disk_usage = []
        
        for partition in disk_partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_usage.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'total': usage.total / (1024 * 1024 * 1024),  # Total in GB
                    'used': usage.used / (1024 * 1024 * 1024),  # Used in GB
                    'free': usage.free / (1024 * 1024 * 1024),  # Free in GB
                    'percent': usage.percent
                })
            except Exception as e:
                self.logger.error(f"Could not get disk info for {partition.mountpoint}: {e}")
        
        return disk_usage

    def get_network_info(self) -> Dict[str, Any]:
        """Get network usage statistics."""
        net_io = psutil.net_io_counters()
        
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv
        }

    def get_running_processes(self) -> List[Dict[str, Any]]:
        """Get details of all running processes."""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'status', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'user': proc.info['username'],
                    'status': proc.info['status'],
                    'cpu_usage': proc.info['cpu_percent'],
                    'memory_usage': proc.info['memory_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        return sorted(processes, key=lambda x: x['cpu_usage'], reverse=True)[:50]

    def _update_history(self, metric: str, value: float):
        """Update performance history for a given metric."""
        if len(self.performance_history[metric]) >= self.max_history_length:
            self.performance_history[metric].pop(0)
        self.performance_history[metric].append(value)

    def kill_process(self, pid: int) -> Dict[str, Any]:
        """Terminate a process by its PID."""
        try:
            process = psutil.Process(pid)
            process.terminate()
            return {'status': 'success', 'message': f'Process {pid} terminated'}
        except psutil.NoSuchProcess:
            return {'status': 'error', 'message': f'No process found with PID {pid}'}
        except psutil.AccessDenied:
            return {'status': 'error', 'message': f'Access denied to terminate process {pid}'}

    def get_performance_history(self) -> Dict[str, List[float]]:
        """Retrieve performance history for metrics."""
        return self.performance_history
    


    def set_process_priority(self, pid: int, priority_level: str) -> Dict[str, Any]:
        """
        Set process priority.
        Priority levels: 'low', 'normal', 'high', 'realtime'
        """
        try:
            process = psutil.Process(pid)
            
            # Map priority levels to psutil priority values
            priority_map = {
                'low': psutil.IDLE_PRIORITY_CLASS,
                'normal': psutil.NORMAL_PRIORITY_CLASS,
                'high': psutil.HIGH_PRIORITY_CLASS,
                'realtime': psutil.REALTIME_PRIORITY_CLASS
            }
            
            if priority_level.lower() not in priority_map:
                return {
                    'status': 'error', 
                    'message': f'Invalid priority level. Choose from: {", ".join(priority_map.keys())}'
                }
            
            # Set process priority
            process.nice(priority_map[priority_level.lower()])
            
            return {
                'status': 'success', 
                'message': f'Process {pid} priority set to {priority_level}'
            }
        except psutil.NoSuchProcess:
            return {'status': 'error', 'message': f'No process found with PID {pid}'}
        except psutil.AccessDenied:
            return {'status': 'error', 'message': f'Access denied to modify process {pid} priority'}

    def get_running_processes(self) -> List[Dict[str, Any]]:
        """Get details of all running processes with current priority."""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'status', 'cpu_percent', 'memory_percent', 'nice']):
            try:
                # Map nice values to priority levels
                nice = proc.info['nice']
                if nice is None:
                    priority = 'Unknown'
                elif nice < 0:
                    priority = 'High'
                elif nice == 0:
                    priority = 'Normal'
                else:
                    priority = 'Low'
                
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'user': proc.info['username'],
                    'status': proc.info['status'],
                    'cpu_usage': proc.info['cpu_percent'],
                    'memory_usage': proc.info['memory_percent'],
                    'priority': priority
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        return sorted(processes, key=lambda x: x['cpu_usage'], reverse=True)[:50]
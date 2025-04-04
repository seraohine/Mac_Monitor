from flask import Flask, render_template, jsonify
import psutil
import datetime
from collections import defaultdict

app = Flask(__name__)

def get_system_info():
    # 获取系统信息
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    
    # 获取进程信息
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']):
        try:
            info = proc.info
            if info['cpu_percent'] is None or info['memory_percent'] is None:
                continue
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'user': proc.info['username'],
                'cpu': proc.info['cpu_percent'],
                'memory': proc.info['memory_percent'],
                'status': proc.info['status']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return {
        'time': datetime.datetime.now().strftime("%H:%M:%S"),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'cpu_count': psutil.cpu_count(),
        'memory_total': mem.total,
        'memory_used': mem.used,
        'memory_percent': mem.percent,
        'disk_total': disk.total,
        'disk_used': disk.used,
        'disk_percent': disk.percent,
        'network_sent': net.bytes_sent,
        'network_recv': net.bytes_recv,
        'processes': processes
    }

@app.route('/')
def index():
    return render_template('mac_monitor.html')

@app.route('/system_info')
def system_info():
    return jsonify(get_system_info())

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, jsonify
import psutil
import datetime

app = Flask(__name__)


def get_system_info():
    
    mem = psutil.virtual_memory()   #获取内存信息
    disk = psutil.disk_usage('/')   #获取磁盘信息
    net = psutil.net_io_counters()  #获取网络带宽
    
    # 获取进程信息
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']):
        try:
            info = proc.info
            if info['cpu_percent'] is None or info['memory_percent'] is None:
                continue
            processes.append({
                'pid': info['pid'],
                'name': info['name'],
                'user': info['username'] or 'SYSTEM',
                'cpu': info['cpu_percent'],
                'memory': info['memory_percent'],
                'status': info['status']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    # 按CPU使用率排序进程
    processes.sort(key=lambda p: p['cpu'], reverse=True)
    
    return {
        'time': datetime.datetime.now().strftime("%H:%M:%S"),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': mem.percent,
        'disk_percent': disk.percent,
        'network_sent': net.bytes_sent,
        'network_recv': net.bytes_recv,
        'processes': processes[:50]  # 只返回前50个进程
    }

@app.route('/')
def index():
    return render_template('mac_monitor.html')  

@app.route('/api/system_info')
def system_info():
    return jsonify(get_system_info())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
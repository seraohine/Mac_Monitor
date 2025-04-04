from flask import Flask , jsonify , render_template
import psutil
import datetime

app = Flask(__name__)


def get_system_info():
    memory = psutil.virtual_memory()    #获取内存
    disk = psutil.disk_usage('/')       #获取磁盘使用情况
    net = psutil.net_io_counters()      #获取网络带宽
    
    processes = []                      #获取进程信息
    for proc in psutil.process_iter(['pid','name','username','cpu_percent','memory_percent','status']):
        try:
            processes.append({
                'pid':proc.info['pid'],
                'name':proc.info['name'],
                'user':proc.info['username'],
                'cpu':proc.info['cpu_percent'],
                'memory':proc.info['memory_percent'],
                'status':proc.info['status']
            })
        except (psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
            pass
    
    return{
        'time':datetime.datetime.now().strftime("%H:%M:%S"),
        'cpu_percent':psutil.cpu_percent(interval=1),
        'memory_total':memory.total,
        'memory_used':memory.used,
        'memory_percent':memory.percent,
        'disk_total':disk.total,
        'disk_used':disk.used,
        'disk_percent':disk.percent,    
        'network_sent':net.bytes_sent,
        'network_recv':net.bytes_recv,
        'processes': processes
    }
    
@app.route('/system_info')
def system_info():
    return jsonify(get_system_info())

@app.route('/')
def index():
    return render_template('mac_monitor.html')

if __name__ == '__main__' :
    app.run(debug=True)
    
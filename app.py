from flask import Flask , jsonify
import psutil
import datetime

app = Flask(__name__)


def get_system_info():
    memory = psutil.virtual_memory()    #获取内存
    disk = psutil.disk_usage('/')       #获取磁盘使用情况
    net = psutil.net_io_counters()      #获取网络带宽
    
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
        'network_recv':net.bytes_recv
    }
    
@app.route('/system_info')
def system_info():
    return jsonify(get_system_info())

@app.route('/')
def index():
    return "hello,world!"

if __name__ == '__main__' :
    app.run(debug=True)
    
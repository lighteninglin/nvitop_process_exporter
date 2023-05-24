import prometheus_client
from prometheus_client import Counter, Gauge, Info
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask
from psutil import *
from api.metrics import process_gpu
import random
app = Flask(__name__)

REGISTRY = CollectorRegistry(auto_describe=False)
info = Info(
    f"running_process",
    "Information about running processes.",
    labelnames=['pid_rand'],
    registry=REGISTRY)

@app.route('/metrics')
def metrics():
    info.clear()
    tmps = process_gpu()
    # 编写Prom语句并定义一个监控
    for pid, gpu_i, status, used, user, cmd, started, running_time in tmps:
        rand_tmp = random.randint(0,1000)
        # 将参数传入监控项内
        info.labels(f'{pid}_{rand_tmp}').info({'pid': str(pid), 'GPU': str(gpu_i), 'status': str(status), 'used': str(used), 'user': str(user), 'cmd': str(cmd), 'started': str(started), 'running_time': str(running_time)})
    print(info)
    return Response(prometheus_client.generate_latest(REGISTRY),
    mimetype="text/plain")

@app.route('/')
def index():
    return "<h1>Customized Exporter</h1><br> <a href='metrics'>Metrics</a>"

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=54100,debug=True)
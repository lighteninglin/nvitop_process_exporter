from nvitop import Device
import time, datetime

def pprint_secs(secs):
    """Format seconds in a human readable form."""
    now = time.time()
    secs_ago = int(now - secs)
    if secs_ago < 60 * 60 * 24:
        fmt = "%H:%M:%S"
    else:
        fmt = "%Y-%m-%d %H:%M:%S"
    return datetime.datetime.fromtimestamp(secs).strftime(fmt)

def process_gpu():
    tmp = []
    all_devices      = Device.all()
    all_process = list(map(Device.processes, all_devices))
    for device in all_process:
        for pid, gpu_process in device.items():
            print(gpu_process.device.index)
            print(pid)
            print(gpu_process.status())
            print(gpu_process.gpu_memory_human())
            print(gpu_process.username())
            print(gpu_process.command())
            print(pprint_secs(gpu_process.host.create_time()))
            
            # tmp.append((pid, f'GPU:{gpu_process.device.index} PID:{pid} 状态:{gpu_process.status()} 显存占用:{gpu_process.gpu_memory_human()} 用户:{gpu_process.username()} 命令:{gpu_process.command()} 开始时间:{pprint_secs(gpu_process.host.create_time())} 运行时间:{gpu_process.host.running_time_human()}'))
            tmp.append((pid, gpu_process.device.index, gpu_process.status(), gpu_process.gpu_memory_human(), gpu_process.username(), gpu_process.command(), pprint_secs(gpu_process.host.create_time()), gpu_process.host.running_time_human()))
    
    return tmp

if __name__ == "__main__":
    process_gpu()
import psutil
import os

def get_metrics():

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent

    drive = os.environ.get("SystemDrive", "C:") + "\\"
    disk = psutil.disk_usage(drive).percent

    network = psutil.net_io_counters()

    return {
        "cpu": cpu,
        "ram": ram,
        "disk": disk,
        "network_sent": round(network.bytes_sent / (1024 ** 2), 2),
        "network_received": round(network.bytes_recv / (1024 ** 2), 2)
    }